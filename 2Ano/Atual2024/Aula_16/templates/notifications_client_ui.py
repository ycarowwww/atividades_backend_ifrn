import streamlit as st
from views import View

class NotificationsClientUI:
    """Página das Notificações do Cliente."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Minhas Notificações",
            page_icon="🔔"
        )
        
        st.header("🔔 Minhas Notificações")

        user_id: int = st.session_state["user_id"]
        client_data = View.get_client(user_id)
        if client_data is None: return

        notifications = View.get_notifications(client_data.id, View.get_users_type().CLIENT)

        for notif in notifications:
            st.divider()
            st.subheader("Corpo da Mensagem")
            st.text(notif.message)
            st.text(f"Data de Envio: {notif.get_formatted_date_sent()}")

        if len(notifications) <= 0:
            st.warning("Nenhuma Notificação Ainda!", icon="⚠")
