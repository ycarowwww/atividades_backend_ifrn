import streamlit as st
from rectangle import Rectangle

class RectangleUI:
    @staticmethod
    def main() -> None:
        st.header("Rectangle Properties")
        col1, col2 = st.columns(2)
        base = col1.number_input("Base's Value:", min_value=0.0, step=0.1)
        height = col2.number_input("Height's Value:", min_value=0.0, step=0.1)
        do_calculation = st.button("Calculate", type="primary")

        if do_calculation:
            rect = Rectangle(base, height)
            
            st.text(rect)
            st.text(f"Rectangle's Area: {rect.calc_area()}")
            st.text(f"Rectangle's Diagonal: {rect.calc_diagonal()}")
