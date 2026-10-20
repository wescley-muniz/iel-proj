import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "troque-esta-chave"  # necessária para usar flash()
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


def inicializar_banco():
    os.makedirs(app.instance_path, exist_ok=True)
    connection = conectar_banco()
    try:
        with connection:
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


@app.route("/")
def inicio():
    materiais = listar_materiais()
    return render_template("main.html", materiais=materiais)


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
            codigo = f"MAT-{cursor.lastrowid:04d}"
    except sqlite3.IntegrityError:
        flash("Esse produto já está cadastrado.")
        return redirect(url_for("inicio"))
    finally:
        connection.close()

    flash(f"Produto cadastrado! Código interno: {codigo}")
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