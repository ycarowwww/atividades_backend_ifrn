from templates.keep_client_ui import KeepClientUI
from templates.keep_service_ui import KeepServiceUI
import streamlit as st

class IndexUI:
    @classmethod
    def menu_admin(cls) -> None:
        st.sidebar.header("Menu de Admin")

        op = st.sidebar.selectbox("Menu", ["Cadastro de Clientes", "Cadastro de Serviços"])
        
        if op == "Cadastro de Clientes": KeepClientUI.main()
        if op == "Cadastro de Serviços": KeepServiceUI.main()

    @staticmethod
    def sidebar() -> None:
        IndexUI.menu_admin()

    @staticmethod
    def main() -> None:
        IndexUI.sidebar()

if __name__ == "__main__":
    IndexUI.main()
