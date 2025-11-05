import pandas as pd
import streamlit as st
from time import sleep
from views import View

class KeepProfessionalUI:
    """Página do Admin para o Gerenciamento dos Profissionais."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Cadastro de Profissionais",
            page_icon="👨‍✈️"
        )
        
        st.header("👨‍✈️ Cadastro de Profissionais")

        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Deletar"])

        with tab1: KeepProfessionalUI.list_professionals()
        with tab2: KeepProfessionalUI.insert_professional()
        with tab3: KeepProfessionalUI.update_professional()
        with tab4: KeepProfessionalUI.remove_professional()
    
    @staticmethod
    def list_professionals() -> None:
        professionals = View.get_professional_list()
        professionals_data = [ [ prof.id, prof.name, prof.email, prof.speciality, prof.council, prof.password ] for prof in professionals ]
        
        data = pd.DataFrame(
            professionals_data,
            columns=["ID", "Nome", "E-mail", "Especialidade", "Conselho", "Senha"]
        )

        st.table(data)

    @staticmethod
    def insert_professional() -> None:
        profile_photo = st.file_uploader("Insira a Foto de Perfil", ["png", "jpg", "jpeg"])
        if profile_photo: 
            st.image(profile_photo, "Foto de Perfil Selecionada")
        name = st.text_input("Insira o Nome")
        email = st.text_input("Insira o E-mail")
        speciality = st.text_input("Insira a Especialidade")
        council = st.text_input("Insira o Conselho")
        password = st.text_input("Insira a Senha", type="password")
        services_list = View.get_service_list()
        services = st.multiselect("Serviços Disponibilizados (Nenhum para todos)", services_list)

        do_insert = st.button("Inserir Profissional")

        if do_insert:
            profile_photo = profile_photo if profile_photo is None else profile_photo.read()
            services = [ serv.id for serv in services ]

            try:
                View.append_professional(name, email, speciality, council, password, services, profile_photo)
                st.success("Profissional Inserido com Sucesso!", icon="✔")
            except Exception as e:
                st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
            sleep(2)
            st.rerun()

    @staticmethod
    def update_professional() -> None:
        professionals = View.get_professional_list()

        if len(professionals) <= 0:
            st.warning("Nenhum Profissional Registrado.", icon="⚠")
        else:
            professional_selected = st.selectbox(
                "Selecione um Profissional para Atualizar",
                professionals
            )
            st.image(professional_selected.profile_photo, "Foto de Perfil Atual")
            new_profile_photo = st.file_uploader("Insira a Nova Foto de Perfil", ["png", "jpg", "jpeg"])
            actual_photo_if_any = st.checkbox("Deixar Foto Atual caso nenhuma Selecionada", True)
            if new_profile_photo: st.image(new_profile_photo, "Foto de Perfil Selecionada")
            new_name = st.text_input("Insira o Novo Nome", professional_selected.name)
            new_email = st.text_input("Insira o Novo E-mail", professional_selected.email)
            new_speciality = st.text_input("Insira a Nova Especialidade", professional_selected.speciality)
            new_council = st.text_input("Insira o Novo Conselho", professional_selected.council)
            new_password = st.text_input("Insira a Nova Senha", professional_selected.password, type="password")
            services_list = View.get_service_list()
            curr_services_list = [ serv for serv in services_list if serv.id in professional_selected.services_id ]
            services = st.multiselect("Novos Serviços Disponibilizados (Nenhum para todos)", services_list, default=curr_services_list)
            do_update = st.button("Atualizar Profissional")

            if do_update:
                if new_profile_photo is None and actual_photo_if_any:
                    new_profile_photo = professional_selected.profile_photo
                elif new_profile_photo is not None:
                    new_profile_photo = new_profile_photo.read()
                services = [ serv.id for serv in services ]
                
                try:
                    View.update_professional(professional_selected.id, new_name, new_email, new_speciality, new_council, new_password, services, new_profile_photo)
                    st.success("Profissional Atualizado com Sucesso!", icon="✔")
                except Exception as e:
                    st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
                sleep(2)
                st.rerun()

    @staticmethod
    def remove_professional() -> None:
        professionals = View.get_professional_list()

        if len(professionals) <= 0:
            st.warning("Nenhum Profissional Registrado.", icon="⚠")
        else:
            professional_selected = st.selectbox(
                "Selecione um Profissional para Deletar",
                professionals
            )
            do_removal = st.button("Deletar Profissional", type="primary")

            if do_removal:
                try:
                    View.remove_professional(professional_selected.id)
                    st.success("Profissional Deletado com Sucesso!", icon="✔")
                except Exception as e:
                    st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
                sleep(2)
                st.rerun()
