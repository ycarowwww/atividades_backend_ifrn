import pandas as pd
import streamlit as st
from views import View

class ScheduleProfessionalUI:
    """Página do Profissional que mostra seus Horários cadastrados."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Visualizar Horários",
            page_icon="⏰"
        )
        
        st.header("⏰ Meus Horários")

        user_id: int = st.session_state["user_id"]
        prof_data = View.get_professional(user_id)

        schedules = View.get_schedule_list()
        schedules_data: list[list] = []
        for schedule in schedules:
            if schedule.professional_id != prof_data.id: continue # Pega apenas os horários que pertencem ao Profissional atual.
            client_name = View.get_client(schedule.client_id)
            if client_name: client_name = client_name.name # Pega o nome do Cliente se ele existir.
            service_description = View.get_service(schedule.service_id)
            if service_description: service_description = service_description.description # Pega a descrição do Serviço se ele existir.

            schedules_data.append([ schedule.id, schedule.get_formatted_date(), schedule.confirmed, client_name, service_description ])
        
        data = pd.DataFrame(
            schedules_data,
            columns=["ID", "Data", "Confirmado", "Cliente", "Serviço"]
        )

        st.dataframe(data)
