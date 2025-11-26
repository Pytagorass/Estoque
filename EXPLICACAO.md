# Guia de implementação – Controle de Estoque do Barco-Hotel

Este documento resume as principais decisões tomadas ao construir o projeto e serve como apoio para futuras manutenções.

## Objetivo

Modernizar o controle de estoque do barco-hotel Aguapé utilizando apenas recursos nativos do Django (models, forms, views, templates), seguindo o visual do sistema já existente do cliente.

## Estrutura criada

- **barcohotel/**: pacote raiz com `settings.py`, `urls.py`, `views.py`, `wsgi.py` e `asgi.py`.
  - `settings.py` define `LOGIN_URL`, paths de `templates/` e `static/`, além do banco SQLite padrão.
  - `urls.py` inclui as rotas do app `controle` e os arquivos de mídia em modo debug.
  - `views.home` redireciona para o dashboard (`controle:relatorio`).
- **controle/**: app principal com tudo sobre itens, movimentações e relatórios.
  - `models.py`: `Item` e `Movimentacao` (com validações em `clean` e ajuste automático do saldo no `save`).
  - `forms.py`: `ItemForm`, `MovimentacaoForm` e `LoginForm` (herda de `AuthenticationForm`).
  - `views.py`: todas as telas protegidas via `@login_required`, além das classes `LoginPageView`/`LogoutPageView`.
  - `urls.py`: define rotas para login, logout, cadastros, movimentações e relatório.
- **templates/**: layout base + pastas `controle/` e `conta/`.
  - `base.html`: contém sidebar, cabeçalho e variações para esconder a barra no login.
  - `templates/conta/login.html`: formulário centralizado com o tema Aguapé.
  - `templates/controle/*.html`: páginas de itens, movimentação e relatório usando cards e tabelas.
- **static/css/aguape.css**: tema inspirado nas telas do cliente (sidebar verde, cards arredondados, badges, status pills). Inclui estados especiais para a tela de login.
- **README.md**: passo a passo para instalar, configurar, criar superusuário e rodar o sistema.
- **EXPLICACAO.md** (este arquivo): guia textual das decisões.

## Fluxo de autenticação

1. Todas as views de negócio são decoradas com `@login_required`.
2. `LOGIN_URL`, `LOGIN_REDIRECT_URL` e `LOGOUT_REDIRECT_URL` estão definidos em `barcohotel/settings.py`.
3. `controle/views.LoginPageView` usa `LoginForm` (subclasse de `AuthenticationForm`).
4. `templates/base.html` detecta a rota `login` para remover a sidebar e centralizar o conteúdo.

## Regras de negócio

- **Item**: controla nome, código de estoque, unidade, estoque mínimo e flag `ativo`. O método `em_alerta` compara `estoque_atual` com o mínimo.
- **Movimentação**: `Entrada`/`Saída` com quantidade positiva. O `save` atualiza automaticamente o saldo do item.
- **Relatório básico**: resume as últimas movimentações (7 dias), mostra contagem de itens e alertas.

## Como evoluir

- Adicionar filtros no relatório (por data e tipo).
- Criar exports (CSV/PDF) a partir das tabelas de itens e movimentações.
- Implementar notificações ou webhooks quando `em_alerta` for verdadeiro.
- Usar testes automatizados (pytest/django test) para validar a lógica de estoque.

Mantendo este guia atualizado, qualquer novo desenvolvedor terá uma visão clara de como o projeto foi concebido.
