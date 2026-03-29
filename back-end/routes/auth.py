from fastapi import APIRouter, Form, Request, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from database import SessionLocal
from passlib.context import CryptContext
from pydantic import BaseModel, constr
from models import Link, Usuario
from fastapi.templating import Jinja2Templates
import cloudinary
import os

base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "..", "templates"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gerar_senha_hash(senha):
    return pwd_context.hash(senha)

def verificar_senha(senha_digitada, senha_do_banco):
    return pwd_context.verify(senha_digitada, senha_do_banco)

class UserCreate(BaseModel):
    username: str
    password: constr(min_length=3, max_length=72)

router = APIRouter()

@router.post("/usuario")
def criar_usuario(dados: UserCreate):
    db =  SessionLocal()

    print(type(dados.password))

    usuario_existente = db.query(Usuario).filter(Usuario.username == dados.username).first()
    if usuario_existente:
        db.close()
        return {"erro": "Este nome de usuário já está em uso. Escolha outro!"}
    
    senha_criptografada = gerar_senha_hash(dados.password)
    novo_user = Usuario(username=dados.username, hashed_password=senha_criptografada)
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    db.close()
    return {"status": "Usuário criado!", "dados": novo_user.username}

@router.get("/usuarios")
def listar_usuarios():
    db = SessionLocal()
    lista = db.query(Usuario).all()
    db.close()
    return lista

@router.get("/login", response_class=HTMLResponse)
def tela_login(request: Request):
    return templates.TemplateResponse(request, "login.html")

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.username == username).first()

    if not usuario or not verificar_senha(password, usuario.hashed_password):
        db.close()
        return {"erro": "Usuário ou senha incorretos"}
    
    meu_id = usuario.id
    db.close()

    return f'Login deu certo! Seu ID de usuário é: {meu_id}'

@router.post("/auth/login")
def processar_login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.username == username).first()

    if not usuario or not verificar_senha(password, usuario.hashed_password):
        db.close()
        return "Usuário ou senha incorreta!"
    
    request.session["user_id"] = usuario.id
    request.session["username"] = usuario.username
    db.close()
    return RedirectResponse(url=f"/dashboard", status_code=303)

@router.get("/user/{username_digitado}", response_class=HTMLResponse)
def carregar_perfil(request: Request, username_digitado: str):
    db = SessionLocal()
    user = db.query(Usuario).filter(Usuario.username == username_digitado).first()
    if not user:
        db.close()
        return HTMLResponse(content="<h1>Usuário não encontrado</h1>", status_code=404)
    links_do_usuario = db.query(Link).filter(Link.usuario_id == user.id).all()
    db.close()
    return templates.TemplateResponse(request,"perfil.html", {
        "usuario": user.username,
        "links": links_do_usuario,
        "bio": user.bio,
        "foto_url": user.foto_url,
        "fundo_url": user.fundo_url
    })

@router.post("/auth/cadastro")
def cadastrar_perfil(request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()
    usuario_existente = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario_existente:
        db.close()
        return{"erro": "Este nome de usuário já existe. Escolha outro!"}
    senha_criptografada = gerar_senha_hash(password)
    novo_user = Usuario(username=username, hashed_password=senha_criptografada)
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    request.session["user_id"] = novo_user.id
    request.session["username"] = novo_user.username
    db.close()
    return RedirectResponse(url=f"/dashboard", status_code=303)

@router.get("/cadastro", response_class=HTMLResponse)
def tela_cadastro(request: Request):
    return templates.TemplateResponse(request,"cadastro.html")

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@router.get("/dashboard", response_class=HTMLResponse)
def tela_dashboard(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(url="/login", status_code=303)

    user_id = request.session.get("user_id")
    username = request.session.get("username")
    return templates.TemplateResponse(request,"dashboard.html", {
        "user_id": user_id,
        "username": username
    })

@router.get("/editar-perfil", response_class=HTMLResponse)
def tela_editar_perfil(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(url="/login", status_code=303)
        
    user_id = request.session.get("user_id")
    username = request.session.get("username")
    return templates.TemplateResponse(request,"editar_perfil.html", {
        "user_id": user_id,
        "username": username
    })

@router.post("/auth/editar_perfil")
def editar_perfil(request: Request,
    bio: str = Form(None),
    foto_perfil: UploadFile = File(None),
    wallpaper: UploadFile = File(None)
):
    import cloudinary_config

    db = SessionLocal()
    user_id = request.session.get("user_id")
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()

    if bio is not None and bio != "":
        usuario.bio = bio

    if foto_perfil and foto_perfil.filename != "":
        resultado = cloudinary.uploader.upload(foto_perfil.file)
        usuario.foto_url = resultado["secure_url"]
    if wallpaper and wallpaper.filename != "":
        resultado = cloudinary.uploader.upload(wallpaper.file)
        usuario.fundo_url = resultado["secure_url"]
    db.commit()
    db.close()
    return RedirectResponse(url="/dashboard", status_code=303)