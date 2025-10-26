import streamlit as st
from views import View
from time import sleep

class AdminProfileUI:
    """Página de Perfil do Admin que permite ele ver e alterar seus dados."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Meu Perfil",
            page_icon="🪪"
        )
        
        st.header("🪪 Meus Dados")

        user_id: int = st.session_state["user_id"]
        admin_data = View.get_admin(user_id)

        new_name = st.text_input("Informe o Novo Nome", admin_data.name)
        new_email = st.text_input("Informe o Novo E-mail", admin_data.email, disabled=True)
        new_password = st.text_input("Informe a Nova Senha", admin_data.password, type="password")
        do_update = st.button("Atualizar")

        if do_update:
            try:
                View.update_admin(admin_data.id, new_name, new_email, new_password)
                st.success("Seus Dados foram Atualizados com Sucesso!", icon="✔")
            except Exception as e:
                st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
            sleep(2)
            st.rerun()
