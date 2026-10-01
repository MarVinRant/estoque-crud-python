import pandas as pd
import streamlit as st

from db import (
    create_product,
    delete_product,
    initialize,
    list_products,
    search_products,
    update_price,
    update_stock,
)


st.set_page_config(page_title="Estoque CRUD", page_icon="📦")
initialize()
st.title("📦 Sistema de Estoque")
st.caption("Projeto acadêmico com Python, SQLite e operações CRUD")

with st.expander("Cadastrar produto", expanded=True):
    with st.form("new_product"):
        nome = st.text_input("Nome")
        categoria = st.text_input("Categoria")
        preco = st.number_input("Preço", min_value=0.0, step=0.01)
        estoque = st.number_input("Estoque", min_value=0, step=1)
        estoque_minimo = st.number_input("Estoque mínimo", min_value=0, value=5, step=1)
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if not nome.strip() or not categoria.strip():
                st.error("Nome e categoria são obrigatórios.")
            else:
                create_product(nome.strip(), categoria.strip(), preco, estoque, estoque_minimo)
                st.success("Produto cadastrado.")
                st.rerun()

search_term = st.text_input("Buscar por nome", placeholder="Digite parte do nome")
products = search_products(search_term) if search_term else list_products()
if products:
    data = pd.DataFrame([dict(row) for row in products])
    st.subheader("Produtos cadastrados")
    st.dataframe(data, width="stretch", hide_index=True)
    low_stock = data[data["estoque"] <= data["estoque_minimo"]]
    if not low_stock.empty:
        st.warning(f"{len(low_stock)} produto(s) atingiram o estoque mínimo.")

    selected_id = st.selectbox("Produto para alterar", data["id"].tolist())
    new_stock = st.number_input("Novo estoque", min_value=0, step=1)
    if st.button("Atualizar estoque"):
        update_stock(selected_id, new_stock)
        st.success("Estoque atualizado.")
        st.rerun()

    new_price = st.number_input("Novo preço", min_value=0.0, step=0.01)
    if st.button("Atualizar preço"):
        update_price(selected_id, new_price)
        st.success("Preço atualizado.")
        st.rerun()

    if st.button("Excluir produto selecionado"):
        delete_product(selected_id)
        st.success("Produto excluído.")
        st.rerun()
else:
    st.info("Nenhum produto cadastrado ainda.")

