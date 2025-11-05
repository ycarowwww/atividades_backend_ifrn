import streamlit as st
from views import View
from datetime import datetime
from time import sleep

class CancelScheduleProfessionalUI:
    """Página do Profissional de Cancelar um Horário."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Cancelar Agenda",
            page_icon="📅"
        )
        
        st.header("📅 Cancelar/Excluir Agenda")

        user_id: int = st.session_state["user_id"]
        prof_data = View.get_professional(user_id)
        if prof_data is None: return

        my_schedules = View.get_schedules_by_professional(prof_data.id)
        if len(my_schedules) <= 0:
            st.warning("Não há Horários Cadastrados.", icon="⚠")
            return
        
        schedule = st.selectbox("Selecione um Horário", my_schedules)
        
        schedule_description = View.get_service(schedule.service_id)
        schedule_description = schedule_description.description if schedule_description else None
        st.text_input("Serviço do Horário", schedule_description, disabled=True)
        schedule_client = View.get_client(schedule.client_id)
        schedule_client = schedule_client.name if schedule_client else None
        st.text_input("Cliente do Horário", schedule_client, disabled=True)
        msg_reason = "Não Especificado"
        if schedule_client:
            msg_reason = st.text_input("Motivo do Cancelamento")
            msg_reason = msg_reason if msg_reason != "" else "Não Especificado"

        cancel_schedule = st.button("Cancelar Horário", type="primary")

        if cancel_schedule:
            try:
                if schedule_client:
                    View.update_schedule(schedule.id, schedule.date, False, None, None, prof_data)
                View.remove_schedule(schedule.id)
                View.append_notification(f"Horário {schedule.id} foi Cancelado e Excluído por {prof_data.name} devido: {msg_reason}.", datetime.now(), schedule.client_id, View.get_users_type().CLIENT)
                st.success("Horário Cancelado e Excluído com Sucesso!", icon="✔")
            except Exception as e:
                st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
            sleep(1)
            st.rerun()
