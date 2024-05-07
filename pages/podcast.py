import streamlit as st
import json
import os
from dotenv import load_dotenv
load_dotenv()



def show_podcast():

    st.set_page_config(page_title="Personalized Podcat", page_icon="🎧")

    st.title("Podcast")

    audio_file = os.getenv("AZURE_BLOB")
    # print(audio_file)
    st.audio(audio_file, format="audio/mp4", start_time=0, sample_rate=None, end_time=None, loop=False, autoplay=False)

    st.header("Powering the Future: Responsible AI and Malaysia's Tech Boom")
    st.write("Host: Gino.ai")
    st.write(f"Generated Time: May 6, 2024 08:50 pm")

    with open('files/audio_transcript.json', 'r') as file:
        text = json.load(file)
        st.write(text['transcript'])
        

    st.subheader("Source")
    st.markdown("1. [What is Responsible AI?](https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai?view=azureml-api-2)")
    st.markdown("2. [Microsoft Will Invest $2.2 Billion in Cloud and AI Services in Malaysia](https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai?view=azureml-api-2)")


if __name__ == "__main__":
    show_podcast()