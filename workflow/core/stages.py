import logging
import sys

from workflow import WorkflowState
from workflow.core import stage
from workflow.core.jobs import Job



class Stage:

    _current_state = WorkflowState.NONE

    def __init__(self):
        self.__load()


    def __load(self):
        self.__PIPELINE = None
        self.__STAGE = None

    def start(self, *args, **kwargs):
        self.__PIPELINE = kwargs.get("__pipeline")
        self.__STAGE = kwargs.get("__stage")
        self.__PIPELINE._current_state, self._current_state = WorkflowState.RUNNING, WorkflowState.RUNNING
        logging.debug(f"Start {self} -> {self.__STAGE['name']}")
        self.notify()

    def stop(self):
        logging.debug(f"Stop {self} -> {self.__STAGE['name']}")
        self._current_state = WorkflowState.COMPLETED
        self.notify()

    @property
    def name(self): return self.__STAGE["name"]

    @property
    def jobs(self): return self.__STAGE["jobs"]

    def notify(self):
        stage, stages = self.__STAGE["name"], self.__PIPELINE._realtime.stages
        any_stage = self.__PIPELINE._realtime.exists(stage, "stages")
        index = self.__PIPELINE._realtime.index_of(stage, "stages") if any_stage else None
        data = {
            "name": stage,
            "state": self._current_state.name,
            "jobs": [] if not any_stage else self.__PIPELINE._realtime.jobs(stage_index=index)
        }
        self.__PIPELINE._realtime.stages.append(data) if not any_stage else self.__PIPELINE._realtime.update(stage, "stages", data)
            
    @stage
    def run(self, *args, **kwargs):
        list(Job().run(
            __job=job,
            __stage=self,
            __pipeline=kwargs.get("__pipeline")
            ) for job in self.jobs)

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"{self.__str__()}: {id(self)}"
