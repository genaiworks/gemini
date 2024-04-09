import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """ You are Youtube video summarizer.  
You will bt taking the transcript test and summarizing the entire video and providing 
the important summary in points within 250 words.  Please provide the summary of text here: """



#getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id=video_id)
        print(transcript_text)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        print(transcript)
        return transcript
        
    except Exception as e:
        raise e

#summary from prompt
def generate_gemini_content(transcript,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript)
    return response.text

st.title("Youtube transcript to detailed notes converter")
youtube_link = st.text_input("Enter Youtube Video Link")
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
if st.button("Get Detailed Notes"):
    transcript_text =  extract_transcript_details(youtube_link) 
    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt) 
        st.markdown("### Detail Notes ")
        st.write(summary)





