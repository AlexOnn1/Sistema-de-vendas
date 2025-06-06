import streamlit as st

lista_produtos = [
    {"nome": "Café", "valor": 17.50, "quantidade": 20, "descricao": "Um cafézinho bem bom", "id": "01", "imagem": "https://placehold.co/100x100"},
    {"nome": "Suco", "valor": 7.50, "quantidade": 10, "descricao": "Um suquinho bem bom", "id": "02", "imagem": "https://placehold.co/100x100"},
    {"nome": "Pão", "valor": 2.50, "quantidade": 245, "descricao": "Um pãozinho bem bom", "id": "03", "imagem": "https://placehold.co/100x100"},
    {"nome": "Leite", "valor": 20, "quantidade": 30, "descricao": "Um leitinho bem bom", "id": "04", "imagem": "https://placehold.co/100x100"}
]

st.title("Produtos à venda")

# Inicializa o carrinho na sessão
if "carrinho" not in st.session_state:
    st.session_state["carrinho"] = {}

#função de validação no carrinho
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
else:
    st.sidebar.write("Carrinho vazio.")