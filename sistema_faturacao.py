from datetime import datetime

# ==========================================
# SISTEMA DE FATURACAO DE PRODUTOS ALIMENTARES
# ==========================================

clientes = []
fila_prioritaria = []
fila_normal = []
faturas = []

contador_faturas = 1
contador_chegada = 1


def formatar_kz(valor):
    valor_formatado = f"{valor:,.2f}"
    valor_formatado = valor_formatado.replace(",", "X")
    valor_formatado = valor_formatado.replace(".", ",")
    valor_formatado = valor_formatado.replace("X", ".")
    return valor_formatado + " Kz"


def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Erro: este campo nao pode ficar vazio.")


def ler_inteiro(mensagem, minimo=0):
    while True:
        try:
            valor = int(input(mensagem))
            if valor >= minimo:
                return valor
            print(f"Introduza um valor igual ou superior a {minimo}.")
        except ValueError:
            print("Erro: introduza um numero inteiro valido.")


def ler_valor(mensagem):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor > 0:
                return valor
            print("O valor deve ser superior a zero.")
        except ValueError:
            print("Introduza um valor monetario valido.")


def ler_sim_nao(mensagem):
    while True:
        resposta = input(mensagem + " (S/N): ").strip().upper()
        if resposta in ["S", "N"]:
            return resposta == "S"
        print("Resposta invalida. Introduza S ou N.")


def registar_compra():
    global contador_faturas, contador_chegada

    print("\n========== REGISTAR COMPRA ==========")
    nome = ler_texto("Nome do cliente: ")

    while True:
        genero = input("Genero (M/F): ").strip().upper()
        if genero in ["M", "F"]:
            break
        print("Introduza M para Masculino ou F para Feminino.")

    idade = ler_inteiro("Idade do cliente: ", 0)

    gravida = False
    if genero == "F":
        gravida = ler_sim_nao("A cliente esta gravida?")

    deficiencia = ler_sim_nao(
        "O cliente possui alguma deficiencia?"
    )

    valor_compras = ler_valor("Valor total das compras (Kz): ")

    # Bonus comercial: apenas para compras superiores a 100.000 Kz
    bonus = valor_compras * 0.10 if valor_compras > 100000 else 0
    valor_pagar = valor_compras - bonus

    # Prioridade no atendimento: independente do bonus comercial
    idoso = idade >= 60
    tem_prioridade = gravida or idoso or deficiencia
    categoria = "PRIORITARIO" if tem_prioridade else "NORMAL"

    cliente = {
        "nome": nome,
        "genero": genero,
        "idade": idade,
        "gravida": gravida,
        "deficiencia": deficiencia,
        "idoso": idoso,
        "valor_compras": valor_compras,
        "bonus": bonus,
        "valor_pagar": valor_pagar,
        "prioridade": categoria,
        "chegada": contador_chegada
    }

    clientes.append(cliente)

    if tem_prioridade:
        fila_prioritaria.append(cliente)
    else:
        fila_normal.append(cliente)

    fatura = {
        "numero": contador_faturas,
        "nome": nome,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "valor_compras": valor_compras,
        "bonus": bonus,
        "valor_pagar": valor_pagar
    }
    faturas.append(fatura)

    print("\n========== FATURA ==========")
    print("Numero da fatura:", contador_faturas)
    print("Cliente:", nome)
    print("Data:", fatura["data"])
    print("----------------------------")
    print("Valor das compras:", formatar_kz(valor_compras))
    print("Bonus de 10%:", formatar_kz(bonus))
    print("----------------------------")
    print("TOTAL A PAGAR:", formatar_kz(valor_pagar))
    print("----------------------------")
    print("Atendimento:", categoria)

    if idoso:
        print("Motivo: Pessoa idosa")
    if gravida:
        print("Motivo: Mulher gravida")
    if deficiencia:
        print("Motivo: Pessoa com deficiencia")

    print("============================")
    print("Compra registada com sucesso!")

    contador_faturas += 1
    contador_chegada += 1


def visualizar_fila():
    print("\n========== FILA DE ATENDIMENTO ==========")

    if not fila_prioritaria and not fila_normal:
        print("Nao existem clientes na fila.")
        return

    posicao = 1
    print("\n--- CLIENTES PRIORITARIOS ---")
    for cliente in fila_prioritaria:
        print(f"{posicao}. {cliente['nome']} - {cliente['prioridade']}")
        posicao += 1

    print("\n--- CLIENTES NORMAIS ---")
    for cliente in fila_normal:
        print(f"{posicao}. {cliente['nome']} - {cliente['prioridade']}")
        posicao += 1

    print("\nTotal de clientes na fila:",
          len(fila_prioritaria) + len(fila_normal))


def atender_cliente():
    print("\n========== ATENDIMENTO ==========")

    if fila_prioritaria:
        cliente = fila_prioritaria.pop(0)
    elif fila_normal:
        cliente = fila_normal.pop(0)
    else:
        print("Nao existem clientes para atender.")
        return

    print("Cliente chamado:", cliente["nome"])
    print("Categoria:", cliente["prioridade"])
    print("Valor a pagar:", formatar_kz(cliente["valor_pagar"]))
    print("Atendimento realizado com sucesso!")


def listar_clientes():
    print("\n========== CLIENTES REGISTADOS ==========")

    if not clientes:
        print("Ainda nao existem clientes registados.")
        return

    for numero, cliente in enumerate(clientes, start=1):
        print(f"\nCliente {numero}")
        print("Nome:", cliente["nome"])
        print("Genero:", cliente["genero"])
        print("Idade:", cliente["idade"])
        print("Valor das compras:", formatar_kz(cliente["valor_compras"]))
        print("Bonus:", formatar_kz(cliente["bonus"]))
        print("Valor a pagar:", formatar_kz(cliente["valor_pagar"]))
        print("Atendimento:", cliente["prioridade"])


def historico_faturas():
    print("\n========== HISTORICO DE FATURAS ==========")

    if not faturas:
        print("Nao existem faturas registadas.")
        return

    for fatura in faturas:
        print("\nFatura numero:", fatura["numero"])
        print("Cliente:", fatura["nome"])
        print("Data:", fatura["data"])
        print("Compras:", formatar_kz(fatura["valor_compras"]))
        print("Bonus:", formatar_kz(fatura["bonus"]))
        print("Total:", formatar_kz(fatura["valor_pagar"]))


def relatorio_geral():
    total_compras = sum(c["valor_compras"] for c in clientes)
    total_bonus = sum(c["bonus"] for c in clientes)
    total_receber = sum(c["valor_pagar"] for c in clientes)

    prioritarios = sum(1 for c in clientes if c["prioridade"] == "PRIORITARIO")
    normais = len(clientes) - prioritarios

    print("\n========== RELATORIO GERAL ==========")
    print("Total de clientes:", len(clientes))
    print("Total de faturas:", len(faturas))
    print("Clientes prioritarios:", prioritarios)
    print("Clientes normais:", normais)
    print("-------------------------------------")
    print("Total das compras:", formatar_kz(total_compras))
    print("Total de bonus:", formatar_kz(total_bonus))
    print("Total a receber:", formatar_kz(total_receber))
    print("=====================================")


def menu_principal():
    while True:
        print("\n========================================")
        print("     SISTEMA DE FATURACAO DA LOJA")
        print("       PRODUTOS ALIMENTARES")
        print("========================================")
        print("1 - Registar compra e emitir fatura")
        print("2 - Visualizar fila de atendimento")
        print("3 - Atender proximo cliente")
        print("4 - Listar clientes registados")
        print("5 - Consultar historico de faturas")
        print("6 - Consultar relatorio geral")
        print("0 - Sair do sistema")
        print("========================================")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            registar_compra()
        elif opcao == "2":
            visualizar_fila()
        elif opcao == "3":
            atender_cliente()
        elif opcao == "4":
            listar_clientes()
        elif opcao == "5":
            historico_faturas()
        elif opcao == "6":
            relatorio_geral()
        elif opcao == "0":
            print("\nObrigado por utilizar o sistema!")
            print("Sistema encerrado.")
            break
        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
