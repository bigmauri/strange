"""
Entrypoint for the 'strange' python module.

Description:
    It is a WORKFLOW Engine.

---

Example

SIMPLE USAGE
1) Simple Case
>>> python -u -m workflow --debug --run  # it runs the '.workflow.yaml' file in the current directory

Thanks to 'git' most beautiful VCS.
Thanks to 'python', it makes me feel good while coding as always.
"""
import argparse
import json
import logging
import os

from workflow.core.pipelines import Pipeline

# LOG - Setup
logging.basicConfig(level=logging.DEBUG)


# STATIC VARIABLES - Setup
WORKFLOW_EXTENSION = ".workflow.yaml"

def exit_in_case_no_workflow():
    """
    Terminate the application in case no '*.workflow.yaml' reached from the command line parser and
    pretty print the parser.help in console.

    :return: None   
    """
    if not any([f.endswith(WORKFLOW_EXTENSION) for f in os.listdir()]):
        print()
        parser.print_help()
        print()
        exit(0)


# ARGUMENT PARSER - Setup
parser = argparse.ArgumentParser(description="Workflow engine command line interface")
parser.add_argument(
    "--debug",
    action="store_true",
    help="Print out the JSON result of the pipeline workflow"
)
parser.add_argument(
    "--run",
    action="store_true",
    help="Print out the JSON result of the pipeline workflow"
)
arguments = parser.parse_args()

# CURRENT DIRECTORY - Validation
exit_in_case_no_workflow()

# WORKFLOW PIPELINE - Execution
pipeline: Pipeline = Pipeline()
pipeline.run() if arguments.run else None
print(json.dumps(pipeline.info(), indent=2)) if arguments.debug else None
