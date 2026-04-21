import sqlite3
import pandas as pd

def view_database():
    try:
        conn = sqlite3.connect('voice_embeddings.db')
        query = "SELECT id, text FROM embeddings" # Embedding BLOB ని వదిలేసి టెక్స్ట్ మాత్రమే చూపిస్తున్నాం
        df = pd.read_sql_query(query, conn)
        
        if not df.empty:
            print("✅ Database Contents:")
            print(df)
        else:
            print("❌ Database is empty.")
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    view_database()