import streamlit as st
from Interfaces.Login_Page import login_page
from Interfaces.Main_Page import main_page


def main():


    # Initialize session state for tracking login status
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Router Logic
    if not st.session_state.logged_in:
        login_page()
    else:
        main_page()


if __name__ == "__main__":
    main()
