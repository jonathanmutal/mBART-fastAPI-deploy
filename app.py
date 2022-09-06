# Load general libraries
import random
import string
import time


## load our libraries for the models
from settings.settings import load_model_settings
from modules.mBART import mBART
from staticTypes.requests import InputmBART

## load libraries for logging
from settings.settings import loggerModels


### Load libraries for the API
from fastapi import FastAPI, Request


## models initialization
## change the name of the file for the example
modelsConfiguration = load_model_settings('settings/mBART-large-many-to-many.yml')
mBARTModel = mBART(modelsConfiguration["mBART"])

# Initialize an instance of FastAPI
description ="""
This is an API to deploy mBART models using huggingface, pytorch and fastAPI.
"""

app = FastAPI(
    title="mBART-huggingface-fastAPI-deploy",
    description=description,
    version="0.0.1",
    contact={
        "name": "Jonathan Mutal",
        "url": "https://www.unige.ch/fti/en/faculte/departements/dtim/membrestim/mutal/",
        "email": "jonathan.mutal@unige.ch",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


# the middleware when each http request is done.
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    The moddleware to track all the http requests.
    """
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    loggerModels.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    loggerModels.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response

@app.get("/healthy")
async def root():
    """
    A healthy method to verify that everything works well.
    """
    return {'status': 200}

@app.post("/translate")
async def translate(input: InputmBART):
    """
    The main function of the API to translate:
    input: a list of strings (the input of the models)
    id: the id of the model (to set in settings/models.yml)
    output: the translation of the input
    """
    requestDict = input.dict()
    inputToTranslate = requestDict['input']
    translations = mBARTModel.translate(inputToTranslate)
    
    loggerModels.info('input: {}'.format(inputToTranslate))
    loggerModels.info('predictions: {}'.format(translations))
    return {'predictions': translations, "status": 200}
