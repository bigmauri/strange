import json
import logging
import os

from workflow.core.pipelines import Pipeline


logging.basicConfig(level=logging.DEBUG)


def main():
    pipeline: Pipeline = Pipeline()
    pipeline.run()
    print(json.dumps(pipeline.info(), indent=2))


if __name__ == '__main__':
    main()