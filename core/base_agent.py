class BaseAgent:

    """The __init__ method with all attributes listed when asked this u write this """
    def __init__(self,agent_id,name,agent_type):
        self.agent_id=agent_id
        self.name=name
        self.agent_type=agent_type
        self.qualities={}
        self.state={}
        self.memory=[]
        self.known_info={}
        self.strategy="rational"

    """Empty method stubs for perceive(), decide(), act(), update_state() — each with raise NotImplementedError this is the thing u have to write """
    def perceive(self,environment):
        raise NotImplementedError

    def decide(self,perceived_info):
        raise NotImplementedError

    def act(self,decision,environment):
        raise NotImplementedError

    def update_state(self,environment):
        raise NotImplementedError




