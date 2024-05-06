import assemblyai as aai
import streamlit as st
import sys
import urllib.parse
import requests
import importlib.metadata

# st.set_page_config(page_title="Darwin&Verne Audio Transcriber", max_upload_size=500)

# Speaker colors
speaker_colors = {
    "Speaker A": "#FF5733",
    "Speaker B": "#33C4FF",
    "Speaker C": "#8EFF33",
    "Speaker D": "#FF33E6",
    "Speaker E": "#FFD933",
    "Speaker F": "#33FFC4",
    "Speaker G": "#336BFF",
    "Speaker H": "#FF336B",
    "Speaker I": "#33FF33",
    "Speaker J": "#FF3333",
    "Speaker K": "#3333FF",
    "Speaker L": "#FF33C4",
    "Speaker M": "#33FF33",
    "Speaker N": "#FF33FF",
    "Speaker O": "#33C4FF",
    "Speaker P": "#FF5733",
    "Speaker Q": "#33C4FF",
    "Speaker R": "#8EFF33",
    "Speaker S": "#FF33E6",
    "Speaker T": "#FFD933",
    "Speaker U": "#33FFC4",
}

def transcribe_audio(audio_file):
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        language_code='es',
        disfluencies=False,
    )

    transcriber = aai.Transcriber()
    # Save temporary audio file if uploaded
    if audio_file is not None:
        with open(audio_file.name, "wb") as f:
            f.write(audio_file.getbuffer())
        transcript = transcriber.transcribe(audio_file.name, config)
        return transcript

def main():
    aai.settings.api_key = st.secrets["assembly_api_key"]

    st.title("Darwin&Verne Audio Transcriber")
    audio_file = st.file_uploader("Desplaza tus archivos de audio aquí:", type=['mp3'])

    col1, col2 = st.columns(2)

    with col1:
      transcribe_button = st.button("Transcribir")

    transcript = None
    if transcribe_button and audio_file:
      try:
          with st.spinner("Transcribiendo audio..."):
              transcript = transcribe_audio(audio_file)
              st.write("Resultado de la transcripción:")
              full_text = ""
              for utterance in transcript.utterances:
                  speaker_text = f"Speaker {utterance.speaker}: {utterance.text}\n\n"
                  full_text += speaker_text

                  speaker_label = f"Speaker {utterance.speaker}"
                  color = speaker_colors.get(speaker_label, "#000000")  # Default color
                  st.markdown(f'<span style="color:{color};">**{speaker_label}:**</span> {utterance.text}', unsafe_allow_html=True)

      except Exception as e:
          st.error(f"Hubo un error: {e}")

    if transcript:
      with col2:
          st.download_button(
              label="Download Transcript",
              data=full_text,
              file_name=f"{audio_file.name}_transcript.txt",
              mime="text/plain"
          )


if __name__ == "__main__":
    main()
