import pandas as pd
import streamlit as st
from datetime import datetime, date, time
from time import sleep
from views import View
from typing import Any

class KeepScheduleUI:
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Cadastro de Horários",
            page_icon="⏱️"
        )
        
        st.header("⏱️ Cadastro de Horários")

        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Deletar"])

        with tab1: KeepScheduleUI.list_schedules()
        with tab2: KeepScheduleUI.insert_schedule()
        with tab3: KeepScheduleUI.update_schedule()
        with tab4: KeepScheduleUI.remove_schedule()
    
    @staticmethod
    def list_schedules() -> None:
        schedules = View.get_schedule_list()
        schedules_data: list[list[Any]] = []
        for schedule in schedules:
            client_name = View.get_client(schedule.client_id)
            if client_name: client_name = client_name.name # Gets the Client's name if the client exists
            service_description = View.get_service(schedule.service_id)
            if service_description: service_description = service_description.description # Gets the Service's description if the service exists
            professional_name = View.get_professional(schedule.professional_id)
            if professional_name: professional_name = professional_name.name

            schedules_data.append([ schedule.id, schedule.get_formatted_date(), schedule.confirmed, client_name, service_description, professional_name ])
        
        data = pd.DataFrame(
            schedules_data,
            columns=["ID", "Data", "Confirmado", "Cliente", "Serviço", "Profissional"]
        )

        st.dataframe(data)

    @staticmethod
    def insert_schedule() -> None:
        date_entered = st.date_input("Informe a data do Serviço", date.today())
        col1, col2, col3 = st.columns(3)
        with col1: hours = st.number_input("Horas", 0, 23, step=1)
        with col2: minutes = st.number_input("Minutos", 0, 59, step=1)
        with col3: seconds = st.number_input("Segundos", 0, 59, step=1)
        time_entered = time(hours, minutes, seconds)
        datetime_entered = datetime.combine(date_entered, time_entered)
        confirmed = st.checkbox("Confirmado", key="confirmed_1")
        client = st.selectbox("Informe o Cliente", View.get_client_list(), index=None)
        service = st.selectbox("Informe o Serviço", View.get_service_list(), index=None)
        professional = st.selectbox("Informe o Profissional", View.get_professional_list(), index=None)

        do_insert = st.button("Inserir Horário")

        if do_insert:
            View.append_schedule(datetime_entered, confirmed, client, service, professional)
            st.success("Horário Inserido com Sucesso!", icon="✔")
            sleep(2)
            st.rerun()

    @staticmethod
    def update_schedule() -> None:
        schedules = View.get_schedule_list()

        if len(schedules) <= 0:
            st.write("Nenhum Horário Registrado.")
        else:
            schedule_selected = st.selectbox(
                "Selecione um Horário para Atualizar",
                schedules
            )
            date_entered = st.date_input("Informe a nova data do Serviço", schedule_selected.date)
            col1, col2, col3 = st.columns(3)
            with col1: hours = st.number_input("Novas Horas", 0, 23, schedule_selected.date.hour, 1)
            with col2: minutes = st.number_input("Novos Minutos", 0, 59, schedule_selected.date.minute, 1)
            with col3: seconds = st.number_input("Novos Segundos", 0, 59, schedule_selected.date.second, 1)
            time_entered = time(hours, minutes, seconds)
            datetime_entered = datetime.combine(date_entered, time_entered)
            confirmed = st.checkbox("Confirmado", schedule_selected.confirmed, "confirmed_2")
            client = st.selectbox("Informe o novo Cliente", View.get_client_list(), index=None)
            service = st.selectbox("Informe o novo Serviço", View.get_service_list(), index=None)
            professional = st.selectbox("Informe o novo Profissional", View.get_professional_list(), index=None)

            do_update = st.button("Atualizar Horário")

            if do_update:
                View.update_schedule(schedule_selected.id, datetime_entered, confirmed, client, service, professional)
                st.success("Horário Atualizado com Sucesso!", icon="✔")
                sleep(2)
                st.rerun()

    @staticmethod
    def remove_schedule() -> None:
        schedules = View.get_schedule_list()

        if len(schedules) <= 0:
            st.write("Nenhum Horário Registrado.")
        else:
            schedule_selected = st.selectbox(
                "Selecione um Horário para Deletar",
                schedules
            )
            do_removal = st.button("Deletar Horário", type="primary")

            if do_removal:
                View.remove_schedule(schedule_selected.id)
                st.success("Horário Deletado com Sucesso!", icon="✔")
                sleep(2)
                st.rerun()
