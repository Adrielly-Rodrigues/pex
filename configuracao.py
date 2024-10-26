import streamlit as st
import json

# Função para carregar dados de usuários de um arquivo JSON
def load_users():
    with open('users.json', 'r') as f:
        users = json.load(f)
    return users

# Função para salvar usuários de volta no arquivo JSON
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Página de Configuração do Usuário
def config_page():
    if st.session_state.logged_in:  # Verifica se o usuário está logado
        st.title("Configurações")
        users = load_users()
        user = users[st.session_state.username]

        # Editar informações do usuário
        nome = st.text_input("Nome", value=user['nome'])
        email = st.text_input("Email", value=user['email'])
        senha = st.text_input("Senha", value=user['senha'], type="password")
        idade = st.number_input("Idade", value=user['idade'], min_value=0)

        if st.button("Alterar"):
            users[st.session_state.username] = {
                "id": user['id'],
                "nome": nome,
                "email": email,
                "senha": senha,
                "idade": idade,
                "role": user['role']
            }
            save_users(users)
            st.success("Dados atualizados com sucesso!")
    else:
        st.warning("Você precisa estar logado para acessar esta página.")
