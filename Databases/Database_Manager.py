import sqlite3
from Databases.Context_Manager import database_manager
from datetime import datetime
import pandas as pd

class member_database_entry:
    
    def __init__(self):
        self.db = database_manager("inventory.db")


    def insert_access_table(self, In_Full_Name, In_User_Name, In_Password, User_added_date):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if record already exists
            cursor.execute("SELECT 1 FROM Access_Table WHERE Full_Name = ?", (In_Full_Name,))
            if cursor.fetchone():
                return "Duplicate record: Full name already exists."
            
            # Insert if it doesn't exist
            cursor.execute(
                """
                INSERT INTO Access_Table(Full_Name, User_Name, Password, User_added_date)
                VALUES (?, ?, ?, ?)
                """,
                (In_Full_Name, In_User_Name, In_Password, User_added_date)
            )
            conn.commit()
            
        return "User added successfully."


    def validate_access_table(self, In_User_Name, In_Password):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Corrected SQL query (removed invalid VALUES clause)
            cursor.execute(
                """
                SELECT * FROM Access_Table WHERE User_Name = ? AND Password = ?
                """,
                (In_User_Name, In_Password)
            )
            output = cursor.fetchone()

            # Check if record was found (None means no match found)
            if output is not None:
                return output[0]
            else:
                return None


    def insert_product(
        self,
        product_name,
        product_quantity,
        product_suppliers,
        product_cost,
        last_entry_date_time,
        last_entry_person,
        minimum_quantity,
    ):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Check if Product_Name already exists (Notice the comma inside (product_name,))
            cursor.execute(
                "SELECT 1 FROM Invertory_table WHERE Product_Name = ?", (product_name,)
            )
            existing_product = cursor.fetchone()

            if existing_product:
                return "Item already available"
            else:
            # 2. Insert Invertory_table if not available (Only one clean insert statement)
                cursor.execute(
                    """
                            INSERT INTO Invertory_table (
                                Product_Name, 
                                Product_Quantity, 
                                Product_Suppliers, 
                                Product_Cost, 
                                Last_Entry_Date_Time, 
                                Last_Entry_Person, 
                                Minimum_quantity
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                    (
                        product_name,
                        product_quantity,
                        product_suppliers,
                        product_cost,
                        last_entry_date_time,
                        last_entry_person,
                        minimum_quantity,
                    ),
                )
                conn.commit()
                # 3. Insert Transaction_table if not available (Only one clean insert statement)
                cursor.execute(
                    """
                            INSERT INTO Transaction_table (
                                Product_Name, 
                                Product_Quantity, 
                                Product_Suppliers, 
                                Product_Cost, 
                                Last_Entry_Date_Time, 
                                Last_Entry_Person 
                            ) VALUES (?, ?, ?, ?, ?, ?)
                        """,
                    (
                        product_name,
                        product_quantity,
                        product_suppliers,
                        product_cost,
                        last_entry_date_time,
                        last_entry_person,
                    ),
                )
                conn.commit()
                return "Item inserted successfully"


    def delete_product(self, product_name):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Check if the product exists before trying to delete
            cursor.execute(
                "SELECT 1 FROM Invertory_table WHERE Product_Name = ?", (product_name,)
            )
            existing_product = cursor.fetchone()

            if not existing_product:
                return "Item not found"

            # 2. Delete the record if it exists
            cursor.execute(
                "DELETE FROM Invertory_table WHERE Product_Name = ?", (product_name,)
            )
            conn.commit()
            
            return "Item deleted successfully"


    def get_product_summary_list(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            # Query Product_Name, Product_Suppliers, and Product_Cost from your table
            cursor.execute(
                "SELECT Product_Name, Product_Quantity, Product_Suppliers, Product_Cost FROM Invertory_table"
            )
            rows = cursor.fetchall()

            # Build the list of dictionaries: [{product_name: {"Supplier_Name": ..., "Product_Cost": ...}}, ...]
            result_list = []
            for row in rows:
                product_name = row[0]
                product_quantity = row[1]
                supplier_name = row[2]
                product_cost = row[3]

                product_dict = {
                    product_name: {
                        "Supplier_Name": supplier_name,
                        "Product_Quantity": product_quantity,
                        "Product_Cost": product_cost,
                    }
                }
                result_list.append(product_dict)

            return result_list


    def update_product(
            self,
            product_name,
            product_quantity,
            product_suppliers,
            product_cost,
            last_entry_date_time,
            last_entry_person,
        ):
            with self.db.get_connection() as conn:
                cursor = conn.cursor()

                # 1. Update Invertory_table if not available (Only one clean insert statement)
                cursor.execute("""
                    UPDATE Invertory_table
                    SET Product_Quantity = ?
                    WHERE Product_Name = ?
                """, 
                (product_quantity,product_name))
                
                conn.commit()

                # 3. Insert Transaction_table if not available (Only one clean insert statement)
                cursor.execute(
                    """
                            INSERT INTO Transaction_table (
                                Product_Name, 
                                Product_Quantity, 
                                Product_Suppliers, 
                                Product_Cost, 
                                Last_Entry_Date_Time, 
                                Last_Entry_Person 
                            ) VALUES (?, ?, ?, ?, ?, ?)
                        """,
                    (
                        product_name,
                        product_quantity,
                        product_suppliers,
                        product_cost,
                        last_entry_date_time,
                        last_entry_person,
                    ),
                )
                conn.commit()
                return "Item updated successfully"

    def return_invertory_table(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Corrected SQL query (removed invalid VALUES clause)
            cursor.execute(
                """
                SELECT * FROM Invertory_table
                """
            )
            output = cursor.fetchall()

            # Check if record was found (None means no match found)
            if output is not None:
                columns = [
                    "Product Name",
                    "Product Quantity",
                    "Product Suppliers",
                    "Product Cost",
                    "Last Entry Date Time",
                    "Last Entry Person",
                    "Minimum Quantity"
                ]

                # Create the DataFrame
                inventory_df = pd.DataFrame(output, columns=columns)
                return inventory_df
            else:
                return None

    def return_invertory_alerts(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Corrected SQL query (removed invalid VALUES clause)
            cursor.execute(
                """
                SELECT product_name,product_quantity,minimum_quantity
                FROM Invertory_table
                WHERE product_quantity < minimum_quantity
                """
            )
            output = cursor.fetchall()

            # Check if record was found (None means no match found)
            if output is not None:
                columns = [
                    "Product Name",
                    "Product Quantity",
                    "Minimum Quantity"
                ]

                # Create the DataFrame
                inventory_df = pd.DataFrame(output, columns=columns)
                return inventory_df
            else:
                return None


    def return_transaction_table(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Corrected SQL query (removed invalid VALUES clause)
            cursor.execute(
                """
                SELECT * FROM Transaction_table
                ORDER BY Last_Entry_Date_Time DESC
                """
            )
            output = cursor.fetchall()

            # Check if record was found (None means no match found)
            if output is not None:
                columns = [
                    "Product Name",
                    "Product Quantity",
                    "Product Suppliers",
                    "Product Cost",
                    "Last Entry Date Time",
                    "Last Entry Person",
                ]

                # Create the DataFrame
                inventory_df = pd.DataFrame(output, columns=columns)
                return inventory_df
            else:
                return None




