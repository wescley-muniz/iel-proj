
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sistema de Materiais</title>
        </head>
        <body>
            <h1>Sistema de Controle de Materiais</h1>
            <p>Servidor funcionando corretamente!</p>
        </body>
        </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
