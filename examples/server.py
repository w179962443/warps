import json
import logging
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pyhocon import ConfigFactory
from entities.server_entity import * 
from pipeline import PipelineSolver

conf = ConfigFactory.parse_file('configs/base_config.conf')
logger = logging.getLogger(__name__)

app = FastAPI(
    title='warp',
    default_response_class=JSONResponse,
    description='内部测试',
    version='0.0.1'
)
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], allow_credentials=True
)

solver=PipelineSolver()



@app.post("/warp_chatgpt",response_model=WarpChatgptOutput)
def warp_chatgpt(request: WarpChatgptInput):
    logger.info()
    return 








