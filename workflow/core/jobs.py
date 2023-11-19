import logging
import sys

from workflow import WorkflowState
from workflow.core import job
from workflow.core.steps import Step

class Job:

    _current_state = WorkflowState.NONE

    def __init__(self):
        self.__load()

    def __load(self):
        self.__PIPELINE = None
        self.__STAGE = None
        self.__JOB = None

    @property
    def name(self): return self.__JOB["name"]

    def start(self, *args, **kwargs):
        self.__PIPELINE = kwargs.get("__pipeline")
        self.__STAGE = kwargs.get("__stage")
        self.__JOB = kwargs.get("__job")
        self.__PIPELINE._current_state, self._current_state = WorkflowState.RUNNING, WorkflowState.RUNNING
        logging.debug(f"Start {self} -> {self.__JOB["name"]}")
        self.notify()

    def stop(self):
        logging.debug(f"Stop {self} -> {self.__JOB["name"]}")
        self._current_state = WorkflowState.COMPLETED
        self.notify()

    @property
    def steps(self): return self.__JOB["steps"]

    def notify(self):
        job, stage, stages = self.__JOB["name"], self.__STAGE.name, self.__PIPELINE._realtime.stages
        index = self.__PIPELINE._realtime.index_of(stage, "stages")
        any_job = any(job in d.values() for d in stages[index]["jobs"])
        if any_job:
            jindex = next((i for i, entry in enumerate(stages[index]["jobs"]) if job in entry.values()), None)
        data = {
            "name": job,
            "state": self._current_state.name,
            "steps": [] if not any_job else stages[index]["jobs"][jindex]["steps"],
        }
        stages[index]["jobs"].append(data) if not any_job else list(d.update(data) for d in stages[index]["jobs"] if job in d.values())

    @job
    def run(self, *args, **kwargs):
        list(Step().run(
            __step=step,
            __job=kwargs.get("__job"),
            __stage=kwargs.get("__stage"),
            __pipeline=kwargs.get("__pipeline")
            ) for step in self.steps)

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"{self.__str__()}: {id(self)}"
