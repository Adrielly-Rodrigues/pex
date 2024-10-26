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

# Página de Administração (CRUD de Usuários)
def admin_users_page():
    
    users = load_users()  # Carregar usuários no início

    # Colunas para título e botão
    col1, col2 = st.columns([5, 1])
    col1.title("Administração de Usuários")
    if col2.button("➕", key="add_user"):
        st.session_state.show_add_user = not st.session_state.get('show_add_user', False)

    # Seção para adicionar novo usuário
    if st.session_state.get('show_add_user', False):
        st.subheader("Adicionar novo usuário")
        
        new_username = st.text_input("Nome do usuário", key="new_username")
        col1, col2, col3 = st.columns(3)
        new_password = col1.text_input("Senha", type="password", key="new_password")
        new_idade = col2.number_input("Idade", min_value=0, key="new_idade")
        new_role = col3.selectbox("Role", ["admin", "common"], key="new_role")

        if st.button("Criar Usuário"):
            if new_username not in users:
                new_id = max([details['id'] for details in users.values()]) + 1 if users else 1
                users[new_username] = {
                    "id": new_id,
                    "nome": new_username,
                    "email": "",
                    "senha": new_password,
                    "idade": new_idade,
                    "role": new_role
                }
                save_users(users)
                st.success(f"Usuário {new_username} criado com sucesso!")
            else:
                st.error("Usuário já existe!")

    # Cabeçalho da tabela
    st.write("### Usuários cadastrados:")
    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
    col1.write("ID")
    col2.write("Nome")
    col3.write("Cargo")
    col4.write("Editar")
    col5.write("Deletar")
    st.write("---")

    # Tabela com Usuários
    for username, details in users.items():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
        col1.write(details["id"])
        col2.write(details["nome"])
        col3.write(details["role"])  # Mostra o nome do cargo
        editar_coluna = col4.button(f"✏️", key=f"edit_{username}")
        deletar_coluna = col5.button(f"🗑️", key=f"delete_{username}")

        if editar_coluna:
            st.session_state.editing_user = username

        if deletar_coluna:
            if st.confirm(f"Você tem certeza que deseja deletar o usuário {username}?"):
                del users[username]
                save_users(users)
                st.success(f"Usuário {username} deletado com sucesso!")
                st.session_state.refresh_data = True  # Sinaliza para atualizar os dados

    # Formulário de edição
    if 'editing_user' in st.session_state:
        editing_user = st.session_state.editing_user
        user_details = users[editing_user]

        st.write(f"### Editando usuário: {editing_user}")

        # Primeira linha: Nome e Email
        col1, col2 = st.columns(2)
        new_name = col1.text_input("Nome do usuário", value=user_details["nome"], key="edit_name")
        new_email = col2.text_input("Email", value=user_details["email"], key="edit_email")

        # Segunda linha: Senha, Idade e Role
        col3, col4, col5 = st.columns(3)
        new_password = col3.text_input("Senha", type="password", key="edit_password")
        new_age = col4.number_input("Idade", min_value=0, value=user_details["idade"], key="edit_age")
        new_role = col5.selectbox("Role", ["admin", "common"], index=0 if user_details["role"] == "admin" else 1, key="edit_role")

        # Atualizar usuário
        if st.button("Salvar alterações"):
            users[editing_user]["nome"] = new_name
            users[editing_user]["email"] = new_email
            users[editing_user]["senha"] = new_password  # Atualizar a senha
            users[editing_user]["idade"] = new_age
            users[editing_user]["role"] = new_role  # Atualizar o cargo
            save_users(users)
            st.success(f"Usuário {editing_user} atualizado com sucesso!")
            del st.session_state.editing_user  # Limpar o estado de edição
