## 1. `action.py`

```python
import abc
import logging
import sys
from typing import Tuple, Literal

import pyquoridor.board
from pyquoridor.exceptions import InvalidFence

IS_DEBUG = '--debug' in sys.argv
FENCES_MAX = 10

```

### 1.1. 클래스 `Action` (추상 클래스)

- **속성**
    - `_logger`: `logging.Logger` — 액션 수행 시 디버깅 로그를 남기는 데 사용
- **메서드**
    - `__call__(self, board, avoid_check=False)`
        - **추상 메서드**. 하위 클래스에서 구현
        - **파라미터**
            - `board`: `GameBoard` 인스턴스
            - `avoid_check` (`bool`): `True`이면 승리 검사(`check_winner`) 등을 생략
        - **동작**: 주어진 `board` 객체에 액션을 실행 또는 시뮬레이션
        - **사용 주의**: 직접 호출 불가. 하위 클래스(`MOVE`, `BLOCK`)에서 구현됨.

---

### 1.2. 클래스 `MOVE(Action)`

페awns(말)를 지정한 위치로 이동하는 액션

- **생성자** `__init__(self, player: Literal['black','white'], position: Tuple[int,int])`
    - `player`: `'black'` 또는 `'white'`
    - `position`: 이동할 칸의 `(row, col)` 좌표
    - **검사**: `player`가 `'black'`/`'white'`가 아니면 `AssertionError`
- **표현** `__repr__(self) -> str`
    - 예: `MOVE(4,5) of white`
- **실행** `__call__(self, board, avoid_check=False)`
    - 내부적으로 `board._board.move_pawn(...)` 호출
    - `IS_DEBUG=True`면 디버깅 로그 출력
    - 잘못된 이동 시 `pyquoridor.exceptions.InvalidMove`, 또는 게임 종료 시 `GameOver` 발생

---

### 1.3. 클래스 `BLOCK(Action)`

격자 모서리에 장벽(fence)을 설치하는 액션

- **생성자**
    
    `__init__(self, player: Literal['black','white'], edge: Tuple[int,int], orientation: Literal['horizontal','vertical'])`
    
    - `player`: `'black'` 또는 `'white'`
    - `edge`: 장벽 중심 좌표 `(row, col)`
    - `orientation`: `'horizontal'` 또는 `'vertical'`
    - 내부적으로 `orientation[0]` (`'h'`/`'v'`) 저장
    - **검사**: 남은 장벽 수(`board._board.fences_left`) 확인, 플레이어 유효성
- **표현** `__repr__(self) -> str`
    - 예: `BLOCK_h(3,2) of player black`
- **실행** `__call__(self, board, avoid_check=False)`
    - 남은 장벽 수 확인 후 `board._board.place_fence(...)` 호출
    - 성공 시 `board._fences` 리스트에 `(edge, orientation)` 추가
    - 잘못된 설치 시 `pyquoridor.exceptions.InvalidFence`, 또는 게임 종료 시 `GameOver` 발생

---

### 1.4. 상수

- `FENCES_MAX = 10`: 플레이어별 최대 장벽 수

---

## 2. `board.py`

```python
python
복사편집
import heapq, logging, os, random, sys
from copy import deepcopy
from random import randint as random_integer
from typing import Tuple, List, Literal

from psutil import Process as PUInfo, NoSuchProcess
from pyquoridor.board import Board
from pyquoridor.exceptions import GameOver, InvalidFence, InvalidMove
from pyquoridor.square import MAX_COL, MAX_ROW

from action import Action, BLOCK, MOVE, FENCES_MAX
from util import print_board

IS_DEBUG = '--debug' in sys.argv
IS_RUN   = 'fixed_evaluation' in sys.argv[0]

```

### 클래스 `GameBoard`

Quoridor 게임 보드를 래핑(wrap)하여 **Agent** 구현에 필요한 퍼블릭 API 제공

### 2.1. Private 속성

- `_board`: 내부 `pyquoridor.board.Board` 인스턴스
- `_current_player`: 현재 차례 플레이어 (`'white'`/`'black'`)
- `_initial`, `_current`: 상태 표현(`dict`)을 저장
- `_fences`: 설치된 장벽 리스트
- `_process_info`, `_init_memory`, `_max_memory`: 메모리 사용량 추적
- `_rng`: 내부 난수 생성기
- `_logger`: 로깅용

---

### 2.2. 초기화 & 상태 복원

- **`_initialize(self, start_with_random_fence: int = 0)`** – **(private)**
    - 평가용. 새 게임판 생성, 내부 상태 초기화, 메모리 트래킹 시작
    - **절대** Agent 코드에서 호출 불가
- **`reset_memory_usage(self)`**
    - `_init_memory`, `_max_memory` 초기화 후 즉시 메모리 갱신
- **`set_to_state(self, specific_state: dict=None, is_initial: bool=False)`**
    - `specific_state` 딕셔너리를 기반으로 `_board` 상태 완전 복원
    - `is_initial=True`이면 `_initial` 상태로 덮어쓰기

---

### 2.3. 게임 진행 정보 조회

- **`is_game_end(self) -> bool`**
    
    현재 상태가 게임 종료인지(`Board.game_finished()`) 반환
    
- **`current_player(self) -> Literal['white','black']`**
    
    내부 보드의 `current_player()` 반환
    
- **`get_state(self) -> dict`**
    
    현재 상태 표현을 딥카피하여 반환
    
- **`get_initial_state(self) -> dict`**
    
    초기화된 상태 표현(첫 상태) 딥카피 반환
    
- **`get_position(self, player: Literal['white','black']) -> Tuple[int,int]`**
    
    해당 플레이어 말의 `(row, col)` 좌표 반환
    

---

### 2.4. 가능 행동 목록 조회

- **`get_applicable_moves(self, player: Literal['white','black']=None) -> List[Tuple[int,int]]`**
    1. 인자로 받은(또는 현재 차례) 플레이어가 이동 가능한 모든 칸 좌표 리스트
    2. 내부적으로 `Board.valid_pawn_moves(..., check_winner=False)` 사용
    3. 메모리 사용량 갱신
- **`get_applicable_fences(self, player: Literal['white','black']=None) -> List[Tuple[Tuple[int,int], str]]`**
    1. 남은 장벽 수 확인
    2. 보드 전 영역 순회하며 설치 가능한 `(edge, orientation)` 수집
    3. 메모리 사용량 갱신
- **`number_of_fences_left(self, player: Literal['white','black']) -> int`**
    
    해당 플레이어의 남은 장벽 수
    

---

### 2.5. 메모리 사용량 조회

- **`get_current_memory_usage(self) -> int`**
    
    프로세스의 현재 메모리(USS) 반환
    
- **`get_max_memory_usage(self) -> int`**
    
    세션 시작 이후 최대 메모리 사용량 차이(`_max_memory - _init_memory`) 반환
    

---

### 2.6. 액션 시뮬레이션

- **`simulate_action(self, state: dict=None, *actions: Action) -> dict`**
    1. `state`(없으면 `_initial`)로 복원
    2. 순서대로 `actions`를 `__call__` 실행
    3. 게임 종료(`GameOver`) 발생 시 중단
    4. 최종 상태를 `_current`에 저장 & 딥카피 반환
    5. 메모리 사용량 갱신

---

### 2.7. Private 헬퍼

- **`_update_memory_usage(self)`** – `_max_memory` 갱신
- **`_unique_game_state_identifier(self) -> str`** – `Board.partial_FEN()`
- **`_save_state(self) -> dict`** – 현재 상태를 딕셔너리로 직렬화
- **`_restore_state(self, state: dict)`** – `_save_state` 포맷 복원

> Note: 위 모두 언더바(_)로 시작하므로 Agent 코드에서 직접 사용 불가
> 

---

### 2.8. 모듈 상수 및 export

```python
python
복사편집
__all__ = ['GameBoard', 'IS_DEBUG', 'IS_RUN']

```

- `IS_DEBUG`, `IS_RUN`: 실행 모드 플래그
- `GameBoard`: Agent가 사용할 유일한 클래스

---

## 3. `compete.py`

```python
python
복사편집
import logging, random, psutil as pu
from argparse import ArgumentParser
from collections import defaultdict
from multiprocessing import Process, Queue
from queue import Empty
from random import seed, shuffle, randint
from time import time, sleep
from traceback import format_exc
from itertools import combinations

from agents.load import get_all_agents
from board import GameBoard, InvalidFence, InvalidMove
from evaluator.util import MEGABYTES

GAMES       = 10
TIME_LIMIT  = 60
MEMORY_LIMIT= 1024
QUIT_SIGNAL = 'QUIT'

```

### 3.1. Private 함수

- **`_query(player, player_side, query_queue: Queue, action_queue: Queue)`**
    - 에이전트 모듈 로드 → `Agent(player_side)` 인스턴스화
    - `GameBoard._initialize()` → 루프
        - `query_queue`로 받은 상태로 `set_to_state`
        - `adversarial_search(...)` 호출 → `action_queue`에 결과 전송
- **`_execute(player, player_side, query_queue, action_queue) -> Process`**
    - 별도 프로세스로 `_query` 실행
- **`_info(msg)`**
    - `logging.info` + `print`

> 이 셋 모두 평가 시스템 내부용이며, Agent 구현 시 전혀 사용할 일이 없습니다.
> 

---

### 3.2. 메인 블록 (`if __name__ == '__main__':`)

1. **인자 파싱** (`p`, `-players`, `-debug`)
2. **로거 설정**
3. **리그 매치**
    - 플레이어 조합별 총 `GAMES`번 대결
    - 백·흑 무작위 배정 → `GameBoard` 초기화
    - `_execute`로 프로세스 시작
    - 매 턴마다
        1. `query_queue`에 상태 전송
        2. `action_queue`에서 `TIME_LIMIT+5`초 이내 응답 대기
        3. 메모리·시간 초과, 예외 발생 시 패배 결정
        4. `simulate_action`으로 보드 업데이트
    - 승패 집계 및 로그 출력

---

### 3.3. 핵심 예외 처리

- `Empty` (Timeout)
- `InvalidFence`, `InvalidMove` (잘못된 액션)
- `GameOver` (게임 종료 감지)
- 메모리 오버플로우(1024 MB 초과)
- **결과**: 에러 발생 시 상대방 승리 처리## 1. `action.py`

```python
python
복사편집
import abc
import logging
import sys
from typing import Tuple, Literal

import pyquoridor.board
from pyquoridor.exceptions import InvalidFence

IS_DEBUG = '--debug' in sys.argv
FENCES_MAX = 10

```

### 1.1. 클래스 `Action` (추상 클래스)

- **속성**
    - `_logger`: `logging.Logger` — 액션 수행 시 디버깅 로그를 남기는 데 사용
- **메서드**
    - `__call__(self, board, avoid_check=False)`
        - **추상 메서드**. 하위 클래스에서 구현
        - **파라미터**
            - `board`: `GameBoard` 인스턴스
            - `avoid_check` (`bool`): `True`이면 승리 검사(`check_winner`) 등을 생략
        - **동작**: 주어진 `board` 객체에 액션을 실행 또는 시뮬레이션
        - **사용 주의**: 직접 호출 불가. 하위 클래스(`MOVE`, `BLOCK`)에서 구현됨.

---

### 1.2. 클래스 `MOVE(Action)`

페awns(말)를 지정한 위치로 이동하는 액션

- **생성자** `__init__(self, player: Literal['black','white'], position: Tuple[int,int])`
    - `player`: `'black'` 또는 `'white'`
    - `position`: 이동할 칸의 `(row, col)` 좌표
    - **검사**: `player`가 `'black'`/`'white'`가 아니면 `AssertionError`
- **표현** `__repr__(self) -> str`
    - 예: `MOVE(4,5) of white`
- **실행** `__call__(self, board, avoid_check=False)`
    - 내부적으로 `board._board.move_pawn(...)` 호출
    - `IS_DEBUG=True`면 디버깅 로그 출력
    - 잘못된 이동 시 `pyquoridor.exceptions.InvalidMove`, 또는 게임 종료 시 `GameOver` 발생

---

### 1.3. 클래스 `BLOCK(Action)`

격자 모서리에 장벽(fence)을 설치하는 액션

- **생성자**
    
    `__init__(self, player: Literal['black','white'], edge: Tuple[int,int], orientation: Literal['horizontal','vertical'])`
    
    - `player`: `'black'` 또는 `'white'`
    - `edge`: 장벽 중심 좌표 `(row, col)`
    - `orientation`: `'horizontal'` 또는 `'vertical'`
    - 내부적으로 `orientation[0]` (`'h'`/`'v'`) 저장
    - **검사**: 남은 장벽 수(`board._board.fences_left`) 확인, 플레이어 유효성
- **표현** `__repr__(self) -> str`
    - 예: `BLOCK_h(3,2) of player black`
- **실행** `__call__(self, board, avoid_check=False)`
    - 남은 장벽 수 확인 후 `board._board.place_fence(...)` 호출
    - 성공 시 `board._fences` 리스트에 `(edge, orientation)` 추가
    - 잘못된 설치 시 `pyquoridor.exceptions.InvalidFence`, 또는 게임 종료 시 `GameOver` 발생

---

### 1.4. 상수

- `FENCES_MAX = 10`: 플레이어별 최대 장벽 수

---

## 2. `board.py`

```python
python
복사편집
import heapq, logging, os, random, sys
from copy import deepcopy
from random import randint as random_integer
from typing import Tuple, List, Literal

from psutil import Process as PUInfo, NoSuchProcess
from pyquoridor.board import Board
from pyquoridor.exceptions import GameOver, InvalidFence, InvalidMove
from pyquoridor.square import MAX_COL, MAX_ROW

from action import Action, BLOCK, MOVE, FENCES_MAX
from util import print_board

IS_DEBUG = '--debug' in sys.argv
IS_RUN   = 'fixed_evaluation' in sys.argv[0]

```

### 클래스 `GameBoard`

Quoridor 게임 보드를 래핑(wrap)하여 **Agent** 구현에 필요한 퍼블릭 API 제공

### 2.1. Private 속성

- `_board`: 내부 `pyquoridor.board.Board` 인스턴스
- `_current_player`: 현재 차례 플레이어 (`'white'`/`'black'`)
- `_initial`, `_current`: 상태 표현(`dict`)을 저장
- `_fences`: 설치된 장벽 리스트
- `_process_info`, `_init_memory`, `_max_memory`: 메모리 사용량 추적
- `_rng`: 내부 난수 생성기
- `_logger`: 로깅용

---

### 2.2. 초기화 & 상태 복원

- **`_initialize(self, start_with_random_fence: int = 0)`** – **(private)**
    - 평가용. 새 게임판 생성, 내부 상태 초기화, 메모리 트래킹 시작
    - **절대** Agent 코드에서 호출 불가
- **`reset_memory_usage(self)`**
    - `_init_memory`, `_max_memory` 초기화 후 즉시 메모리 갱신
- **`set_to_state(self, specific_state: dict=None, is_initial: bool=False)`**
    - `specific_state` 딕셔너리를 기반으로 `_board` 상태 완전 복원
    - `is_initial=True`이면 `_initial` 상태로 덮어쓰기

---

### 2.3. 게임 진행 정보 조회

- **`is_game_end(self) -> bool`**
    
    현재 상태가 게임 종료인지(`Board.game_finished()`) 반환
    
- **`current_player(self) -> Literal['white','black']`**
    
    내부 보드의 `current_player()` 반환
    
- **`get_state(self) -> dict`**
    
    현재 상태 표현을 딥카피하여 반환
    
- **`get_initial_state(self) -> dict`**
    
    초기화된 상태 표현(첫 상태) 딥카피 반환
    
- **`get_position(self, player: Literal['white','black']) -> Tuple[int,int]`**
    
    해당 플레이어 말의 `(row, col)` 좌표 반환
    

---

### 2.4. 가능 행동 목록 조회

- **`get_applicable_moves(self, player: Literal['white','black']=None) -> List[Tuple[int,int]]`**
    1. 인자로 받은(또는 현재 차례) 플레이어가 이동 가능한 모든 칸 좌표 리스트
    2. 내부적으로 `Board.valid_pawn_moves(..., check_winner=False)` 사용
    3. 메모리 사용량 갱신
- **`get_applicable_fences(self, player: Literal['white','black']=None) -> List[Tuple[Tuple[int,int], str]]`**
    1. 남은 장벽 수 확인
    2. 보드 전 영역 순회하며 설치 가능한 `(edge, orientation)` 수집
    3. 메모리 사용량 갱신
- **`number_of_fences_left(self, player: Literal['white','black']) -> int`**
    
    해당 플레이어의 남은 장벽 수
    

---

### 2.5. 메모리 사용량 조회

- **`get_current_memory_usage(self) -> int`**
    
    프로세스의 현재 메모리(USS) 반환
    
- **`get_max_memory_usage(self) -> int`**
    
    세션 시작 이후 최대 메모리 사용량 차이(`_max_memory - _init_memory`) 반환
    

---

### 2.6. 액션 시뮬레이션

- **`simulate_action(self, state: dict=None, *actions: Action) -> dict`**
    1. `state`(없으면 `_initial`)로 복원
    2. 순서대로 `actions`를 `__call__` 실행
    3. 게임 종료(`GameOver`) 발생 시 중단
    4. 최종 상태를 `_current`에 저장 & 딥카피 반환
    5. 메모리 사용량 갱신

---

### 2.7. Private 헬퍼

- **`_update_memory_usage(self)`** – `_max_memory` 갱신
- **`_unique_game_state_identifier(self) -> str`** – `Board.partial_FEN()`
- **`_save_state(self) -> dict`** – 현재 상태를 딕셔너리로 직렬화
- **`_restore_state(self, state: dict)`** – `_save_state` 포맷 복원

> Note: 위 모두 언더바(_)로 시작하므로 Agent 코드에서 직접 사용 불가
> 

---

### 2.8. 모듈 상수 및 export

```python
python
복사편집
__all__ = ['GameBoard', 'IS_DEBUG', 'IS_RUN']

```

- `IS_DEBUG`, `IS_RUN`: 실행 모드 플래그
- `GameBoard`: Agent가 사용할 유일한 클래스

---

## 3. `compete.py`

```python
python
복사편집
import logging, random, psutil as pu
from argparse import ArgumentParser
from collections import defaultdict
from multiprocessing import Process, Queue
from queue import Empty
from random import seed, shuffle, randint
from time import time, sleep
from traceback import format_exc
from itertools import combinations

from agents.load import get_all_agents
from board import GameBoard, InvalidFence, InvalidMove
from evaluator.util import MEGABYTES

GAMES       = 10
TIME_LIMIT  = 60
MEMORY_LIMIT= 1024
QUIT_SIGNAL = 'QUIT'

```

### 3.1. Private 함수

- **`_query(player, player_side, query_queue: Queue, action_queue: Queue)`**
    - 에이전트 모듈 로드 → `Agent(player_side)` 인스턴스화
    - `GameBoard._initialize()` → 루프
        - `query_queue`로 받은 상태로 `set_to_state`
        - `adversarial_search(...)` 호출 → `action_queue`에 결과 전송
- **`_execute(player, player_side, query_queue, action_queue) -> Process`**
    - 별도 프로세스로 `_query` 실행
- **`_info(msg)`**
    - `logging.info` + `print`

> 이 셋 모두 평가 시스템 내부용이며, Agent 구현 시 전혀 사용할 일이 없습니다.
> 

---

### 3.2. 메인 블록 (`if __name__ == '__main__':`)

1. **인자 파싱** (`p`, `-players`, `-debug`)
2. **로거 설정**
3. **리그 매치**
    - 플레이어 조합별 총 `GAMES`번 대결
    - 백·흑 무작위 배정 → `GameBoard` 초기화
    - `_execute`로 프로세스 시작
    - 매 턴마다
        1. `query_queue`에 상태 전송
        2. `action_queue`에서 `TIME_LIMIT+5`초 이내 응답 대기
        3. 메모리·시간 초과, 예외 발생 시 패배 결정
        4. `simulate_action`으로 보드 업데이트
    - 승패 집계 및 로그 출력

---

### 3.3. 핵심 예외 처리

- `Empty` (Timeout)
- `InvalidFence`, `InvalidMove` (잘못된 액션)
- `GameOver` (게임 종료 감지)
- 메모리 오버플로우(1024 MB 초과)
- **결과**: 에러 발생 시 상대방 승리 처리