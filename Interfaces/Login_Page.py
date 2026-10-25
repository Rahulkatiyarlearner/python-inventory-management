import streamlit as st
from Databases.Database_Manager import member_database_entry


# Configure the page layout and title
st.set_page_config(page_title="App Navigation", page_icon="🔒")

def login_page():
    # Header / Page Title matching design
    st.markdown("### Inventory Management:")
    st.markdown("#### Login Page")
    st.text("Default - User Name : Admin - Password  : Admin123")
    
    # Create a clean boxed form for credentials
    with st.form("login_form", clear_on_submit=False):
        st.subheader("Login")
        
        # Username and Password input fields
        username = st.text_input("User Name",max_chars=10)
        password = st.text_input("Password", type="password",max_chars=12)
        
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            # Validate credentials
            md = member_database_entry()
            return_data = md.validate_access_table(username,password)
            if return_data is not None:
                st.session_state.logged_in = True
                st.session_state["user_full_name"] = return_data
                st.success("Login successful!")
                st.rerun()  # Refresh the app state to show the main page
            else:
                # Show error message in case of incorrect input
                st.error("Incorrect User Name or Password. Please try again.")

                


