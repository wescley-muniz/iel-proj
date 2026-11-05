# 📦 Sistema de Materiais

Aplicação web local desenvolvida em **Python e Flask** para cadastrar, consultar e gerenciar materiais por meio de uma interface simples e intuitiva. Os dados são armazenados localmente em um banco de dados **SQLite**, permitindo que os cadastros sejam mantidos entre as execuções do sistema.

## ✨ Funcionalidades

- 📋 **Listagem de materiais:** visualizar os materiais cadastrados.
- ➕ **Cadastro manual:** adicionar novos materiais informando seus dados.
- 📷 **Leitura de códigos de barras:** digitar o código ou utilizar a câmera do dispositivo.
- 🗑️ **Exclusão de materiais:** remover um cadastro pelo botão disponível na lista ou pela leitura do código de barras correspondente.
- 💾 **Armazenamento local:** salvar os dados no banco SQLite, localizado em `instance/materiais.sqlite3`.

## ⚠️ Como funciona a leitura de códigos de barras

O comportamento atual do sistema depende da existência do código no banco de dados:

- **Código já cadastrado:** o material correspondente é excluído.
- **Código ainda não cadastrado:** o sistema solicita o nome do material para realizar o cadastro.

> **Importante:** ler um código de barras já cadastrado exclui o material correspondente. Ao ler um código novo, o sistema solicita o nome do material para cadastrá-lo. O sistema mantém um cadastro de materiais, mas não controla as quantidades em estoque.

## 🛠️ Tecnologias utilizadas

- **Python** — linguagem de programação.
- **Flask** — framework para a aplicação web.
- **SQLite** — banco de dados local.
- **HTML, CSS e JavaScript** — estrutura, estilos e interatividade da interface.

## 🚀 Como executar localmente

### 1. Pré-requisitos

- Python instalado no computador.
- Um navegador atualizado.
- Conexão com a internet para carregar a biblioteca utilizada na leitura pela câmera.

### 2. Abra a pasta do projeto

Abra o terminal no diretório em que os arquivos do projeto estão localizados.

### 3. Crie um ambiente virtual

No Windows, execute:

```powershell
python -m venv .venv
```

### 4. Ative o ambiente virtual

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se estiver utilizando o Prompt de Comando (CMD), execute:

```cmd
.venv\Scripts\activate.bat
```

### 5. Instale o Flask

Com o ambiente virtual ativado, execute:

```powershell
python -m pip install Flask
```

### 6. Inicie a aplicação

Execute:

```powershell
python app.py
```

### 7. Acesse o sistema

Abra o navegador e entre no endereço:

**http://127.0.0.1:5000**

Para encerrar a aplicação, volte ao terminal e pressione `Ctrl + C`.

## 📷 Leitura de códigos de barras pela câmera

Para utilizar a câmera, permita o acesso quando o navegador solicitar.

- **Acesso local:** a câmera geralmente funciona em `localhost` ou `127.0.0.1`.
- **HTTPS:** em dispositivos acessando a aplicação por outro computador ou celular, normalmente é necessário utilizar uma conexão HTTPS segura.
- **Internet:** a biblioteca JavaScript utilizada pelo leitor precisa ser carregada. Portanto, a leitura pela câmera pode depender de uma conexão com a internet.

Caso a câmera não funcione, verifique as permissões do navegador, a conexão com a internet e a disponibilidade da biblioteca de leitura.

## 💾 Armazenamento dos dados

O banco de dados é armazenado localmente em:

```text
instance/
└── materiais.sqlite3
```

Os dados permanecem salvos nesse arquivo mesmo após o encerramento da aplicação. Para evitar a perda dos cadastros, faça cópias de segurança do banco de dados periodicamente.

## 🔒 Observações

- A aplicação foi projetada para execução local.
- Os dados são armazenados no computador em que o sistema é executado.
- A exclusão de um material remove seu cadastro do banco de dados.
- Antes de realizar alterações ou excluir registros, recomenda-se manter uma cópia de segurança do banco de dados.

---

python -m pip install -r requirements.txt

**Projeto em desenvolvimento.** Novas funcionalidades e melhorias poderão ser adicionadas conforme as necessidades de uso.

