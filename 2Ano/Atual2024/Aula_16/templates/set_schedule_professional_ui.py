import streamlit as st
from views import View
from datetime import date, time, datetime
from time import sleep

class SetScheduleProfessionalUI:
    """Página do Profissional de Agendar um Serviço."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Abrir Minha Agenda",
            page_icon="📅"
        )
        
        st.header("📅 Abrir Minha Agenda")

        user_id: int = st.session_state["user_id"]
        prof_data = View.get_professional(user_id)
        if prof_data is None: return

        date_entered = st.date_input("Informe a data do Serviço", date.today())
        col1, col2, col3 = st.columns(3) # Inputs para o tempo da data (o "date_input" não oferece a hora, apenas a data).
        with col1: beginning_hours = st.number_input("Horas Iniciais", 0, 23, step=1)
        with col2: beginning_minutes = st.number_input("Minutos Iniciais", 0, 59, step=1)
        with col3: beginning_seconds = st.number_input("Segundos Iniciais", 0, 59, step=1)

        with col1: ending_hours = st.number_input("Horas Finais", 0, 23, step=1)
        with col2: ending_minutes = st.number_input("Minutos Finais", 0, 59, step=1)
        with col3: ending_seconds = st.number_input("Segundos Finais", 0, 59, step=1)
        beginning_time = time(beginning_hours, beginning_minutes, beginning_seconds) # Converte os inputs de tempo para um objeto "time"
        ending_time = time(ending_hours, ending_minutes, ending_seconds) # Converte os inputs de tempo para um objeto "time"
        beginning_datetime = datetime.combine(date_entered, beginning_time) # Junta o "time" com o "date" do "date_input"
        ending_datetime = datetime.combine(date_entered, ending_time) # Junta o "time" com o "date" do "date_input"

        interval = st.number_input("Informe o intervalo entre os horários (Minutos)", 0)
        set_schedule = st.button("Abrir Agenda")

        if set_schedule:
            if beginning_datetime > ending_datetime:
                st.warning("Horários Inválidos", icon="⚠")
                sleep(1)
                st.rerun()
                return
            
            try:
                View.append_multiple_schedules(beginning_datetime, ending_datetime, interval, prof_data)
                st.success("Horário Agendado com Sucesso!", icon="✔")
            except Exception as e:
                st.error(f"Um Erro Ocorreu: {e}", icon="🚨")
            sleep(1)
            st.rerun()
