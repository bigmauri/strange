import enum


class Realtime:

    __state = None

    def __init__(self):
        self.__state = {}

    @property
    def pipeline(self): return self.__state["pipeline"]

    @pipeline.setter
    def pipeline(self, value):
        self.__state["pipeline"] = {} 

    @property
    def stages(self): return self.pipeline["stages"]

    @stages.setter
    def stages(self, value):
        self.__state["pipeline"]["stages"] = []

    def jobs(self, stage_index: int):
        return self.stages[stage_index]["jobs"]

    def update(self, property_name: str, property_list: str, data: dict) -> None:
        list(d.update(data) for d in getattr(self, property_list) if property_name in d.values())

    def exists(self, property_name: str, property_list: str) -> bool: 
        return any(property_name in e.values() for e in getattr(self, property_list))

    def index_of(self, property_name: str, property_list: str) -> int:
        return next((i for i, entry in enumerate(getattr(self, property_list)) if property_name in entry.values()), None)

    def to_dict(self):
        return self.__state


class WorkflowState(enum.Enum):

    RUNNING     = 1
    COMPLETED   = 0
    NONE        = 9
