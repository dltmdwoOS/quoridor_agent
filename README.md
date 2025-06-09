# CAU57456 Challenge: Algorithm for Quoridor

## Overview / 개관


This semester's programming challenge is to create an agent that plays the Quoridor game.

이번 학기의 프로그래밍 도전과제는 쿼리도 게임을 하는 에이전트를 만드는 것입니다.

The challenge consists of 4 problems: (1) Heuristic Search, (2) Local Search, (3) Belief-State Search, and (4) Adversarial Search.

도전과제는 4개의 문제로 구성되어 있습니다: (1) 휴리스틱 탐색, (2) 국소 탐색, (3) 믿음공간 탐색, (4) 적대적 탐색.

Based on this codebase, you need to write a program that solves the 4 parts, and if your performance meets the given criteria below, you will earn points.

이 코드베이스를 기준으로 여러분은 4개 부분을 해결하는 프로그램을 작성하고, 아래에 작성된 기준보다 더 높은 성능을 얻으면 됩니다.

The scoring criteria are categorized into Basic, Intermediate, Advanced, and Challenge levels, and your score will be determined based on whether your agent satisfied each level. You will receive 1 point for submitting working code, 2 points for satisfying the Basic-level criteria, 3 points for satisfying the Intermediate-level criteria, and 4 points for satisfying the Advanced-level criteria. You will earn 5 points for defeating the Challenge-level agent, and there are additional bonus points available. Bonus points are applied without exceeding the total score.

채점 기준은 **기초**, **중급**, **고급**, **도전** 단계로 구분되며, 어떤 단계의 기준을 만족했는지에 따라 점수가 결정됩니다. 동작하는 코드를 제출하였을 때 1점, 기초 에이전트를 이겼을 때 2점, 중급 에이전트를 이겼을 때에는 3점, 고급 에이전트를 이겼을 때에는 4점이 주어집니다. 도전 단계의 에이전트를 이겼을 때에는 5점이 주어지며, 별도의 가산점이 주어지는 항목들이 있습니다. 가산점은 점수 합계를 넘지 않는 선에서 적용됩니다.

Below, the detailed PEAS description for each problem is provided. Please write your code based on the PEAS description.

아래에 각 문제의 PEAS 상세정보가 주어져 있습니다. PEAS 상세정보를 바탕으로 여러분의 코드를 작성하세요.

(Are you curious about how to run the evaluation? Then, go to [RUN](./#RUN) section!)

(어떻게 평가를 실행하는지 궁금하다면, [RUN](./#RUN) 부분으로 넘어가세요!)

## PEAS description

### Performance measure (수행지표)

With one exception, everything follows the basic rules of Quoridor. Unlike the movement rules in Quoridor, in this challenge, the number of turns required to move between each cell varies. For example, moving up from a certain cell may take 3 turns, moving right may take 5 turns, moving left may take 1 turn, and moving down may take 4 turns. Different cells have different movement times. All other rules are the same as in Quoridor.

한 가지 사항을 제외하면, 모든 것은 기본적인 쿼리도의 규칙을 따릅니다. 쿼리도의 이동 규칙과 다르게, 이 도전과제 전체에서는 각 칸 사이의 이동에 소요되는 턴 수가 서로 다릅니다. 예를 들어, 어떤 칸에서 위로 갈 때는 3턴이 걸리고, 오른쪽으로 갈 때는 5턴, 왼쪽으로는 1턴, 아래로는 4턴이 걸릴 수 있습니다. 다른 칸에서는 다른 이동시간이 적용됩니다. 이 외의 모든 규칙은 쿼리도와 동일합니다.

The determination of "winning" is done through absolute evaluation. If any action that is not allowed in basic Quoridor is taken, it will result in disqualification. In addition to the actions that are not allowed in the game, there may be additional disqualification conditions depending on the assignment. In case of disqualification, only the base score of 1 point can be earned.

'이겼다'의 판단은 절대평가로 진행됩니다. 기본적인 쿼리도의 규칙을 따르며, 쿼리도에서 할 수 없는 행동을 한 경우에는 실격됩니다.
또한, 게임 내 불가능한 행동 외에도 과제에 따라 서로 다른 실격 조건이 추가됩니다. 실격패인 경우, 제출 기본 점수 1점만 얻을 수 있습니다.

#### Part 4. Adversarial Search

The goal of this problem is to achieve the victory, against other player.

이 문제의 목표는 상대편을 이기는 것입니다.

Each turn of yours, the system will provide current board and ask your next single action.

여러분의 차례마다, 시스템이 현재 판의 상태를 여러분에게 제공하고, 여러분의 다음 행동을 물어볼 것입니다.

- Type: Group Assignment
  형태: 그룹과제

- Disqualification: You will be disqualified if any of the following conditions are violated:

  실격: 다음 조건 중 하나라도 **위반** 하였을 때

  1. For each turn, your algorithm should compute the next action within a minute. 
  
     매 턴마다, 알고리즘은 1분 이내에 다음 행동를 계산하여야 한다.
  2. The additional memory usage of your algorithm should not exceed 1024MB.
  
     알고리즘의 추가 메모리 사용량이 1024MB 이내여야 한다.
  
- Point system
  - Basically, your point will be given as the following equation:
    
    기본적으로, 여러분의 점수는 다음과 같이 계산됩니다.
  
    Point = min[ MAX{ (winning rate in league match) * 6, (winning rate against default) * 3, 1 } , 5 ]
  
  - (winning rate in league match): Average winning rate of all match in the league / 리그전 전체 평균 승률
  
  - (winning rate against default): Average winning rate against default agent (`default.py`) / 기본 에이전트 (`default`) 대비 평균 승률

#### Environment (환경)

도전과제의 환경 구성은 기본적인 쿼리도 판 구성을 따릅니다.

In terms of seven characteristics, the game can be classified as:

환경을 기술하는 7개의 특징을 기준으로, 게임은 다음과 같이 분류됩니다:

- Fully observable (전체관측가능)

  You know everything required to decide your action.

  여러분은 이미 필요한 모든 내용을 알고 있습니다.

- Competitive Multi-agent (경쟁적 다중 에이전트)

  The other agents will do greedy actions to win the game.

  다른 에이전트들은 게임을 이기기 위하여 탐욕적 행동들을 수행합니다.

- Deterministic (결정론적)

  There's no unexpected chances of change on the board when executing the sequence of actions.

  행동을 순서대로 수행할 때, 예상치 못한 변수가 작용하지 않습니다.

- Sequential actions (순차적 행동)

  You should handle the sequence of your actions to play the game.

  게임 플레이를 위해서 필요한 여러분의 행동의 순서를 고민해야 합니다.

- Semi-dynamic performance (준역동적 지표)

  Some winning conditions are related to dynamic things, such as memory usage or time.

  승리조건의 일부 요소는 메모리나 시간의 영향을 받습니다.

- Discrete action, perception, state and time (이산적인 행동, 지각, 상태 및 시간개념)

  All of your actions, perceptions, states and time will be discrete, although you can query about your current memory usage in the computing procedure.

  여러분의 모든 행동, 지각, 상태 및 시간 흐름은 모두 이산적입니다. 여러분이 계산 도중 메모리 사용량을 시스템에 물어볼 수 있다고 하더라도 말입니다.

- Known rules (규칙 알려짐)

  All rules basically follows the original Quoridor game.

  모든 규칙은 기본적으로 원래의 쿼리도 게임을 따릅니다.

#### Actions

You can take one of the following actions.

다음 행동 중의 하나를 할 수 있습니다.

- **MOVE(direction)**: Move your piece to one of the four directions.

  상하좌우 방향 중 하나로 말 옮기기

- **BLOCK(position)**: Place a block at a position.

  특정한 모서리에 장벽 세워서 막기

  Here, the list of applicable edges will be given by the board.

  도로 짓기가 가능한 모서리의 목록은 board가 제공합니다.

#### Sensors

You can perceive the game state, during the search, as follows:

- The board (게임 판)
  - Coordinates of pieces and blocks

    모든 말과 장벽의 위치

  - You can ask the board to the list of applicable actions for.

    가능한 행동에 대해서 게임판 객체에 물어볼 수 있습니다.

- The number of total blocks remained (사용가능한, 남은 장벽 수)

## Structure of evaluation system

평가 시스템의 구조

The evaluation code has the following structure.

평가용 코드는 다음과 같은 구조를 가지고 있습니다.

```text
/                   ... The root of this project
/README.md          ... This README file
/compete.py         ... The entrance file to run the final evaluation code (as a league match)
/board.py           ... The file that specifies programming interface with the board
/actions.py         ... The file that specifies actions to be called
/util.py            ... The file that contains several utilities for board and action definitions.
/agents             ... Directory that contains multiple agents to be tested.
/agents/__init__.py ... Helper code for loading agents to be evaluated
/agents/load.py     ... Helper code for loading agents to be evaluated
/agents/default.py  ... A randomized agent.
/agents/_skeleton.py... A skeleton code for your agent. (You should change the name of file to run your code)
```

All the codes have documentation that specifies what's happening on that code (only in English).

모든 코드는 어떤 동작을 하는 코드인지에 대한 설명이 달려있습니다 (단, 영어로만).

To deeply understand the `board.py` and `actions.py`, you may need some knowlege about [`pyquoridor` library](https://github.com/playquoridor/python-quoridor).

`board.py`와 `actions.py`를 깊게 이해하고 싶다면, [`pyquoridor` library](https://github.com/playquoridor/python-quoridor) 라이브러리에 대한 지식이 필요할 수 있습니다.

### What should I submit?

You should submit an agent python file, which has a similar structure to `/agents/default.py`.
That file should contain a class name `Agent` and that `Agent` class should have a method named `heuristic_search(board)`, `local_search(board, time_limit)`, `belief_state_search(board, time_limit)`, and `adversarial_search(board, time_limit)`.
Please use `/agents/_skeleton.py` as a skeleton code for your submission.

`/agents/default.py`와 비슷하게 생긴 에이전트 코드를 담은 파이썬 파일을 제출해야 합니다.
해당 코드는 `Agent`라는 클래스가 있어야 하고, `Agent` 클래스는 `heuristic_search(board)`, `local_search(board, time_limit)`, `belief_state_search(board, time_limit)` 및 `adversarial_search(board, time_limit)` 메서드를 가지고 있어야 합니다.
편의를 위해서 `/agents/_skeleton.py`를 골격 코드로 사용하여 제출하세요.

Also, you cannot use the followings to reduce your search time:

그리고 시간을 줄이기 위해서 다음에 나열하는 것을 사용하는 행위는 제한됩니다.

- multithreading / 멀티스레딩
- multiprocessing / 멀티프로세싱
- using other libraries other than basic python libraries. / 기본 파이썬 라이브러리 이외에 다른 라이브러리를 사용하는 행위

The TA will check whether you use those things or not. If so, then your evaluation result will be marked as zero.

조교가 여러분이 해당 사항을 사용하였는지 아닌지 확인하게 됩니다. 만약 그렇다면, 해당 평가 점수는 0점으로 처리됩니다.

## RUN

실행

To run the evaluation code, do the following:

1. (Only at the first run) Install the required libraries, by run the following code on your terminal or powershell, etc:

   (최초 실행인 경우만) 다음 코드를 터미널이나 파워쉘 등에서 실행하여, 필요한 라이브러리를 설치하세요.

    ```bash
    pip install -r requirements.txt
    ```

2. Place your code under `/agents` directory.

    여러분의 코드를 `/agents` 디렉터리 밑에 위치시키세요.

3. Execute the evaluation code, by run the following code on a terminal/powershell:

    다음 코드를 실행하여 평가 코드를 실행하세요.

    ```bash 
    python compete.py -p [AGENTS]
    ```
   
    Here, `[AGENTS]` indicates agent names that you will compare. For example, if you want to make a league match between `agent_a`, `agent_b`, and `agent_c`, type:

    여기서, `[AGENTS]`는 비교할 에이전트의 이름입니다. 예를 들어, `agent_a`, `agent_b`, `agent_c` 사이에 리그전 경기를 만들고 싶다면, 아래와 같이 실행하세요:

    ```bash 
    python compete.py -p agent_a agent_b agent_c
    ```

    If you want to print out all computational procedure, then put `--debug` at the end of python call, as follows:

    만약, 모든 계산 과정을 출력해서 보고 싶다면, `--debug`을 파이썬 호출 부분 뒤에 붙여주세요.

    ```bash 
    python compete.py -p agent_a agent_b agent_c --debug
    ```

4. See what's happening.

    어떤 일이 일어나는지를 관찰하세요.

Note: All the codes are tested both on (1) Windows 11 (23H2) with Python 3.9.13 and (2) Ubuntu 22.04 with Python 3.10. Sorry for Mac users, because you may have some unexpected errors.

모든 코드는 윈도우 11 (23H2)와 파이썬 3.9.13 환경과, 우분투 22.04와 파이썬 3.10 환경에서 테스트되었습니다. 예측불가능한 오류가 발생할 수도 있어, 미리 맥 사용자에게 미안하다는 말을 전합니다.
