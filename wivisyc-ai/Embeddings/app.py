import sqlite3
import numpy as np
from faster_whisper import WhisperModel
from sentence_transformers import SentenceTransformer
import os

# Initialize models
whisper_model = WhisperModel("base", compute_type="int8")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def init_db():
    conn = sqlite3.connect("voice_embeddings.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        embedding BLOB
    )
    """)
    conn.commit()
    return conn

def audio_to_text(audio_path):
    if not os.path.exists(audio_path):
        print(f"Error: {audio_path} not found!")
        return None
    segments, _ = whisper_model.transcribe(audio_path)
    text = " ".join([seg.text for seg in segments])
    return text

def store_embedding(conn, text, embedding):
    embedding_bytes = embedding.tobytes()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO embeddings (text, embedding) VALUES (?, ?)",
        (text, embedding_bytes)
    )
    conn.commit()

def process_audio(audio_path):
    conn = init_db()
    print("Transcribing audio...")
    text = audio_to_text(audio_path)
    
    if text:
        print("Text:", text)
        print("Generating embedding...")
        embedding = embed_model.encode(text)
        print("Storing in database...")
        store_embedding(conn, text, embedding)
        print("Done!")
    
    conn.close()

if __name__ == "__main__":
    # మీ ఆడియో ఫైల్ పేరు ఇక్కడ మార్చండి
    audio_file = "medieval-gamer-voice.mp3" 
    process_audio(audio_file)