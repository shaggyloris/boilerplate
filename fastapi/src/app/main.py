import logging
import pathlib
from datetime import timedelta, datetime
import queue
import logging.config, logging.handlers
import yaml
import uvicorn
from fastapi import FastAPI, Security, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from .config import settings
from .schemas import KeyValueIn, KeyValueOut, Token, User, NewUser
from .auth import get_current_user, authenticate_user, create_access_token, add_user_to_db
from .database import get_db

logger = logging.getLogger(__name__)

app = FastAPI(
        title=settings.app_name
        )

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

queue_listener = None

@app.on_event("startup")
async def load_config() -> None:
    # Allows for changing logging configuration and moves logger to a separate process
    log_config_file = pathlib.Path("logging.yaml")
    
    # Get existing logging config
    log_config = uvicorn.config.LOGGING_CONFIG
    if log_config_file.exists():
        try:
            new_log_config = yaml.full_load(log_config_file.read_text())
            log_config.update(new_log_config)
        except Exception as exc:
            print(f"Something went wrong loading file, using default config: {log_config_file} - {exc}")

    log_queue = queue.Queue(-1)
    global queue_listener
    queue_handler = logging.handlers.QueueHandler(log_queue)
    old_handlers = logger.handlers
    queue_listener = logging.handlers.QueueListener(log_queue, *old_handlers, respect_handler_level=True)
    logger.handlers = [queue_handler]
    queue_listener.start()

@app.on_event("shutdown")
def on_app_shutdown():
    global queue_listener
    # Ensures the queue listener is shutdown when the app shuts down
    if queue_listener is not None:
        queue_listener.stop()
        queue_listener = None

@app.post("/token", response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends(),
                db=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
                )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
            )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def index():
    return {"hello": "world"}


@app.post("/add-user")
async def add_user(user: NewUser, db=Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"User {current_user.username} is adding {user.username} to database")
    try:
        add_user_to_db(user, db)
    except ValueError:
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Username {user.username} is unavailable"
                )
    return {"status": "ok", "message": f"{user.username} has been added!"}
