import enum
import logging
import os
import re
import sys
import shlex
import subprocess
import tempfile

from workflow import WorkflowState
from workflow.core import step


class ReturnCode(enum.Enum):

    SUCCESS     = 0
    FAILED      = 1


class Step:

    _current_state = WorkflowState.NONE
    __current_process = {"pid": None, "returncode": None, "out": None, "errs": None}

    def __init__(self):
        self.__load()

    def __load(self): pass

    def start(self, *args, **kwargs):
        self.__PIPELINE = kwargs.get("__pipeline")
        self.__STAGE = kwargs.get("__stage")
        self.__JOB = kwargs.get("__job")
        self.__STEP = kwargs.get("__step")
        self.__PIPELINE._current_state, self._current_state = WorkflowState.RUNNING, WorkflowState.RUNNING        
        logging.debug(f"Start {self} -> {self.__STEP['name']}")
        self.notify()

    def stop(self):
        logging.debug(f"Stop {self} -> {self.__STEP['name']}")
        self._current_state = WorkflowState.COMPLETED
        self.notify()

    @step
    def run(self, *args, **kwargs):
        logging.debug(f"command: {self.__STEP['command']}")
        matches = re.findall(r"\$\((.*?)\)", self.__STEP["command"])
        if matches:
            p = subprocess.Popen(shlex.split(matches[0]), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            o = p.stdout
            self.__STEP["command"] = re.sub(r"\$\((.*?)\)", o.read().decode("utf-8").strip("\n"), self.__STEP["command"])

        command = shlex.split(self.__STEP["command"])
        print("@@@@@"*5, end="\n\n", flush=True)
        print(command, flush=True)

        if "cd" not in command:
            if matches:
                process = subprocess.Popen(command, stdin=p.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                process.wait()
                po, pe = p.communicate()

            else:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, errs = [], []
            if process.stdout:
                for lo in process.stdout: out.append(lo.decode("utf-8").rstrip("\n")); print(lo.decode("utf-8").rstrip("\n"))
            if process.stderr:
                for le in process.stderr: errs.append(le.decode("utf-8").rstrip("\n")); print(le.decode("utf-8").rstrip("\n"))
            self.__current_process["pid"] = process.pid
            self.__current_process["returncode"] = process.returncode
            self.__current_process["out"] = out
            self.__current_process["errs"] = errs
        else:
            os.chdir(command[-1])
            print("Moving to >>>", os.getcwd())
            self.__current_process["pid"] = "built-in shell command"
            self.__current_process["returncode"] = 0
            self.__current_process["out"] = f"Moving to >>> {os.getcwd()}"
            self.__current_process["errs"] = None

        print(f"\n{'@@@@@'*5}", flush=True)

    def notify(self):
        step, job, stage, stages = self.__STEP["name"], self.__JOB["name"], self.__STAGE.name, self.__PIPELINE._realtime.stages
        index = self.__PIPELINE._realtime.index_of(stage, "stages")
        j = next((i for i, entry in enumerate(stages[index]["jobs"]) if job in entry.values()), None)
        any_step = any(step in d.values() for d in stages[index]["jobs"][j]["steps"])
        if any_step:
            z = next((i for i, entry in enumerate(stages[index]["jobs"][j]["steps"]) if step in entry.values()), None)
        data = {
            "name": step,
            "state": self._current_state.name,
            "process": {
                "pid": self.__current_process["pid"],
                "result": ReturnCode.SUCCESS.name if self.__current_process["returncode"] == 0 else ReturnCode.FAILED.name,
                "command": self.__STEP["command"].rstrip("\n"),
                "message": {
                    "out": self.__current_process["out"],
                    "errs": self.__current_process["errs"]
                }
            },
        }
        stages[index]["jobs"][j]["steps"].append(data) if not any_step else list(d.update(data) for d in stages[index]["jobs"][j]["steps"] if step in d.values())
        self.__current_process = {"pid": None, "returncode": None, "out": None, "errs": None}

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f"{self.__str__()}: {id(self)}"

