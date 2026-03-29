from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from database import SessionLocal
from models import Link, Usuario
from pydantic import BaseModel


class LinkUpdate(BaseModel):
    nome: str
    url: str

router = APIRouter()

base_dir = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "..", "templates"))

@router.get("/links")
def get_links():
    db = SessionLocal()
    links = db.query(Link).all()
    db.close()
    return links

@router.post("/links")
def add_link(nome: str, url: str, id_do_dono: int):
    db = SessionLocal()
    novo_link = Link(nome=nome, url=url, usuario_id=id_do_dono)
    db.add(novo_link)
    db.commit()
    db.refresh(novo_link)
    db.close()
    return {"status": "Link vinculado ao usuário!", "link": novo_link}

@router.delete("/links/{link_id}")
def deletar_link(link_id: int):
    db = SessionLocal()
    link = db.query(Link).filter(Link.id == link_id).first()
    
    if not link:
        db.close()
        return {"erro": "Link não encontrado! Verifique o ID no GET /links"}
    
    db.delete(link)
    db.commit()
    db.close()
    return {"status": f"Link {link_id} deletado com sucesso!"}

@router.put("/links/{link_id}")
def editar_link(link_id: int, dados: LinkUpdate):
    db = SessionLocal()
    link = db.query(Link).filter(Link.id == link_id).first()

    if not link:
        db.close()
        return {"erro": "Link não encontrado!"}
    
    link.nome = dados.nome
    link.url = dados.url

    db.commit()
    db.refresh(link)
    db.close()
    return{"status": "Link atualizado!", "link": link}

@router.get("/gerenciar/{user_id}")
def gerenciar_links(request: Request, user_id: int):
    if not request.session.get("user_id"):
        return RedirectResponse(url="/login", status_code=303)
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    links = db.query(Link).filter(Link.usuario_id == user_id).all()
    db.close()
    return templates.TemplateResponse(request,"gerenciar_links.html", {
        "links": links,
        "user_id": user_id,
        "username": usuario.username
    })


@router.post("/links/adicionar")
def adicionar_link(user_id: int = Form(...), nome : str = Form(...), url: str = Form(...)):
    db = SessionLocal()
    novo_link = Link(nome=nome, url=url, usuario_id=user_id)
    db.add(novo_link)
    db.commit()
    db.close()
    return RedirectResponse(url=f'/gerenciar/{user_id}', status_code=303)

@router.post("/links/deletar/{link_id}")
def deletar_link(link_id: int, user_id: int = Form(...)):
    db = SessionLocal()
    link = db.query(Link).filter(Link.id == link_id).first()
    if link:
        db.delete(link)
        db.commit()
    db.close()
    return RedirectResponse(url=f"/gerenciar/{user_id}", status_code=303)
