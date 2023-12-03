import logging
import os
import json
import random
import sys
import time
import yaml

from workflow import Realtime, WorkflowState
from workflow.core import pipeline
from workflow.core.stages import Stage


class Pipeline:

    __WORKFLOW: dict = None
    __PIPELINE: dict = None
    __PIPELINE_ROOT_DIRECTORY: str = None

    _current_state = WorkflowState.NONE
    _realtime: Realtime = Realtime()

    def __init__(self, document: str = None):
        self.__load(document)
        self._realtime.pipeline = {}
        self._realtime.stages = []


    def __load(self, document):
        document: str = ".workflow.yaml" if document is None else document
        with open(document, "r") as stream:
            self.__WORKFLOW = yaml.safe_load(stream)
        self.__PIPELINE = self.__WORKFLOW["pipeline"]

    def before_start(self): 
        logging.debug("BEFORE START >>> run container")
        self.__PIPELINE_ROOT_DIRECTORY = os.getcwd()
        logging.info(F"REGISTER ROOT DIRECTORY >>> {self.__PIPELINE_ROOT_DIRECTORY}")


    def start(self):
        logging.debug(f"Start {self} -> {self.__PIPELINE['name']}")
        self._current_state = WorkflowState.RUNNING
        self.notify()

    def stop(self):
        logging.debug(f"Stop {self} -> {self.__PIPELINE['name']}")
        self._current_state = WorkflowState.COMPLETED
        self.notify()

    def after_stop(self): 
        logging.debug("AFTER STOP >>> stop container")
        os.chdir(self.__PIPELINE_ROOT_DIRECTORY)
        logging.info(F"BACK TO ROOT DIRECTORY >>> {self.__PIPELINE_ROOT_DIRECTORY}")

    @property
    def stages(self) -> dict: return self.__PIPELINE["stages"]

    @pipeline
    def run(self, *args, **kwargs):
        list(Stage().run(
            __stage=stage,
            __pipeline=self
            ) for stage in self.stages)

    def notify(self):
        stages = self.stages
        data = {
            "name": self.__PIPELINE["name"],
            "state": self._current_state.name,
            "stages": stages if any(stages) else []
        }
        self.pipeline = data


    def info(self):
        return dict(
            status=self._realtime.to_dict(),
            #__meta=self.__PIPELINE
            )

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"{self.__str__()}: {id(self)}"
