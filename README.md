# Links2u

Clone do Linktree com perfis customizáveis e gerenciamento de links.

[![Live Demo](https://img.shields.io/badge/demo-live-green)](https://links2u-9zim.onrender.com)

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6b206808-c339-4883-8c00-9aaa6b051d82" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5f3d2d39-cbce-45d8-90f1-b092a8c7cdeb" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1aca23e9-28b0-46e6-94b4-33aca4aea4ad" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a4861fc5-aa90-4e09-a670-07ebd84d64d8" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/f7fda915-d890-4c45-9c57-596c2bda519c" />


## Sobre o projeto

Links2u é uma aplicação web inspirada no Linktree. Cada usuário tem uma página pública com seus links, foto de perfil, ícone e wallpaper personalizados.

## Funcionalidades

- Cadastro e login com senha criptografada (bcrypt)
- Upload de foto de perfil via Cloudinary
- Customização de ícone e wallpaper do perfil
- Gerenciamento de links (adicionar, editar, remover)
- Página pública acessível por qualquer pessoa
- Proteção contra IDOR nas rotas autenticadas

## Tecnologias

- Python 3 / FastAPI
- SQLAlchemy + PostgreSQL
- Jinja2 (templates HTML)
- Cloudinary (upload de imagens)
- Deploy: Render

## Como rodar localmente

```bash
git clone https://github.com/gabusaki/linktree
cd linktree
pip install -r requirements.txt
```

Crie um arquivo `.env` com:

```
DATABASE_URL=sua_url_aqui
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

```bash
uvicorn main:app --reload
```

## Deploy

Aplicação hospedada no [Render](https://links2u-9zim.onrender.com) com banco PostgreSQL.
