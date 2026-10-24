
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


# =========================================================
# LOAD VOICE ENCODER
# =========================================================

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


# =========================================================
# GENERATE VOICE EMBEDDING
# =========================================================

def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True,
        )

        if len(audio) == 0:
            st.error("Audio is empty. Please record again.")
            return None

        wav = preprocess_wav(audio, source_sr=sr)
        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()

    except Exception as e:
        st.error(f"Voice recognition error: {e}")
        return None


# =========================================================
# IDENTIFY SPEAKER
# =========================================================

def identify_speaker(
    new_embedding,
    candidates_dict,
    threshold=0.65,
):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    new_embedding = np.asarray(
        new_embedding,
        dtype=np.float32,
    ).reshape(-1)

    new_norm = np.linalg.norm(new_embedding)

    if new_norm == 0:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding is None:
            continue

        try:
            stored_embedding = np.asarray(
                stored_embedding,
                dtype=np.float32,
            ).reshape(-1)

            if stored_embedding.shape != new_embedding.shape:
                continue

            stored_norm = np.linalg.norm(stored_embedding)

            if stored_norm == 0:
                continue

            similarity = float(
                np.dot(new_embedding, stored_embedding)
                / (new_norm * stored_norm)
            )

            if similarity > best_score:
                best_score = similarity
                best_sid = sid

        except (TypeError, ValueError):
            continue

    if best_sid is not None and best_score >= threshold:
        return best_sid, best_score

    return None, max(best_score, 0.0)


# =========================================================
# PROCESS BULK AUDIO
# =========================================================

def process_bulk_audio(
    audio_bytes,
    candidates_dict,
    threshold=0.65,
):
    try:
        if not audio_bytes:
            st.warning("Please provide an audio recording.")
            return {}

        if not candidates_dict:
            st.warning("No registered voice profiles found.")
            return {}

        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True,
        )

        if len(audio) == 0:
            st.warning("No audio detected. Please record again.")
            return {}

        # Detect non-silent segments
        segments = librosa.effects.split(
            audio,
            top_db=30,
        )

        identified_results = {}

        for start, end in segments:
            # Ignore segments shorter than 0.5 seconds
            if (end - start) < int(sr * 0.5):
                continue

            segment_audio = audio[start:end]

            wav = preprocess_wav(
                segment_audio,
                source_sr=sr,
            )

            if len(wav) == 0:
                continue

            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(
                embedding,
                candidates_dict,
                threshold=threshold,
            )

            if sid is not None:
                if (
                    sid not in identified_results
                    or score > identified_results[sid]
                ):
                    identified_results[sid] = score

        return identified_results

    except Exception as e:
        st.error(f"Bulk audio processing failed: {e}")
        return {}
