import hmac
import os
import re
import secrets
import sqlite3

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
os.makedirs(app.instance_path, exist_ok=True)
secret_key_path = os.path.join(app.instance_path, "secret_key")
try:
    with open(secret_key_path, "x", encoding="utf-8") as secret_key_file:
        secret_key_file.write(secrets.token_hex(32))
except FileExistsError:
    pass
with open(secret_key_path, encoding="utf-8") as secret_key_file:
    app.secret_key = secret_key_file.read()
app.config["DATABASE"] = os.path.join(app.instance_path, "materiais.sqlite3")

materiais_iniciais = [
    {"nome": "Gaze", "tem_barras": True},
    {"nome": "Compressa pequena", "tem_barras": True},
    {"nome": "Compressa grande", "tem_barras": True},
    {"nome": "Fraldas", "tem_barras": False},
    {"nome": "Agulha de 3 ml", "tem_barras": False},
    {"nome": "Agulha de 5 ml", "tem_barras": False},
    {"nome": "Agulha de 10 ml", "tem_barras": False},
    {"nome": "Agulha de 20 ml", "tem_barras": False},
    {"nome": "IV3000", "tem_barras": True},
    {"nome": "Equipo macro", "tem_barras": True},
    {"nome": "Sonda Foley 7.5", "tem_barras": True},
    {"nome": "Sonda Foley 7.0", "tem_barras": True},
    {"nome": "Propofol", "tem_barras": False},
    {"nome": "Beriplex", "tem_barras": False},
    {"nome": "Dipirona", "tem_barras": False},
    {"nome": "Aramin", "tem_barras": False},
    {"nome": "Cloridrato de dexametasona", "tem_barras": False},
    {"nome": "Ultiva", "tem_barras": False},
    {"nome": "Fasten", "tem_barras": False},
    {"nome": "Dimorf 10 ml", "tem_barras": False},
    {"nome": "Ondansetrona", "tem_barras": False},
    {"nome": "Transamim", "tem_barras": False},
    {"nome": "Ropi 10 ml", "tem_barras": False},
]

def conectar_banco():
    connection = sqlite3.connect(app.config["DATABASE"])
    connection.row_factory = sqlite3.Row
    return connection

def gerar_codigo_barras(connection, material_id):
    primeiro_numero = material_id
    ultimo_numero = 100_000_000_000

    for numero in range(primeiro_numero, ultimo_numero):
        base = f"2{numero:011d}"
        soma = sum(int(digito) for digito in base[::2])
        soma += 3 * sum(int(digito) for digito in base[1::2])
        digito_verificador = (-soma) % 10
        codigo_barras = f"{base}{digito_verificador}"

        existente = connection.execute(
            "SELECT 1 FROM materiais WHERE codigo_barras = ?",
            (codigo_barras,),
        ).fetchone()
        if existente is None:
            return codigo_barras

    raise RuntimeError("Não foi possível gerar um código de barras exclusivo.")

def inicializar_banco():
    os.makedirs(app.instance_path, exist_ok=True)
    connection = conectar_banco()
    try:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    senha_hash TEXT NOT NULL
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS materiais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    tem_barras INTEGER NOT NULL,
                    codigo_barras TEXT NOT NULL DEFAULT ''
                )
            """)

            quantidade = connection.execute(
                "SELECT COUNT(*) FROM materiais"
            ).fetchone()[0]
            if quantidade == 0:
                connection.executemany(
                    """
                    INSERT INTO materiais (nome, tem_barras, codigo_barras)
                    VALUES (?, ?, '')
                    """,
                    [
                        (material["nome"], material["tem_barras"])
                        for material in materiais_iniciais
                    ],
                )

            materiais_sem_codigo = connection.execute(
                """
                SELECT id FROM materiais
                WHERE TRIM(COALESCE(codigo_barras, '')) = ''
                ORDER BY id
                """
            ).fetchall()
            for material in materiais_sem_codigo:
                codigo_barras = gerar_codigo_barras(connection, material["id"])
                connection.execute(
                    """
                    UPDATE materiais
                    SET codigo_barras = ?, tem_barras = 1
                    WHERE id = ?
                    """,
                    (codigo_barras, material["id"]),
                )
    finally:
        connection.close()

def listar_materiais():
    connection = conectar_banco()
    try:
        registros = connection.execute(
            "SELECT id, nome, tem_barras, codigo_barras FROM materiais ORDER BY id"
        ).fetchall()
        return [
            {
                "id": registro["id"],
                "codigo": f"MAT-{registro['id']:04d}",
                "nome": registro["nome"],
                "tem_barras": bool(registro["tem_barras"]),
                "codigo_barras": registro["codigo_barras"],
            }
            for registro in registros
        ]
    finally:
        connection.close()


inicializar_banco()

def csrf_token():
    token = session.get("_csrf_token")
    if token is None:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


@app.context_processor
def disponibilizar_csrf_token():
    return {"csrf_token": csrf_token}


@app.before_request
def proteger_rotas():
    if request.method == "POST":
        token = session.get("_csrf_token", "")
        token_enviado = request.form.get("_csrf_token", "")
        if not token or not hmac.compare_digest(token, token_enviado):
            return "Token de segurança inválido. Atualize a página e tente novamente.", 400

    if request.endpoint in {"login", "cadastro", "static"} or request.endpoint is None:
        return None

    if "usuario_id" not in session:
        flash("Entre na sua conta para acessar o sistema.")
        return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario_id" in session:
        return redirect(url_for("inicio"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("password", "")
        connection = conectar_banco()
        try:
            usuario = connection.execute(
                "SELECT id, senha_hash FROM usuarios WHERE email = ?",
                (email,),
            ).fetchone()
        finally:
            connection.close()

        if usuario is None or not check_password_hash(usuario["senha_hash"], senha):
            flash("E-mail ou senha incorretos.")
            return redirect(url_for("login"))

        session.clear()
        session["usuario_id"] = usuario["id"]
        return redirect(url_for("inicio"))

    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if "usuario_id" in session:
        return redirect(url_for("inicio"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("password", "")
        confirmar_senha = request.form.get("confirm_password", "")

        if (
            len(email) > 254
            or re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is None
        ):
            flash("Informe um e-mail válido.")
            return redirect(url_for("cadastro"))
        if len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres.")
            return redirect(url_for("cadastro"))
        if senha != confirmar_senha:
            flash("As senhas não conferem.")
            return redirect(url_for("cadastro"))

        connection = conectar_banco()
        try:
            with connection:
                connection.execute(
                    "INSERT INTO usuarios (email, senha_hash) VALUES (?, ?)",
                    (email, generate_password_hash(senha)),
                )
        except sqlite3.IntegrityError:
            flash("Já existe uma conta com esse e-mail.")
            return redirect(url_for("cadastro"))
        finally:
            connection.close()

        flash("Conta criada. Entre com seu e-mail e sua senha.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/sair", methods=["POST"])
def logout():
    session.clear()
    flash("Você saiu da sua conta.")
    return redirect(url_for("login"))


@app.route("/materiais")
def inicio():
    materiais = listar_materiais()
    return render_template("main.html", materiais=materiais)


@app.route("/ler-codigo", methods=["POST"])
def ler_codigo_barras():
    codigo_barras = request.form.get("codigo_barras", "").strip()
    if not codigo_barras:
        flash("Leia um código de barras antes de continuar.")
        return redirect(url_for("inicio"))

    connection = conectar_banco()
    try:
        with connection:
            material = connection.execute(
                "SELECT id, nome FROM materiais WHERE codigo_barras = ?",
                (codigo_barras,),
            ).fetchone()

            if material is not None:
                connection.execute(
                    "DELETE FROM materiais WHERE id = ?",
                    (material["id"],),
                )
    finally:
        connection.close()

    if material is not None:
        flash(f"{material['nome']} foi excluído do cadastro pela leitura do código.")
        return redirect(url_for("inicio"))

    flash("Código não cadastrado. Informe o nome para cadastrar esse material.")
    return render_template(
        "main.html",
        materiais=listar_materiais(),
        codigo_pendente=codigo_barras,
    )

@app.route("/adicionar-lido", methods=["POST"])
def adicionar_material_lido():
    nome = request.form.get("nome", "").strip()
    codigo_barras = request.form.get("codigo_barras", "").strip()

    if not nome or not codigo_barras:
        flash("Informe o nome do material e leia novamente o código.")
        return redirect(url_for("inicio"))

    connection = conectar_banco()
    try:
        with connection:
            existente = connection.execute(
                """
                SELECT nome FROM materiais
                WHERE codigo_barras = ? OR nome = ? COLLATE NOCASE
                """,
                (codigo_barras, nome),
            ).fetchone()
            if existente is not None:
                if existente["nome"].lower() == nome.lower():
                    flash("Esse material já está cadastrado.")
                else:
                    flash("Esse código de barras já está associado a outro material.")
                return redirect(url_for("inicio"))

            connection.execute(
                """
                INSERT INTO materiais (nome, tem_barras, codigo_barras)
                VALUES (?, 1, ?)
                """,
                (nome, codigo_barras),
            )
    except sqlite3.IntegrityError:
        flash("Não foi possível cadastrar: o material já existe.")
        return redirect(url_for("inicio"))
    finally:
        connection.close()

    flash(f"{nome} cadastrado com o código de barras {codigo_barras}.")
    return redirect(url_for("inicio"))

@app.route("/adicionar", methods=["POST"])
def adicionar_produto():
    nome = request.form.get("nome", "").strip()
    tem_barras = request.form.get("tem_barras") == "on"
    codigo_barras = request.form.get("codigo_barras", "").strip()

    if not nome:
        flash("O nome não pode ficar vazio.")
        return redirect(url_for("inicio"))

    connection = conectar_banco()
    try:
        nomes_existentes = connection.execute(
            "SELECT nome FROM materiais"
        ).fetchall()
        if any(
            registro["nome"].lower() == nome.lower()
            for registro in nomes_existentes
        ):
            flash("Esse produto já está cadastrado.")
            return redirect(url_for("inicio"))

        if codigo_barras:
            codigo_existente = connection.execute(
                "SELECT 1 FROM materiais WHERE codigo_barras = ?",
                (codigo_barras,),
            ).fetchone()
            if codigo_existente is not None:
                flash("Esse código de barras já está cadastrado.")
                return redirect(url_for("inicio"))

        with connection:
            cursor = connection.execute(
                """
                INSERT INTO materiais (nome, tem_barras, codigo_barras)
                VALUES (?, ?, ?)
                """,
                (
                    nome,
                    tem_barras,
                    codigo_barras if tem_barras else "",
                ),
            )
            material_id = cursor.lastrowid
            if not codigo_barras or not tem_barras:
                codigo_barras = gerar_codigo_barras(connection, material_id)
                connection.execute(
                    """
                    UPDATE materiais
                    SET codigo_barras = ?, tem_barras = 1
                    WHERE id = ?
                    """,
                    (codigo_barras, material_id),
                )
            codigo = f"MAT-{material_id:04d}"
    except sqlite3.IntegrityError:
        flash("Esse produto já está cadastrado.")
        return redirect(url_for("inicio"))
    finally:
        connection.close()

    flash(
        f"Produto cadastrado! Código interno: {codigo}. "
        f"Código de barras: {codigo_barras}"
    )
    return redirect(url_for("inicio"))

@app.route("/excluir/<int:material_id>", methods=["POST"])
def excluir_material(material_id):
    connection = conectar_banco()
    try:
        with connection:
            cursor = connection.execute(
                "DELETE FROM materiais WHERE id = ?",
                (material_id,),
            )
            excluido = cursor.rowcount > 0
    finally:
        connection.close()

    if excluido:
        flash("Material excluído.")
    else:
        flash("Esse material não foi encontrado.")
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)