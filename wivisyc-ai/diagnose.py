"""
Diagnostic script - run this BEFORE test.py to isolate which stage is broken.
Usage:
    python diagnose.py --a Embeddings/medieval-gamer-voice.wav
"""
import sys, os, io, wave, argparse
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))

# ── STEP 1: STT ───────────────────────────────────────────────────────────────
print("\n[STEP 1] Loading Whisper STT...")
from faster_whisper import WhisperModel
stt = WhisperModel("tiny", device="cpu", compute_type="int8")

parser = argparse.ArgumentParser()
parser.add_argument("--a", required=True)
args = parser.parse_args()

print(f"  Transcribing: {args.a}")
segments, info = stt.transcribe(args.a, beam_size=5)
text = "".join(s.text for s in segments).strip()
lang = info.language
print(f"  Language detected : {lang}")
print(f"  Transcribed text  : '{text}'")

if not text:
    print("  ❌ STT returned empty text — check your audio file has clear speech")
    sys.exit(1)
print("  ✅ STT OK")

# ── STEP 2: Translation ───────────────────────────────────────────────────────
print("\n[STEP 2] Loading MarianMT translation models...")
from transformers import MarianMTModel, MarianTokenizer

if lang == "en":
    name = "Helsinki-NLP/opus-mt-en-es"
    tgt_lang = "es"
elif lang == "es":
    name = "Helsinki-NLP/opus-mt-es-en"
    tgt_lang = "en"
else:
    print(f"  ❌ Unsupported language: {lang}")
    sys.exit(1)

tokenizer = MarianTokenizer.from_pretrained(name)
model_mt = MarianMTModel.from_pretrained(name)
tokens = tokenizer(text, return_tensors="pt", padding=True)
out = model_mt.generate(**tokens)
translated = tokenizer.decode(out[0], skip_special_tokens=True)
print(f"  Translated ({lang} → {tgt_lang}): '{translated}'")

if not translated:
    print("  ❌ Translation returned empty string")
    sys.exit(1)
print("  ✅ Translation OK")

# ── STEP 3: TTS ───────────────────────────────────────────────────────────────
print("\n[STEP 3] Loading XTTS model...")
from TTS.api import TTS

tts_api = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
xtts = tts_api.synthesizer.tts_model

latent  = xtts.speaker_manager.speakers["Ana Florence"]["gpt_cond_latent"]
embedding = xtts.speaker_manager.speakers["Ana Florence"]["speaker_embedding"]

print(f"  Synthesising in language: '{tgt_lang}'")
print(f"  Text to speak: '{translated}'")

with torch.no_grad():
    result = xtts.inference(
        text=translated,
        language=tgt_lang,
        gpt_cond_latent=latent,
        speaker_embedding=embedding,
        temperature=0.65,
        top_k=30,
        top_p=0.85,
        repetition_penalty=10.0,
        speed=1.0,
    )

wav = np.array(result["wav"], dtype=np.float32)
print(f"  WAV samples     : {len(wav)}")
print(f"  WAV duration    : {len(wav)/24000:.2f}s")
print(f"  WAV value range : min={wav.min():.4f}  max={wav.max():.4f}")

if len(wav) < 1000:
    print("  ❌ WAV output is too short — TTS likely failed silently")
    sys.exit(1)

if wav.max() < 0.01:
    print("  ❌ WAV values are near zero — audio is silent/noise")
    sys.exit(1)

# write diagnostic output
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagnose_out.wav")
pcm = (wav * 32767).astype(np.int16).tobytes()
buf = io.BytesIO()
with wave.open(buf, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(pcm)
with open(out_path, "wb") as f:
    f.write(buf.getvalue())

print(f"  ✅ TTS OK — output written to: {out_path}")
print("\n✅ All stages passed. If diagnose_out.wav still sounds wrong, the issue is in the audio input quality or language detection.")
