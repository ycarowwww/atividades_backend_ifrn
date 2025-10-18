import pandas as pd
import streamlit as st
from views import View

class ScheduleClientUI:
    """Página do Cliente que mostra seus Horários cadastrados."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Visualizar Serviços",
            page_icon="⏰"
        )
        
        st.header("⏰ Meus Serviços")

        user_id: int = st.session_state["user_id"]

        schedules = View.get_schedules_by_client(user_id)
        schedules_data: list[list] = []
        for schedule in schedules:
            service_description = View.get_service(schedule.service_id)
            if service_description: service_description = service_description.description # Pega a descrição do Serviço se ele existir.
            professional_name = View.get_professional(schedule.professional_id)
            if professional_name: professional_name = professional_name.name # Pega o nome do Profissional se ele existir.

            schedules_data.append([ schedule.id, schedule.get_formatted_date(), schedule.confirmed, service_description, professional_name ])
        
        data = pd.DataFrame(
            schedules_data,
            columns=["ID", "Data", "Confirmado", "Serviço", "Profissional"]
        )

        st.dataframe(data)
