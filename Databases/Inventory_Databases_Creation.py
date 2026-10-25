import sqlite3


def create_inventory_database():
  # Connect to SQLite database (this creates 'inventory.db' in your directory)
  conn = sqlite3.connect("inventory.db")
  cursor = conn.cursor()

  # IMPORTANT: SQLite disables foreign key constraints by default. Enable them:
  cursor.execute("PRAGMA foreign_keys = ON;")

  # 1. Create Access_Table first (so other tables can safely reference it)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS Access_Table (
            Full_Name CHAR(32) PRIMARY KEY,
            User_Name VARCHAR(10) NOT NULL,
            Password VARCHAR(12) NOT NULL,
            User_added_date DATE
        )
    """)

  # 2. Create Invertory_table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS Invertory_table (
            Product_Name VARCHAR(30) UNIQUE NOT NULL,
            Product_Quantity INTEGER NOT NULL,
            Product_Suppliers VARCHAR(50),
            Product_Cost INTEGER NOT NULL,
            Last_Entry_Date_Time TIMESTAMP,
            Last_Entry_Person CHAR(32),
            Minimum_quantity INTEGER NOT NULL,
            FOREIGN KEY (Last_Entry_Person) REFERENCES Access_Table(Full_Name)
        )
    """)

  # 3. Create Transaction_table (allows multiple entries of the same product)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transaction_table (
            Product_Name VARCHAR(30) NOT NULL,
            Product_Quantity INTEGER NOT NULL,
            Product_Suppliers VARCHAR(50),
            Product_Cost INTEGER NOT NULL,
            Last_Entry_Date_Time CHAR(32),
            Last_Entry_Person CHAR(32),
            FOREIGN KEY (Last_Entry_Person) REFERENCES Access_Table(Full_Name)
        )
    """)

  # Commit changes and close connection
  conn.commit()
  conn.close()
  print("Database 'inventory.db' and all three tables created successfully!")


if __name__ == "__main__":
  create_inventory_database()