import streamlit as st
from views import View
from datetime import datetime
from time import sleep

class SetServiceClientUI:
    """Página do Cliente de Agendar um Serviço."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Agendar Serviço",
            page_icon="📅"
        )
        
        st.header("📅 Agendar Serviço")

        user_id: int = st.session_state["user_id"]
        client_data = View.get_client(user_id)
        if client_data is None: return

        profs_list = View.get_professional_list()
        services_list = View.get_service_list()

        if len(profs_list) <= 0:
            st.warning("Nenhum Profissional Cadastrado. Volte mais Tarde.", icon="⚠")
            return
        elif len(services_list) <= 0:
            st.warning("Nenhum Serviço Cadastrado. Volte mais Tarde.", icon="⚠")
            return

        prof = st.selectbox("Informe o Profissional", profs_list)
        schedule = st.selectbox("Informe o Horário", View.get_schedules_to_setting(prof.id))

        prof_services_list = [ serv for serv in services_list if serv.id in prof.services_id ] # Pega os serviços disponibilizados pelo Profissional selecionado
        if len(prof_services_list) == 0: # Se não houver serviço disponibilizado pelo Profissional, ele disponibilizará todos.
            prof_services_list = services_list
        service = st.selectbox("Informe o Serviço", prof_services_list)
        
        if len(View.get_schedules_to_setting(prof.id)) <= 0:
            st.warning("Nenhum Horário Disponível para esse Profissional.", icon="⚠")
            return
        
        set_schedule = st.button("Agendar")

        if set_schedule:
            try:
                View.update_schedule(schedule.id, schedule.date, schedule.confirmed, client_data, service, prof)
                View.append_notification(f"Horário {schedule.id} agendado por {client_data.name}.", datetime.now(), prof.id, View.get_users_type().PROFESSIONAL)
                st.success("Horário Agendado com Sucesso!", icon="✔")
            except Exception as e:
                st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
            sleep(1)
            st.rerun()
