import streamlit as st
from patient import Patient

class PatientUI:
    @staticmethod
    def main() -> None:
        st.header("Patient Data")
        name = st.text_input("Name:")
        cpf = st.text_input("CPF:")
        phone = st.text_input("Phone:")
        birthday = st.date_input("Birthday:")
        
        see_age = st.button("See Age")

        if see_age:
            patient = Patient(name, cpf, phone, birthday)

            years, months = patient.age()
            st.text(f"Patient's Age: {years} Years and {months} Months")
            st.text(patient)

PatientUI.main()
