materiais = [
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
    {"nome": "Ropi 10 ml", "tem_barras": False}
]

# Gerar identificadores internos
for numero, material in enumerate(materiais, start=1):
    material["codigo"] = f"MAT-{numero:04d}"


def listar_produtos():
    print("\n--- PRODUTOS CADASTRADOS ---")

    for produto in materiais:
        print(
            produto["codigo"],
            "|",
            produto["nome"],
            "| Já tem código de barras:",
            "Sim" if produto["tem_barras"] else "Não"
        )

    print("Total:", len(materiais))


def adicionar_produto():
    nome = input("Nome do produto: ").strip()

    if not nome:
        print("O nome não pode ficar vazio.")
        return

    for produto in materiais:
        if produto["nome"].lower() == nome.lower():
            print("Esse produto já está cadastrado.")
            return

    codigo = f"MAT-{len(materiais) + 1:04d}"

    tem_barras = input(
        "Já possui código de barras? (s/n): "
    ).strip().lower() == "s"

    codigo_barras = ""

    if tem_barras:
        codigo_barras = input(
            "Digite o código de barras original: "
        ).strip()

    materiais.append({
        "codigo": codigo,
        "nome": nome,
        "tem_barras": tem_barras,
        "codigo_barras": codigo_barras
    })

    print("Produto cadastrado!")
    print("Código interno:", codigo)


while True:
    print("\n=== SISTEMA DE MATERIAIS ===")
    print("1 - Listar produtos")
    print("2 - Adicionar produto")
    print("0 - Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        listar_produtos()

    elif opcao == "2":
        adicionar_produto()

    elif opcao == "0":
        print("Sistema encerrado.")
        break

    else:
        print("Opção inválida.")
