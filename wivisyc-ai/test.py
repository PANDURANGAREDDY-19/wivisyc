"""
Wivisyc AI - Live Translation Integration Test
===============================================
Simulates a real-time two-speaker translation session.

Pipeline per speaker turn:
    Audio Input -> Speech-to-Text (Whisper) -> Translation (MarianMT)
                -> Text-to-Speech (XTTS v2) -> Audio Output

Speaker A: English input, Spanish audio output
Speaker B: Spanish input, English audio output

Speaker voice embeddings are stored to the database after each turn
for future speaker identification and personalization.

Usage:
    python test.py --a <path_to_speaker_a.wav> --b <path_to_speaker_b.wav>

Requirements:
    Both input files must be valid .wav audio files with clear speech.
"""

import sys
import os
import io
import wave
import argparse
import numpy as np
import torch

# Register module search paths for sibling packages
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Embeddings"))

# Speech-to-text and translation functions from the STT module
from speech_to_text import get_text_from_audio, en_to_es, es_to_en

# Voice embedding storage functions from the Embeddings module
from app import init_db, audio_to_text, embed_model, store_embedding

# Load XTTS v2 directly to avoid the module-level English warmup in
# text_to_speech.py, which corrupts the HiFi-GAN decoder state for
# non-English languages and produces distorted audio output.
print("Initializing XTTS v2 text-to-speech model...")
from TTS.api import TTS as _TTS
_tts_api = _TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
_xtts    = _tts_api.synthesizer.tts_model
_latent  = _xtts.speaker_manager.speakers["Ana Florence"]["gpt_cond_latent"]
_emb     = _xtts.speaker_manager.speakers["Ana Florence"]["speaker_embedding"]
SAMPLE_RATE = 24000


def _speak_to_file(text: str, lang: str, out_path: str) -> None:
    """
    Synthesize speech from text and write the result to a WAV file.

    Args:
        text:     The translated text to synthesize.
        lang:     BCP-47 language code for synthesis (e.g. 'en', 'es').
        out_path: Absolute path to the output WAV file.
    """
    with torch.no_grad():
        result = _xtts.inference(
            text=text,
            language=lang,
            gpt_cond_latent=_latent,
            speaker_embedding=_emb,
            temperature=0.65,
            top_k=30,
            top_p=0.85,
            repetition_penalty=10.0,
            speed=1.0,
        )

    wav = np.array(result["wav"], dtype=np.float32)
    print(f"    Audio duration : {len(wav)/SAMPLE_RATE:.2f}s")
    print(f"    Amplitude range: [{wav.min():.3f}, {wav.max():.3f}]")

    # Convert normalized float32 samples to 16-bit PCM and wrap in WAV container
    pcm = (wav * 32767).astype(np.int16).tobytes()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)
    with open(out_path, "wb") as f:
        f.write(buf.getvalue())


def run_turn(label: str, audio_path: str, out_path: str, conn) -> None:
    """
    Execute one full translation turn for a single speaker.

    Steps:
        1. Transcribe the input audio using Whisper STT.
        2. Store a sentence embedding of the transcription for speaker tracking.
        3. Translate the transcription to the opposing language.
        4. Synthesize the translated text to an output WAV file.

    Args:
        label:      Display name for the speaker (e.g. 'Speaker A').
        audio_path: Path to the speaker's input audio file.
        out_path:   Path where the translated audio output will be saved.
        conn:       Active SQLite database connection for embedding storage.
    """
    print(f"\n[{label}]")
    print(f"  Input  : {audio_path}")

    # Step 1: Transcribe audio to text and detect source language
    text, lang = get_text_from_audio(audio_path)
    print(f"  Transcription ({lang.upper()}): {text}")

    if not text:
        print(f"  WARNING: Empty transcription for {label}. Skipping turn.")
        return

    # Step 2: Encode and store speaker embedding for this utterance.
    # Reuses the Whisper transcription to avoid running a second STT pass.
    embedding = embed_model.encode(text)
    store_embedding(conn, text, embedding)
    print(f"  Embedding stored for {label}")

    # Step 3: Translate to the opposing speaker's language
    if lang == "en":
        translated, tgt_lang = en_to_es(text), "es"
    elif lang == "es":
        translated, tgt_lang = es_to_en(text), "en"
    else:
        print(f"  WARNING: Unsupported language detected ({lang}). Skipping turn.")
        return
    print(f"  Translation ({tgt_lang.upper()}): {translated}")

    # Step 4: Synthesize translated text to audio
    _speak_to_file(translated, tgt_lang, out_path)
    print(f"  Output : {out_path}")


def main():
    """
    Entry point. Parses input audio paths and runs the two-speaker
    translation pipeline, producing one output WAV file per speaker.
    """
    parser = argparse.ArgumentParser(
        description="Wivisyc live two-speaker translation test"
    )
    parser.add_argument("--a", required=True, help="Path to Speaker A audio (.wav)")
    parser.add_argument("--b", required=True, help="Path to Speaker B audio (.wav)")
    args = parser.parse_args()

    base  = os.path.dirname(os.path.abspath(__file__))
    out_a = os.path.join(base, "out_speaker_a.wav")  # Delivered to Speaker A (translated from B)
    out_b = os.path.join(base, "out_speaker_b.wav")  # Delivered to Speaker B (translated from A)

    conn = init_db()
    try:
        run_turn("Speaker A", args.a, out_b, conn)
        run_turn("Speaker B", args.b, out_a, conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
