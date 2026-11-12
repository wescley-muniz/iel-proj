# Sistema de Materiais

Aplicação web local desenvolvida em Python com Flask para gerenciar um cadastro de materiais em ambiente de uso interno. O sistema permite cadastrar itens, escanear códigos de barras, manter o catálogo organizado e controlar o acesso por meio de login de usuário.

## Visão geral

O projeto foi pensado para uso local em um computador ou rede interna simples. Ele salva os dados em um banco SQLite dentro da pasta `instance`, mantendo o catálogo disponível entre execuções da aplicação.

A aplicação oferece:

- cadastro e autenticação de usuários;
- listagem de materiais em uma interface simples;
- inclusão manual de produtos e códigos;
- leitura de código de barras por entrada manual ou câmera do navegador;
- exclusão de materiais por leitura do código ou pela ação direta na tela;
- geração automática de código de barras para materiais que não possuem um valor informado.

## Funcionalidades

- Cadastro de conta com e-mail e senha;
- Login e logout com sessão autenticada;
- Proteção de rotas para usuários não autenticados;
- Listagem completa dos materiais cadastrados;
- Cadastro manual de produto com nome, código de barras e flag de itens com barras;
- Geração automática de código de barras para itens sem código cadastrado;
- Leitura de código de barras já existente para exclusão do material;
- Cadastro de material novo quando o código lido ainda não está no banco;
- Armazenamento seguro de senhas com hash via `Werkzeug`;
- Proteção CSRF em requisições POST.

## Como funciona a leitura de código de barras

A lógica atual do sistema considera o código de barras da seguinte forma:

- se o código já existe no banco, o material correspondente é removido do cadastro;
- se o código ainda não existe, o usuário é solicitado a informar o nome do material para cadastrar o novo item.

> Importante: a leitura de um código de barras já cadastrado exclui o material relacionado. Isso é uma regra do fluxo atual da aplicação e não um controle de estoque.

## Tecnologias

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Werkzeug (hash de senhas e utilitários do Flask)

## Estrutura do projeto

```text
iel-proj/
├── app.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   ├── login.html
│   ├── register.html
│   └── main.html
├── instance/
│   ├── materiais.sqlite3
│   └── secret_key
├── .gitignore
└── README.md
```

A pasta `instance` é criada automaticamente quando a aplicação inicia. Ela contém o banco de dados local e a chave de sessão usada pela aplicação.

## Requisitos

- Python 3.8 ou superior
- Navegador moderno
- Acesso à câmera do navegador, quando for usar a leitura pela webcam

## Execução local

### 1. Clone ou abra o projeto

Entre na pasta do repositório:

```powershell
cd C:\caminho\para\iel-proj
```

### 2. Crie um ambiente virtual

```powershell
python -m venv .venv
```

### 3. Ative o ambiente virtual

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

No CMD:

```cmd
.venv\Scripts\activate.bat
```

### 4. Instale as dependências

```powershell
python -m pip install Flask
```

### 5. Inicie a aplicação

```powershell
python app.py
```

### 6. Acesse a interface

Abra o navegador e acesse:

```text
http://127.0.0.1:5000
```

Na primeira vez, clique em "Cadastre-se" para criar uma conta com e-mail e senha de pelo menos 8 caracteres. Em seguida, faça login para acessar o sistema.

## Observações importantes

- O sistema foi desenvolvido para uso local.
- As credenciais são armazenadas com hash, não em texto puro.
- O banco de dados e a chave de sessão ficam na pasta `instance`.
- A leitura pela câmera depende das permissões do navegador e da disponibilidade da biblioteca JavaScript do scanner.
- A aplicação não implementa controle de estoque ou movimentação de materiais; ela funciona como catálogo e cadastro de itens.

## Dicas de uso

- Mantenha cópias de segurança do arquivo `instance/materiais.sqlite3` periodicamente.
- Se a câmera não funcionar, verifique permissões do navegador e acesso local via `localhost` ou `127.0.0.1`.
- Não compartilhe ou publique o arquivo `instance/secret_key`.

## Status do projeto

Projeto em desenvolvimento e em uso local, com foco em registrar materiais e simplificar a gestão operacional do catálogo.
