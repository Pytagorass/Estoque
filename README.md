# Controle de Estoque do Barco-Hotel

Sistema Django focado em monitorar itens, movimentações e relatórios de estoque do barco-hotel Aguapé. O projeto foi criado para ser 100 % server-side, com validações no `Model`, `ModelForm`, signals e interface HTML/CSS inspirada nas telas administrativas existentes do barco.

## Principais recursos

- **Autenticação** nativa do Django com página de login própria.
- **Cadastro de itens** com alerta de estoque mínimo e campos específicos (SKU, unidade, validade, observações, status).
- **Movimentações simples** (entrada/saída) com indicadores e histórico.
- **Relatórios básicos** com resumo dos últimos dias e lista de itens em alerta.
- **Layout responsivo** reutilizando o tema Aguapé (sidebar, cards, badges e status pills).

## Estrutura do projeto

```
barcohotel/          # Configurações principais (settings, urls, wsgi/asgi)
controle/            # Aplicativo com models, forms, views e urls
templates/           # Base.html + telas (controle e conta/login)
static/css/          # aguape.css com tema geral
media/               # Pasta para uploads (vazia no repositório)
db.sqlite3           # Banco padrão (pode ser recriado via migrate)
```

## Pré-requisitos

- Python 3.10+ (desenvolvido com 3.13).
- Virtualenv recomendado (`python -m venv .venv`).
- Dependências: somente Django (`pip install django`).

## Passo a passo para rodar

1. **Clonar e entrar na pasta**:
   ```bash
   git clone <repo> estoque
   cd estoque
   ```
2. **Criar/ativar o ambiente virtual**:
   ```bash
   python -m venv .venv
   # PowerShell
   .\.venv\Scripts\Activate.ps1
   ```
3. **Instalar dependências**:
   ```bash
   pip install django
   ```
4. **Aplicar migrações**:
   ```bash
   python manage.py migrate
   ```
5. **Criar um usuário (necessário para login)**:
   ```bash
   python manage.py createsuperuser
   ```
6. **Subir o servidor**:
   ```bash
   python manage.py runserver
   ```
7. **Acessar**: abra http://127.0.0.1:8000/ e use as credenciais criadas.

## Fluxo de uso

1. **Login** – `/login/` (sem sidebar, conteúdo centralizado).
2. **Dashboard/Relatórios** – `/relatorio/` exibe resumo semanal e alertas.
3. **Movimentações** – `/movimentacao/` para lançar entradas/saídas rápidas.
4. **Itens** – `/itens/` para cadastrar, editar ou excluir itens.

Todos os endpoints que manipulam dados estão protegidos com `@login_required`.

## Personalização

- `static/css/aguape.css` guarda todo o tema (cores, cards, sidebar, tabelas).
- `templates/base.html` concentra o layout (sidebar e estados especiais de login).
- A pasta `media/` está vazia; configure `MEDIA_ROOT`/`MEDIA_URL` conforme necessário.

## Próximos passos sugeridos

- Criar testes específicos para autenticação e restrições de acesso.
- Expandir relatórios com filtros por período e exportação.
- Integrar notificações (e-mail/SMS) para itens em alerta.

---
Projeto mantido com Django puro, sem React ou SQL manual, seguindo as diretrizes do Barco-Hotel Aguapé.
