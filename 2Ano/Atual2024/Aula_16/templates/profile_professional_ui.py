import streamlit as st
from views import View
from time import sleep

class ProfessionalProfileUI:
    """Página de Perfil do Profissional que permite ele ver e alterar seus dados."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Meu Perfil",
            page_icon="🪪"
        )
        
        st.header("🪪 Meus Dados")

        user_id: int = st.session_state["user_id"]
        prof_data = View.get_professional(user_id)
        if prof_data is None: return

        st.image(prof_data.profile_photo, "Foto de Perfil Atual")
        new_profile_photo = st.file_uploader("Informe a Nova Foto de Perfil", ["png", "jpg", "jpeg"])
        actual_photo_if_any = st.checkbox("Deixar Foto Atual caso nenhuma Selecionada", True)
        if new_profile_photo: # Mostra a foto de perfil selecionada.
            st.image(new_profile_photo, "Foto de Perfil Selecionada")
        new_name = st.text_input("Informe o Novo Nome", prof_data.name)
        new_email = st.text_input("Informe o Novo E-mail", prof_data.email)
        new_speciality = st.text_input("Informe a Nova Especialidade", prof_data.speciality)
        new_council = st.text_input("Informe o Novo Conselho", prof_data.council)
        new_password = st.text_input("Informe a Nova Senha", prof_data.password, type="password")
        services_list = View.get_service_list()
        curr_services_list = [ serv for serv in services_list if serv.id in prof_data.services_id ]
        services = st.multiselect("Novos Serviços Disponibilizados (Nenhum para todos)", services_list, default=curr_services_list)
        do_update = st.button("Atualizar")

        if do_update:
            if new_profile_photo is None and actual_photo_if_any:
                new_profile_photo = prof_data.profile_photo
            elif new_profile_photo is not None:
                new_profile_photo = new_profile_photo.read()
            services = [ serv.id for serv in services ]
            
            try:
                View.update_professional(prof_data.id, new_name, new_email, new_speciality, new_council, new_password, services, new_profile_photo)
                st.success("Seus Dados foram Atualizados com Sucesso!", icon="✔")
            except Exception as e:
                st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
            sleep(2)
            st.rerun()
