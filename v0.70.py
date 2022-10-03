from PySimpleGUI import PySimpleGUI as SG
import json

estoque = {}
usuarios = {}
usuario_atual = ""

try:
    with open("usuarios.json", "r") as user_file:
        usuarios = json.load(user_file)
except:
    pass
try:
    with open("estoque.json", "r") as stock_file:
        estoque = json.load(stock_file)
except:
    pass


print(usuarios)
print(estoque)
lista_estoque = [[produto, estoque[produto]["Preco"], estoque[produto]["Quantidade"]] for produto in estoque]
lista_so_nome = [produto for produto in estoque]
carrinho = []
# TELA DA FASE 00


def telaInicial():
    layout = [
        [SG.Text("Bem vindo")],
        [SG.Text("Email:", size=(8, 1)), SG.Input(key="-EMAIL-")],
        [SG.Text("Login:", size=(8, 1)), SG.Input(key="-SENHA-", password_char="*")],
        [SG.Button("Login", key="-LOGIN-"), SG.Button("Cadastrar", key="-CADASTRO-")],
    ]

    return SG.Window(
        "Mercado Zacarias",
        layout=layout,
        element_justification="c"
    )


# TELA FASE 01


def telaAdmin():
    layout_esquerda = [
        [SG.Table(values=lista_estoque, headings=["Produto", "Preço", "Quant"], auto_size_columns=True, num_rows=30,
                  justification="l",
                  enable_events=True, key="-TABLE-")]

    ]
    layout_direita = [
        [SG.Text("Cadastro")],
        [SG.Text("Produto:", size=(11, 1)), SG.Input(key="-PRODUTO-", enable_events=True)],
        [SG.Text("Quantidade:", size=(11, 1)), SG.Input(key="-QUANTIDADE-", enable_events=True)],
        [SG.Text("Preço:", size=(11, 1)), SG.Input(key="-PRECO-", enable_events=True)],
        [SG.Push(), SG.Button("CADASTRAR", key="-CADPRODUTO-"), SG.Button("REMOVER", key="-REMOVE-")],
        [SG.VPush()],
        [SG.HorizontalSeparator()],
        [SG.VPush()],
        [SG.Text("Produto:", size=(11, 1)), SG.Input(key="-ATTPRODUTO-", enable_events=True)],
        [SG.Text("Quantidade:", size=(11, 1)), SG.Input(key="-ATTQUANT-", enable_events=True)],
        [SG.Radio("ADICIONAR", key="-MAIS-", group_id="-CONTROLE-", enable_events=True, default=True),
         SG.Radio("REMOVER", key="-MENOS-",
                  group_id="-CONTROLE-",
                  enable_events=True),
         SG.Push(), SG.Button("CONFIRMAR", key="-CONFIRMAR-")]
    ]
    layout = [
        [SG.Column(layout_esquerda), SG.VerticalSeparator(), SG.Column(layout_direita)]
    ]
    return SG.Window("Estoque", layout=layout)


# TELA FASE 02


def telaCompra():
    layout_esquerda = [
        [SG.Table(values=lista_estoque, headings=["Produto", "Preço", "Quant"], auto_size_columns=True, num_rows=30,
                  justification="l",
                  enable_events=True, key="-TABLE-")],
        [SG.HorizontalSeparator()],
        [SG.Combo(values=lista_so_nome, key='-ATTPRODUTO-', enable_events=True,
                  size=(27, 6)), SG.Spin([number for number in range(1, 99)], initial_value=1,
                                         size=(5, 1), key='-SPIN-', enable_events=True), SG.Text("="),
         SG.Text(f"0,00", key="-VALOR_QUANTIDADE-")],
        [SG.Button('Adicionar ao carrinho', key='-CARRINHO-'), ]
        ]

    layout_direita = [
        [SG.Table(values=carrinho, headings=["Produto", "Quant", "Preço"], auto_size_columns=True, num_rows=30,
                  justification="l", key="-TABLECARRINHO-", bind_return_key=True)],
        [SG.HorizontalSeparator()],
        [SG.Text(f"Total = ", key="-TOTALCARRINHO-")],
        [SG.Push(), SG.Button("Finalizar compra", key="-FCOMPRA-")]
    ]
    # layout_instrução =[
    #     SG.Text(text=)
    # ]

    layout = [
        [SG.Column(layout_esquerda), SG.VerticalSeparator(), SG.Column(layout_direita)]
    ]

    return SG.Window("Compra", layout=layout)


def ChecarUser():
    global janela
    global log_in
    global fase
    global usuario_atual
    user = values["-EMAIL-"].lower()
    senha = values["-SENHA-"]

    if user in usuarios:
        if senha == (usuarios.get(user)).get("Senha"):
            log_in = True
            ChecarAdmin()
            usuario_atual = user
            print("passou Checa")

    if not log_in:
        SG.Popup(title="ERRO", custom_text="USUARIO OU SENHA INVÁLIDO")


def ChecarAdmin():
    global janela
    global fase
    if values["-EMAIL-"].lower() == "admin@mercadozacarias.com":
        if values["-SENHA-"] == "mercadoadmin":
            janela.close()
            janela = telaAdmin()
            janela.read()
            fase = 1
            print("passou admin")
    else:
        janela.close()
        janela = telaCompra()
        fase = 2


def RegistrarItem():
    global estoque
    global lista_estoque
    produto = values["-PRODUTO-"]
    preco = float(values["-PRECO-"])
    quantidade_atual = int(values["-QUANTIDADE-"])
    if produto in estoque:
        SG.Popup(title="ERRO", custom_text="PRODUTO JÁ CADASTRADO")
    else:
        SG.Popup(title='Sucesso', custom_text=f'O cadastro do produto {produto}'
                                              f' foi realizado com sucesso')
        estoque.setdefault(produto, {"Quantidade": quantidade_atual,
                                     "Preco": preco})
        lista_estoque.append([produto, preco, quantidade_atual])
        janela.find_element('-TABLE-').update(values=lista_estoque)
        janela.refresh()


def RegistrarCliente():
    global fase
    global janela
    user = values['-EMAIL-'].lower()
    senha = values['-SENHA-']
    if user not in usuarios:
        usuarios.update({user: {"Senha": senha, "Carrinho": []}})
        janela.close()
        janela = telaCompra()
        janela.read()
        fase = 2
    else:
        SG.Popup(title="Opa!", custom_text="Usuario já cadastrado")
    pass


def ControleDeEstoque():
    global estoque
    global lista_estoque
    global carrinho
    temp_carrinho = carrinho
    produto = values["-ATTPRODUTO-"]
    mercadoria = estoque[values["-ATTPRODUTO-"]]
    quant = mercadoria.get("Quantidade")
    index = [(i, prop.index(produto)) for i, prop in enumerate(lista_estoque) if produto in prop]

    try:
        quantidade = int(values["-ATTQUANT-"])
    except KeyError:
        pass

    index = index[0][0]

    if event == '-CONFIRMAR-':
        if values['-MENOS-']:
            if quant - quantidade > 0:
                mercadoria.update({"Quantidade": quant - quantidade})
                lista_estoque[index][2] = quant - quantidade
                print({produto: mercadoria})
            if quant - quantidade <= 0:
                mercadoria.update({"Quantidade": 0})
        elif values['-MAIS-']:
            mercadoria.update({"Quantidade": quant + quantidade})
            lista_estoque[index][2] = quant + quantidade
            print({produto: mercadoria})
    elif event == '-TABLECARRINHO-':
        index2 = values['-TABLECARRINHO-'][0]
        produto = temp_carrinho[index2][0]
        index = [(i, prop.index(produto)) for i, prop in enumerate(lista_estoque) if produto in prop]
        index = index[0][0]
        mercadoria = estoque[produto]
        quantidade = carrinho[index2][1]
        lista_estoque[index][2] = quant + quantidade
        mercadoria.update({"Quantidade": quant + quantidade})

    elif event == '-CARRINHO-':
        quantidade = int(values['-SPIN-'])
        mercadoria.update({"Quantidade": quant - quantidade})
        lista_estoque[index][2] = quant - quantidade


    else:
        return quant
    estoque.update({produto: mercadoria})
    print(estoque)
    janela.find_element('-TABLE-').update(values=lista_estoque)
    janela.refresh()


def RemoverProduto():
    global estoque
    global lista_estoque
    produto = values["-PRODUTO-"]
    index = [(i, prop.index(produto)) for i, prop in enumerate(lista_estoque) if produto in prop]
    lista_estoque.pop(index[0][0])
    estoque.pop(produto)
    janela.find_element('-TABLE-').update(values=lista_estoque)
    janela.refresh()


def AdicionarAoCarrinho():
    global carrinho
    global janela
    produto = values['-ATTPRODUTO-']
    valor_retirado = values['-SPIN-']
    temp = estoque.get(produto)
    preco = temp.get("Preco")
    preco_total = float(preco)*int(valor_retirado)
    if event == "-SPIN-" or '-ATTPRODUTO-':
        janela.find_element("-VALOR_QUANTIDADE-").update(f"{preco_total}")
        janela.refresh()

    if event == '-CARRINHO-':
        carrinho.append([produto, valor_retirado, preco_total])
        ControleDeEstoque()
        janela.find_element('-TABLECARRINHO-').update(values=carrinho)
        janela.refresh()


def ControleCarrinho():
    global carrinho
    global janela
    choice, _ = SG.Window('Continue?',
                          [[SG.T('Tem certeza que quer excluir o item selecionado?')], [SG.Yes(s=10), SG.No(s=10)]],
                          disable_close=True).read(close=True)
    if choice == "Yes":
        ControleDeEstoque()
        index_carrinho = values['-TABLECARRINHO-'][0]
        carrinho.pop(index_carrinho)
        janela.find_element('-TABLECARRINHO-').update(values=carrinho)
        janela.refresh()

    elif choice == "No":
        pass


def FinalizarCompra():
    global carrinho
    global lista_estoque
    global estoque
    global usuarios
    estoque = {produto[0]: {"Preco": produto[1], "Quantidade": produto[2]} for produto in lista_estoque}
    print(estoque)
    if event == '-FCOMPRA-':
        SG.Popup(custom_text="COMPRA FEITA COM SUCESSO, OBRIGADO PELA PREFERENCIA")
    SalvarArquivo()
    janela.close()


def SalvarArquivo():
    arquivo_usuario = json.dumps(usuarios)
    arquivo_estoque = json.dumps(estoque)

    file_1 = open("usuarios.json", "w")
    file_2 = open("estoque.json", "w")

    file_1.write(arquivo_usuario)
    file_2.write(arquivo_estoque)

    file_1.close()
    file_2.close()


janela = telaInicial()
fase = 0
log_in = False

while True:
    event, values = janela.read()
    if fase == 0:
        if event == '-LOGIN-':
            ChecarUser()
        if event == '-CADASTRO-':
            RegistrarCliente()

    if fase == 1:
        if event == '-CADPRODUTO-':
            RegistrarItem()
        if event == '-REMOVE-':
            if values['-PRODUTO-'] not in estoque:
                SG.Popup(title="Erro", custom_text="Produto não existe")
            else:
                RemoverProduto()
        if event == "-CONFIRMAR-":
            ControleDeEstoque()
        # Condicional para evitar que o usuário não coloque nada além do pedido nos campos errados
        if event == "-PRECO-" and values["-PRECO-"] and values["-PRECO-"][-1] not in '0123456789.':
            janela["-PRECO-"].update(values["-PRECO-"][:-1])

        if event == "-QUANTIDADE-" and values["-QUANTIDADE-"] and values["-QUANTIDADE-"][-1] not in '0123456789':
            janela["-QUANTIDADE-"].update(values["-QUANTIDADE-"][:-1])

        if event == "-ATTQUANT-" and values["-ATTQUANT-"] and values["-ATTQUANT-"][-1] not in '0123456789':
            janela["-ATTQUANT-"].update(values["-ATTQUANT-"][:-1])

    if fase == 2:
        if event == '-SPIN-':
            AdicionarAoCarrinho()
            janela.find_element("-SPIN-").update(values=[number for number in range(1, ControleDeEstoque() + 1)])
            janela.refresh()
        if event == '-ATTPRODUTO-':
            AdicionarAoCarrinho()
            janela.find_element("-SPIN-").update(values=[number for number in range(1, ControleDeEstoque() + 1)])
            janela.refresh()
        if event == "-CARRINHO-":
            AdicionarAoCarrinho()
            janela.refresh()
        if event == "-TABLECARRINHO-":
            ControleCarrinho()
        if event == "-FCOMPRA-":
            FinalizarCompra()

    if event is None:
        break

FinalizarCompra()

