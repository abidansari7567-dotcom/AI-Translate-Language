import streamlit as st
from mtranslate import translate
import pandas as pd
import os
from gtts import gTTS
import base64

# ------------------ Page Config ------------------
st.set_page_config(page_title="AI Language Translator", layout="centered")

# ------------------ Load Language Dataset ------------------
df = pd.read_csv("language.csv")
df.dropna(inplace=True)

lang = df['name'].to_list()
langlist = tuple(lang)
langcode = df['iso'].to_list()

# language : code dictionary
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}

# ------------------ Session State ------------------
if "lang_choice" not in st.session_state:
    st.session_state.lang_choice = langlist[0]


# ------------------ Main UI ------------------
st.title("🌍 AI Language Translator")

inputtext = st.text_area(
    "Enter text to translate",
    height=120,
    placeholder="Type something here..."
)

# Center language dropdown
st.markdown("### Select Target Language")

c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.session_state.lang_choice = st.selectbox(
        "",
        langlist,
        index=langlist.index(st.session_state.lang_choice)
    )

choice = st.session_state.lang_choice

# ------------------ Speech Supported Languages ------------------
speech_langs = {
    "Afrikaans":"af",
    "Arabic":"ar",
    "Bengali":"bn",
    "Bulgarian":"bg",
    "Catalan":"ca",
    "Czech":"cs",
    "Danish":"da",
    "German":"de",
    "Greek":"el",
    "English":"en",
    "Esperanto":"eo",
    "Spanish":"es",
    "French":"fr",
    "Hindi":"hi",
    "Italian":"it",
    "Japanese":"ja",
    "Kannada":"kn",
    "Korean":"ko",
    "Marathi":"mr",
    "Malayalam":"ml",
    "Nepali":"ne",
    "Odia":"or",
    "Punjabi":"pa",
    "Russian":"ru",
    "Tamil":"ta",
    "Telugu":"te",
    "Thai":"th",
    "Urdu":"ur"
}

# ------------------ Audio Download Function ------------------
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">Download {file_label}</a>'
    return href

# ------------------ Translation Output ------------------
if len(inputtext) > 0:
    try:
        output = translate(inputtext, lang_array[choice])

        col1, col2 = st.columns([4,3])

        with col1:
            st.text_area("Translated Text", output, height=200)

        # Audio Support
        if choice in speech_langs:
            with col2:
                tts = gTTS(text=output, lang=speech_langs[choice], slow=False)
                tts.save("audio.mp3")

                audio_file = open("audio.mp3", "rb")
                audio_bytes = audio_file.read()

                st.audio(audio_bytes, format="audio/mp3")
                st.markdown(
                    get_binary_file_downloader_html("audio.mp3", "Audio File"),
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(e)