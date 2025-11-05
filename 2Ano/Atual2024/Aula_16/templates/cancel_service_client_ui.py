import streamlit as st
from views import View
from datetime import datetime
from time import sleep

class CancelServiceClientUI:
    """Página do Cliente de Cancelar um Serviço."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Cancelar Serviço",
            page_icon="📅"
        )
        
        st.header("📅 Cancelar Serviço")

        user_id: int = st.session_state["user_id"]
        client_data = View.get_client(user_id)
        if client_data is None: return

        my_schedules = View.get_schedules_by_client(client_data.id)
        if len(my_schedules) <= 0:
            st.warning("Não há Horários Cadastrados.", icon="⚠")
            return
        
        schedule = st.selectbox("Selecione um Horário", my_schedules)
        
        schedule_description = View.get_service(schedule.service_id)
        schedule_description = schedule_description.description if schedule_description else None
        st.text_input("Serviço do Horário", schedule_description, disabled=True)
        schedule_professional = View.get_professional(schedule.professional_id)
        schedule_professional = schedule_professional.name if schedule_professional else None
        st.text_input("Profissional do Horário", schedule_professional, disabled=True)

        cancel_schedule = st.button("Cancelar Horário", type="primary")

        if cancel_schedule:
            try:
                View.update_schedule(schedule.id, schedule.date, False, None, None, View.get_professional(schedule.professional_id))
                View.append_notification(f"Horário {schedule.id} foi Cancelado por {client_data.name}.", datetime.now(), schedule.professional_id, View.get_users_type().PROFESSIONAL)
                st.success("Horário Cancelado com Sucesso!", icon="✔")
            except Exception as e:
                st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
            sleep(1)
            st.rerun()
