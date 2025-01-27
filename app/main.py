from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.http.middleware import log_request_response_middleware
from app.infrastructure.http.response import MsgSpecJSONResponse
from app.presentation.api.auth_api import auth_router
from app.presentation.api.user_api import user_router

app = FastAPI(
    title='FastAPI Boilerplate',
    description='Clean Architecture boilerplate for FastAPI apps',
    version='0.1.0',
    swagger_ui_parameters={'persistAuthorization': True},
    default_response_class=MsgSpecJSONResponse,
)

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.middleware('http')(log_request_response_middleware)

# router
app.include_router(auth_router, prefix='/api/v1')
app.include_router(user_router, prefix='/api/v1')
