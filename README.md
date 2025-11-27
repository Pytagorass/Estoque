# Controle de Estoque do Barco-Hotel

Sistema Django focado em monitorar itens, movimentações e relatórios de estoque do barco-hotel Aguapé. O projeto foi criado 100% em Django puro, com validações no `Model`, `ModelForm`, uso de signals quando necessário e uma interface HTML/CSS inspirada nas telas administrativas existentes no Sistema de Gerenciamento do Barco-hotel Aguap.

## Principais recursos

- **Autenticação** nativa do Django com página de login personalizada e enxuta.
- **Catálogo de itens** com alerta de estoque mínimo e campos específicos (código, unidade, observações).
- **Movimentações simples** (entradas e saídas) com painel de indicadores e histórico recente.
- **Relatórios básicos** com resumo dos últimos dias e lista de itens em alerta.
- **Layout responsivo** reutilizando o tema “Aguapé” (sidebar, cards, badges, status pills).

## Estrutura do projeto

```
barcohotel/          # Configurações principais (settings, urls, wsgi/asgi)
catalogo/            # App dedicado ao catálogo de itens (models/forms/views/urls próprios)
controle/            # App operacional (login, movimentações e relatórios)
templates/           # Base.html + telas para catálgo, controle e conta/login
static/css/          # aguape.css com o tema global
media/               # Pasta para uploads
db.sqlite3           # Banco padrão
```

## Pré-requisitos

- Python 3.10+ (o desenvolvimento atual usa 3.13).
- Virtualenv recomendado (`python -m venv .venv`).
- Dependências: somente Django (`pip install django`).

## Passo a passo para rodar

1. **Clonar e entrar na pasta:**
   ```bash
   git clone <repo> estoque
   cd estoque
   ```
2. **Criar/ativar o ambiente virtual:**
   ```bash
   python -m venv .venv
   # PowerShell
   .\.venv\Scripts\Activate.ps1
   ```
3. **Instalar dependências:**
   ```bash
   pip install django
   ```
4. **Aplicar migrações:**
   ```bash
   python manage.py migrate
   ```
5. **Criar um usuário (necessário para login):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Subir o servidor:**
   ```bash
   python manage.py runserver
   ```
7. **Acessar:** abra `http://127.0.0.1:8000/` e use as credenciais criadas.

## Fluxo de uso

1. **Login** – `/login/` para entrar na aplicação.
2. **Dashboard/Relatórios** – `/relatorio/` exibe resumo semanal e alertas.
3. **Movimentações** – `/movimentacao/` registra entradas/saídas rápidas.
4. **Itens** – `/itens/` lista e permite cadastrar/editar/excluir itens ao direcionar para o app `catalogo`.

Todos os endpoints que manipulam dados estão protegidos por `@login_required`.

## Personalização

- `static/css/aguape.css` guarda todo o tema (cores, cards, sidebar, tabelas, alertas).
- `templates/base.html` concentra o layout principal, incluindo o estado especial para a tela de login.

