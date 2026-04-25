import io
import os
import re
import wave
from collections.abc import Generator
import numpy as np
import torch
from TTS.api import TTS

torch.set_num_threads(12)
torch.set_num_interop_threads(6)
torch.backends.mkldnn.enabled = True

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
model = tts.synthesizer.tts_model
LANGUAGE = "en"
SAMPLE_RATE = 24000
LATENT = model.speaker_manager.speakers["Ana Florence"]["gpt_cond_latent"]
EMBEDDING = model.speaker_manager.speakers["Ana Florence"]["speaker_embedding"]
_INFER_PARAMS = dict(
    language=LANGUAGE,
    gpt_cond_latent=LATENT,
    speaker_embedding=EMBEDDING,
    temperature=0.65,
    top_k=3,
    top_p=0.85,
    repetition_penalty=10.0,
    speed=1.0,
)

with torch.no_grad():
    model.inference(text="Hello.", **_INFER_PARAMS)

def _infer(text: str) -> np.ndarray:
    with torch.no_grad():
        result = model.inference(text=text, **_INFER_PARAMS)
    return np.array(result["wav"], dtype=np.float32)

def _to_pcm(samples: np.ndarray) -> bytes:
    return (samples * 32767).astype(np.int16).tobytes()

def _to_wav_bytes(pcm: bytes) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)
    return buf.getvalue()

def _split_chunks(text: str, min_words: int = 15, max_words: int = 20) -> list[str]:
    words = text.split()
    chunks, current = [], []
    for word in words:
        current.append(word)
        at_boundary = re.search(r"[.!?]$", word)
        if at_boundary and len(current) >= min_words or len(current) >= max_words:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks

def speak(text: str) -> bytes:
    chunks = _split_chunks(text)
    samples = np.concatenate([_infer(c) for c in chunks])
    return _to_pcm(samples)

def speak_stream(text: str) -> Generator[bytes, None, None]:
    for chunk in _split_chunks(text):
        yield _to_pcm(_infer(chunk))

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def speak_to_file(text: str, path: str) -> str:
    safe_path = os.path.abspath(path)
    if not safe_path.startswith(BASE_DIR + os.sep):
        raise ValueError(f"Path '{path}' is outside the allowed directory.")
    if not safe_path.endswith(".wav"):
        raise ValueError("Output file must have a .wav extension.")
    all_pcm = b"".join(speak_stream(text))
    with open(safe_path, "wb") as f:
        f.write(_to_wav_bytes(all_pcm))
    return safe_path

def speak_sentences(text: str) -> list[bytes]:
    return [_to_pcm(_infer(c)) for c in _split_chunks(text)]