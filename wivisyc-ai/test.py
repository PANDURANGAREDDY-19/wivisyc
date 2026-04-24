# basic STT + translation pipeline
# using faster-whisper + helsinki models

from faster_whisper import WhisperModel
from transformers import MarianMTModel, MarianTokenizer


print("loading models... this may take some time")

# load whisper (tiny for speed)
stt_model = WhisperModel("tiny", device="cpu", compute_type="int8")

# load translation models
en_es_name = "Helsinki-NLP/opus-mt-en-es"
es_en_name = "Helsinki-NLP/opus-mt-es-en"

en_es_tokenizer = MarianTokenizer.from_pretrained(en_es_name)
en_es_model = MarianMTModel.from_pretrained(en_es_name)

es_en_tokenizer = MarianTokenizer.from_pretrained(es_en_name)
es_en_model = MarianMTModel.from_pretrained(es_en_name)


# -----------------------------
# function to convert speech → text
# -----------------------------
def get_text_from_audio(audio_path):
    segments, info = stt_model.transcribe(audio_path, beam_size=1)

    full_text = ""
    for seg in segments:
        full_text += seg.text

    return full_text.strip(), info.language


# -----------------------------
# translation helpers
# -----------------------------
def en_to_es(text):
    tokens = en_es_tokenizer(text, return_tensors="pt", padding=True)
    out = en_es_model.generate(**tokens)
    return en_es_tokenizer.decode(out[0], skip_special_tokens=True)


def es_to_en(text):
    tokens = es_en_tokenizer(text, return_tensors="pt", padding=True)
    out = es_en_model.generate(**tokens)
    return es_en_tokenizer.decode(out[0], skip_special_tokens=True)


# -----------------------------
# main logic
# -----------------------------
def run_pipeline(audio_file):

    print("\nprocessing:", audio_file)

    text, lang = get_text_from_audio(audio_file)

    print("\n--- raw text ---")
    print(text)
    print("detected language:", lang)

    # decide translation direction
    if lang == "en":
        translated = en_to_es(text)
        print("\ntranslated (EN -> ES):")
        print(translated)

    elif lang == "es":
        translated = es_to_en(text)
        print("\ntranslated (ES -> EN):")
        print(translated)

    else:
        print("\nskipping translation (unsupported language)")


# -----------------------------
# run
# -----------------------------
if __name__ == "__main__":

    # change this file
    audio_path = "audio.wav"

    run_pipeline(audio_path)