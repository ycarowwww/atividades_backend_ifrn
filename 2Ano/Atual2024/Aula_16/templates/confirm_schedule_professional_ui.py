import streamlit as st
from views import View
from datetime import datetime
from time import sleep

class ConfirmScheduleProfessionalUI:
    """Página do Profissional de Confirmar um Serviço."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Confirmar Serviço",
            page_icon="🖊️"
        )
        
        st.header("🖊️ Confirmar Serviço")

        user_id: int = st.session_state["user_id"]
        prof_data = View.get_professional(user_id)
        if prof_data is None: return

        schedules = View.get_schedules_by_professional(prof_data.id)
        if len(schedules) <= 0:
            st.warning("Sem Horários Agendados", icon="⚠")
            return
        
        schedule = st.selectbox("Informe o Horário", schedules)
        schedule_client = View.get_client(schedule.client_id)
        if not schedule_client: 
            st.warning("Nenhum Cliente marcou esse Horário ainda", icon="⚠")
            return
        client = st.text_input("Cliente Marcado", schedule_client, disabled=True)
        service = st.text_input("Serviço Selecionado", View.get_service(schedule.service_id), disabled=True)

        do_confirmation = st.button("Confirmar" if not schedule.confirmed else "Desmarcar")

        if do_confirmation:
            try:
                View.update_schedule(schedule.id, schedule.date, not schedule.confirmed, schedule_client, View.get_service(schedule.service_id), prof_data)
                View.append_notification(f"Horário {schedule.id} foi {'Confirmado' if not schedule.confirmed else 'Desmarcado'}.", datetime.now(), schedule_client.id, View.get_users_type().CLIENT)
                st.success(f"Horário {'Confirmado' if not schedule.confirmed else 'Desmarcado'} com Sucesso!", icon="✔")
            except Exception as e:
                st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
            sleep(2)
            st.rerun()
