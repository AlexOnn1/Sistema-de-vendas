import streamlit as st

lista_produtos = [
    {"nome": "Café", "valor": 17.50, "quantidade": 20, "descricao": "Um cafézinho bem bom", "id": "01", "imagem": "https://placehold.co/100x100"},
    {"nome": "Suco", "valor": 7.50, "quantidade": 10, "descricao": "Um suquinho bem bom", "id": "02", "imagem": "https://placehold.co/100x100"},
    {"nome": "Pão", "valor": 2.50, "quantidade": 245, "descricao": "Um pãozinho bem bom", "id": "03", "imagem": "https://placehold.co/100x100"},
    {"nome": "Leite", "valor": 20, "quantidade": 30, "descricao": "Um leitinho bem bom", "id": "04", "imagem": "https://placehold.co/100x100"}
]
def concluir_pagamento():
    st.session_state["carrinho"] = {}
    st.session_state["pagamento"] = False
    st.session_state["compra_sucesso"] = True

st.title("Produtos à venda")

# Inicializa variáveis de sessão
if "carrinho" not in st.session_state:
    st.session_state["carrinho"] = {}
if "pagamento" not in st.session_state:
    st.session_state["pagamento"] = False
if "compra_sucesso" not in st.session_state:
    st.session_state["compra_sucesso"] = False
if "processar_pagamento" not in st.session_state:
    st.session_state["processar_pagamento"] = False

# Exibe produtos e botões de adicionar/remover
for produto in lista_produtos:
    col1, col2 = st.columns([1.5, 1.5])
    with col1:
        st.write(f"**{produto['nome']}**")
        st.image(produto["imagem"])
        st.write(produto["descricao"])
        st.write(f"R$ {produto['valor']:.2f}")
        st.write("")
    with col2:
        key_input = f"input_{produto['id']}"
        qtd = st.number_input(
            "Qtd:", min_value=1, max_value=produto["quantidade"], value=1, step=1, key=key_input
        )
        if st.button("Adicionar ao carrinho", key=f"add_{produto['id']}"):
            carrinho = st.session_state["carrinho"]
            st.session_state["compra_sucesso"] = False
            qtd_no_carrinho = carrinho.get(produto['id'], {}).get('quantidade', 0)
            if qtd_no_carrinho + qtd > produto["quantidade"]:
                st.warning(f"Não é possível adicionar mais do que o estoque disponível ({produto['quantidade']}).")
            else:
                if produto['id'] in carrinho:
                    carrinho[produto['id']]['quantidade'] += qtd
                else:
                    carrinho[produto['id']] = {
                        "nome": produto["nome"],
                        "valor": produto["valor"],
                        "quantidade": qtd
                    }
                st.success(f"{qtd}x {produto['nome']} adicionado(s) ao carrinho!")
        if st.button("Remover do carrinho", key=f"remove_{produto['id']}"):
            st.session_state["compra_sucesso"] = False
            carrinho = st.session_state["carrinho"]
            if produto['id'] in carrinho:
                if carrinho[produto['id']]['quantidade'] <= qtd:
                    del carrinho[produto['id']]
                    st.success(f"{produto['nome']} removido do carrinho!")
                else:
                    carrinho[produto['id']]['quantidade'] -= qtd
                    st.success(f"{qtd}x {produto['nome']} removido(s) do carrinho!")
            else:
                st.warning(f"{produto['nome']} não está no carrinho.")

# Carrinho de compras na barra lateral
st.sidebar.title("Carrinho de Compras")
total = 0
if st.session_state["carrinho"]:
    for item in st.session_state["carrinho"].values():
        st.sidebar.write(f"{item['quantidade']}x {item['nome']} - R$ {item['valor']*item['quantidade']:.2f}")
        total += item['valor'] * item['quantidade']
    st.sidebar.write(f"**Total: R$ {total:.2f}**")

    # Botão de finalizar compra
    if not st.session_state["pagamento"]:
        if st.sidebar.button("Prosseguir para o pagamento"):
            st.session_state["pagamento"] = True

    # Card de finalização de compra
    if st.session_state["pagamento"]:
        st.sidebar.markdown("---")
        st.sidebar.success("Falta pouco! Selecione a forma de pagamento! 😁")
        opcoes_pagamento = [
            "À vista",
            "Parcelado em 2x",
            "Parcelado em 3x",
            "Parcelado em 4x",
            "Parcelado em 5x",
            "Parcelado em 6x",
            "Parcelado em 7x",
            "Parcelado em 8x"
        ]
        opcao = st.sidebar.selectbox("Forma de pagamento:", opcoes_pagamento)
        juros = 0
        parcelas = 1

        if opcao == "À vista":
            juros = 0
            parcelas = 1
        elif opcao == "Parcelado em 2x":
            juros = 0
            parcelas = 2
        elif opcao == "Parcelado em 3x":
            juros = 0.03
            parcelas = 3
        elif opcao == "Parcelado em 4x":
            juros = 0.05
            parcelas = 4
        elif opcao == "Parcelado em 5x":
            juros = 0.07
            parcelas = 5
        elif opcao == "Parcelado em 6x":
            juros = 0.10
            parcelas = 6
        elif opcao == "Parcelado em 7x":
            juros = 0.13
            parcelas = 7
        elif opcao == "Parcelado em 8x":
            juros = 0.16
            parcelas = 8

        total_com_juros = total * (1 + juros)
        st.sidebar.info(f"Total com juros: R$ {total_com_juros:.2f}")
        if parcelas > 1:
            st.sidebar.info(f"{parcelas}x de R$ {total_com_juros/parcelas:.2f}")

        st.sidebar.button("Concluir pagamento", on_click=concluir_pagamento)




else:
    st.sidebar.write("Carrinho vazio.")

if st.session_state.get("processar_pagamento", False):
    st.session_state["carrinho"] = {}
    st.session_state["pagamento"] = False
    st.session_state["compra_sucesso"] = True
    st.session_state["processar_pagamento"] = False
    st.experimental_rerun()

# Card de sucesso após o pagamento
if st.session_state.get("compra_sucesso", False):
    st.sidebar.markdown("---")
    st.sidebar.success("✅ Compra realizada com sucesso! Obrigado pela preferência. 🎉")