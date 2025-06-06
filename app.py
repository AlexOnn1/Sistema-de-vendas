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

for produto in lista_produtos:
    col1, col2 = st.columns([1.5, 1.5])
    with col1:
        st.write(f"**{produto['nome']}**")
        st.image(produto["imagem"])     
        
        st.write(produto["descricao"])
        st.write(f"R$ {produto['valor']:.2f}")
        st.write("")
    # with col10:
    #     st.image(produto["imagem"])    
    with col2:
        key_input = f"input_{produto['id']}"
        qtd = st.number_input(
            "Qtd:", min_value=1, max_value=produto["quantidade"], value=1, step=1, key=key_input
        )
        if st.button("Adicionar ao carrinho", key=f"add_{produto['id']}"):
            if produto['id'] in st.session_state["carrinho"]:
                st.session_state["carrinho"][produto['id']]['quantidade'] += qtd
            else:
                st.session_state["carrinho"][produto['id']] = {
                    "nome": produto["nome"],
                    "valor": produto["valor"],
                    "quantidade": qtd
                }
            st.success(f"{qtd}x {produto['nome']} adicionado(s) ao carrinho!")
        if st.button("Remover do carrinho", key=f"remove_{produto['id']}"):
            if produto['id'] in st.session_state["carrinho"]:
                st.session_state["carrinho"][produto['id']]['quantidade'] -= qtd
            else:
                st.session_state["carrinho"][produto['id']] = {
                    "nome": produto["nome"],
                    "valor": produto["valor"],
                    "quantidade": qtd
                }
            st.success(f"{qtd}x {produto['nome']} Removido(s) ao carrinho!")        

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