from pathlib import Path


def get_all_agents(agent_names):
    """
    Load all agents in the current directory

    :return: List of agent file names
    """

    agents = []
    for code in Path(__file__).parent.glob('*.py'):  # Query for all python files in this directory
        if code.stem in agent_names:  # If the file name doesn't match with special file names,
            agents.append(code.stem)  # Include them

    return sorted(agents)


# Export only getter function
__all__ = ['get_all_agents']
