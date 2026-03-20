import  os
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi import Body
from fastapi import Form
from database import engine, SessionLocal, Base
from pydantic import BaseModel, constr
from passlib.context import CryptContext
from routes.links import router as links_router
from routes.auth import router as auth_router


base_dir = os.path.dirname(os.path.realpath(__file__))


# Cria a tabela de verdade no arquivo
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(links_router)

templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(base_dir,"static")), name="static")

