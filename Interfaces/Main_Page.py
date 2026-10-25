import streamlit as st
from datetime import datetime
from Databases.Database_Manager import member_database_entry
import time

def main_page():

    # Set page configuration to wide layout for better row formatting
    st.set_page_config(page_title="Main Page", layout="wide")
    mb = member_database_entry()


    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Add New Product"  # Default option

    # Handle Logout
    if not st.session_state.logged_in:
        st.title("Logged Out")
        st.info("You have been successfully logged out.")
        if st.button("Log In Again"):
            st.session_state.logged_in = False
            st.rerun()
        st.stop()

    # ----------------------------------------------------
    # 2. Header Area (Top Right Name & Logout Button)
    # ----------------------------------------------------
    header_col1, header_col2 = st.columns([4, 1.2])

    with header_col1:
        st.title("Main Page")

    with header_col2:
        # Right-aligned user details and logout button
        st.markdown(
            f"<div style='text-align: right; font-weight: bold; padding-top: 10px;'>👤 {st.session_state.user_full_name}</div>", 
            unsafe_allow_html=True
        )
        if st.button("LOGOUT", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.rerun()

    st.divider()

    # ----------------------------------------------------
    # 3. Row Navigation (Horizontal Button Row)
    # ----------------------------------------------------
    nav_options = [
        "Add New Product",
        "Update Existing Product Entries",
        "Check Product",
        "Stock Alerts",
        "Remove Product",
        "Recent Entries",
        "Application Access"
    ]

    # Create equal-width columns for row format buttons
    cols = st.columns(len(nav_options))

    for idx, option in enumerate(nav_options):
        with cols[idx]:
            # Highlight active option button
            is_active = st.session_state.active_tab == option
            button_type = "primary" if is_active else "secondary"
            
            if st.button(option, key=f"nav_btn_{idx}", type=button_type, use_container_width=True):
                st.session_state.active_tab = option
                st.rerun()

    st.write("")  # Spacing

    # ----------------------------------------------------
    # 4. Dynamic Page Content Rendering
    # ----------------------------------------------------
    active = st.session_state.active_tab

    st.subheader(active)

    if active == "Add New Product":
        st.write("### Form to Add a New Product")
        with st.form("add_product_form"):
            p_name = st.text_input("Product Name",max_chars=30)
            p_quantity = st.number_input("Product Quantity",min_value=0)
            p_supplier = st.text_input("Product Supplier",max_chars=30)
            p_cpi = st.number_input("Product Cost(Per Item)",min_value=0)
            p_pmq = st.number_input("Product Minimum Quantity",min_value=0)
            submitted = st.form_submit_button("Save Product")
            if submitted:
                if len(p_name) == 0:
                    st.error("Enter Correct Product Name")
                elif p_quantity == 0:
                    st.error("Quantity can't be Zero '0'")
                elif len(p_supplier) == 0:
                    st.error("Provide Supplier Name")
                elif p_cpi == 0.0:
                    st.error("Provide Cost per Item")
                elif p_pmq == 0:
                    st.error("Minimum Quantity can't be zero")
                else:
                    st.success(mb.insert_product(p_name,p_quantity,p_supplier,p_cpi,datetime.now(),st.session_state.user_full_name,p_pmq))
                

    elif active == "Update Existing Product Entries":
        st.write("Select a product to edit its details.")
        p_data_list = mb.get_product_summary_list()
        p_names_list = [list(item.keys())[0] for item in p_data_list]
        p_name_u = st.selectbox("Choose Product", p_names_list)
        p_quantity_in = ""
        p_supplier_name_in = ""
        p_product_cost_in = ""
        for item in p_data_list:
            if p_name_u in item:
                 p_quantity_in =  item[p_name_u]['Product_Quantity']
                 p_supplier_name_in = item[p_name_u]['Supplier_Name']
                 p_product_cost_in = item[p_name_u]['Product_Cost']
        with st.form("add_product_form"):
            p_quantity_n1 = st.number_input("Provide New Product Quantity",min_value=0)
            st.text(f"Quantity Available : {p_quantity_in}")
            st.text(f"Supplier Name : {p_supplier_name_in}")
            st.text(f"Product Cost per Item : {p_product_cost_in}")
            submitted_up = st.form_submit_button("Save Product")
            if submitted_up:
                if p_quantity_n1 == 0:
                    st.error("Please provide valid quantity")
                else:
                    st.success(mb.update_product(p_name_u,p_quantity_n1,p_supplier_name_in,p_product_cost_in,datetime.now(),st.session_state.user_full_name))
                    time.sleep(1)
                    st.rerun()


    elif active == "Check Product":
        product_df = mb.return_invertory_table()
        st.dataframe(product_df)

    elif active == "Stock Alerts":
        return_df = mb.return_invertory_alerts()
        for i in range(len(return_df)):
            st.warning(f"⚠️ Warning: Product {return_df.iloc[i]["Product Name"]}  is low on stock (Only {return_df.iloc[i]["Product Quantity"]} left). Minimum required - {return_df.iloc[i]["Minimum Quantity"]}")

    elif active == "Remove Product":
        st.write("Select a product to remove from inventory.")
        dl_data_list = mb.get_product_summary_list()
        dl_names_list = [list(item.keys())[0] for item in dl_data_list]
        dl_name_u = st.selectbox("Choose Product", dl_names_list)
        dl_submitted = st.button("Delete Product",type="primary")
        if dl_submitted:
            st.success(mb.delete_product(dl_name_u))
            time.sleep(1)
            st.rerun()

    elif active == "Recent Entries":
        st.write("Displaying recent system entries")
        transaction_df = mb.return_transaction_table()
        st.dataframe(transaction_df)

    elif active == "Application Access":
        st.write("Manage user roles and permissions")
        with st.form("add_product_form"):
            fl_name = st.text_input("Full Name",max_chars=32)
            us_name = st.text_input("User Name",max_chars=10)
            pswd = st.text_input("Password",max_chars=12,type="password")
            submitted_usr = st.form_submit_button("Add User")
            if submitted_usr:
                if len(fl_name) == 0:
                    st.error("Enter Full Name")
                elif len(us_name) == 0:
                    st.error("Enter User Name")
                elif len(pswd) == 0:
                    st.error("Enter Password")
                else:
                    st.success(mb.insert_access_table(fl_name,us_name,pswd,datetime.now().strftime("%Y-%m-%d")))
                    time.sleep(1)
                    st.rerun()
