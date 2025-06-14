import sqlite3

def test_connection():
    try:
        conn = sqlite3.connect("database/weatherdata.db")
        cursor = conn.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if tables:
            print("✅ Tables in the database:")
            for table in tables:
                print("-", table[0])
        else:
            print("⚠️ No tables found in the database.")

        conn.close()

    except Exception as e:
        print("❌ Failed to connect or query the database.")
        print("Error:", e)

test_connection()
