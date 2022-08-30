import yaml
import logging
import time


from typing import List, Dict


## logging initialization
logging.config.fileConfig(
    './settings/logging.config',
    defaults={
            'logfilename': 'logging/' + str(time.time()).replace('\.', '') + 'logs_modelOutput.log'
        },
    disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project. 
                                      # This will get the root logger since no logger in the configuration has this name.

loggerModels = logging.getLogger('models') # the name to save the logs from the models

def load_model_settings(path: str) -> Dict[str, str]:
    with open(path, 'r', encoding='utf-8-sig') as f:
        data_loaded = yaml.load(f, Loader=yaml.FullLoader)
    return data_loaded
