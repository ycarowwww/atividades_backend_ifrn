import streamlit as st
from views import View
from time import sleep

class ClientProfileUI:
    """Página de Perfil do Cliente que permite ele ver e alterar seus dados."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Meu Perfil",
            page_icon="🪪"
        )
        
        st.header("🪪 Meus Dados")

        user_id: int = st.session_state["user_id"]
        client_data = View.get_client(user_id)
        if client_data is None: return

        st.image(client_data.profile_photo, "Foto de Perfil Atual")
        new_profile_photo = st.file_uploader("Informe a Nova Foto de Perfil", ["png", "jpg", "jpeg"])
        actual_photo_if_any = st.checkbox("Deixar Foto Atual caso nenhuma Selecionada", True)
        if new_profile_photo: # Mostra a foto de perfil selecionada.
            st.image(new_profile_photo, "Foto de Perfil Selecionada")
        new_name = st.text_input("Informe o Novo Nome", client_data.name)
        new_email = st.text_input("Informe o Novo E-mail", client_data.email)
        new_phone = st.text_input("Informe o Novo Telefone", client_data.phone)
        new_password = st.text_input("Informe a Nova Senha", client_data.password, type="password")
        do_update = st.button("Atualizar")

        if do_update:
            if new_profile_photo is None and actual_photo_if_any:
                new_profile_photo = client_data.profile_photo
            elif new_profile_photo is not None:
                new_profile_photo = new_profile_photo.read()
            
            try:
                View.update_client(client_data.id, new_name, new_email, new_phone, new_password, new_profile_photo)
                st.success("Seus Dados foram Atualizados com Sucesso!", icon="✔")
            except Exception as e:
                st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
            sleep(2)
            st.rerun()
