import streamlit as st
from views import View

class NotificationsProfessionalUI:
    """Página das Notificações do Profissional."""
    @staticmethod
    def main() -> None:
        st.set_page_config(
            page_title="Minhas Notificações",
            page_icon="🔔"
        )
        
        st.header("🔔 Minhas Notificações")

        user_id: int = st.session_state["user_id"]
        prof_data = View.get_professional(user_id)
        if prof_data is None: return

        notifications = View.get_notifications(prof_data.id, View.get_users_type().PROFESSIONAL)

        for notif in notifications:
            st.divider()
            st.subheader("Corpo da Mensagem")
            st.text(notif.message)
            st.text(f"Data de Envio: {notif.get_formatted_date_sent()}")

        if len(notifications) <= 0:
            st.warning("Nenhuma Notificação Ainda!", icon="⚠")