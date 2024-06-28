import streamlit as st
from gtts import gTTS #google text to speech 

from workflow_text_to_text import generate_story_from_text
from workflow_image_to_text import generate_image_caption, generate_story_from_image_caption #generate caption

@st.cache_data(persist=True) #detocarator catch function output, true-cache remains even if app closes (performance, memory restore)
def generate_audio_from_story(text): #func convert text input into audio using GTTS 
    speech = gTTS(text=text, lang='en', slow=False)
    speech.save("story.mp3")
    return "story.mp3"

st.set_page_config( #set streamlit page configeration 
    page_title="AI Story Generator", layout="wide", page_icon="📖"
)

st.sidebar.markdown("### Select the genre/theme of the story:") 
#sidebar for genre
story_theme = st.sidebar.radio("Genre", ("Horror :ghost:", "Action :man-running:", "Romance :heart:", "Comedy :laughing:", "Historical :hourglass_flowing_sand:", "Science Fiction :rocket:"))
#radio button to select 
selected_theme = story_theme.split(":")[0].strip()
#extract selected theme from radio button into substring(text without emoji)

theme_based_prompts = { #dictionary assigns genre a start for generating story 
    "Horror": "Write a horror story using:",
    "Action": "Write a story with lots of action using: ",
    "Romance": "Write a romantic story using: ",
    "Comedy": "Write a funny story using: ",
    "Historical": "Write a story based on a historical event with the help of the input: ",
    "Science Fiction": "Write a science fiction story using: "
}

st.markdown("# KATHASANGAM :closed_book:") # used to give title "#" for TITLE
st.markdown("## Stories by Purvika and Subhangi :book:") #give the subtitle as used "##"

with st.expander("About this app :bulb:", expanded=False): #creates an expander 
    st.markdown("#### This app uses the **Clarifai AI** engine to generate stories based on the input you provide using **LLM** models. You can either upload an image or enter some text to get started. The app will then generate a story based on the input you provide. The story will be generated using the theme you choose, you can select the theme from the sidebar. The app will also generate an **audio file** of the story for you to listen to. You can **download the story as a text file or an audio file (audio from the three-dot menu)**.")
    #to provide text inside the expander in heading as used "####"
st.markdown("## Choose the input type for generating the story")

input_type = st.radio("Input type", ("Text :pencil:", "Image :camera:")) #radio button for input type selection

st.write("*You can also find the story **audio output** below the story*") #to write normal text with no formatting (like italic, bold)

if input_type == "Text :pencil:": #if text input

    st.markdown("### Enter the sentences you want to have your story revolve around: ")

    input_text = st.text_area("Enter the text here", height=100, value="As the rain poured down on a quiet, dimly lit street, I found myself standing in front of a quaint bookstore")
    #user to input text 
    theme_based_input = theme_based_prompts[selected_theme] + " " + input_text
    #concatination of the theme and input prompt
    if st.button("Generate story"): 
        with st.status("Generating story...", expanded=True) as status_text:

            st.write("Fusing your story elements together...")
            st.write("This may take about 30-40 seconds (more if runnung the first time), please hang tight...")

            story = generate_story_from_text(theme_based_input)

            status_text.update(label="Story created!")
        
        st.markdown("### Your Story based on your input!")
        st.download_button('Download story as text file', story, 'story.txt')

        story_lines = story.split('\n')
        formatted_story = "\n".join(["##### " + line for line in story_lines])
        
        with st.expander("View story", expanded=True):
            st.markdown(formatted_story)
        
        with st.status("Generating audio...", expanded=True) as status_audio:

            st.write("Generating your audio file...")
            st.write("This may take about 10-20 seconds")

            generate_audio_from_story(story)
            
            status_audio.update(label="Audio generated...")
        
        st.audio("story.mp3")
        # Create download button for the audio file
        with open("story.mp3", "rb") as f:
            audio_bytes = f.read()
        
        st.download_button('Download story as audio file', audio_bytes, 'story.mp3')



if input_type == "Image :camera:":

    st.markdown("### Upload the image you want your story to be based on:")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    if uploaded_file is not None:

        st.image(uploaded_file, caption="Uploaded Image", use_column_width=False, width=500)   

        if st.button("Generate story"):
            with st.status("Generating story...", expanded=True) as status_text:

                st.write("Fusing your photo elements together to create a story...")
                st.write("This may take about 30-40 seconds (more if runnung the first time), please hang tight...")

                # make uploaded_file into a file-like object
                file_bytes = uploaded_file.read()

                caption = generate_image_caption(file_bytes)
                theme_based_input = theme_based_prompts[selected_theme] + " " + caption

                story = generate_story_from_image_caption(theme_based_input)

                status_text.update(label="Story created!")
            
            st.markdown("### Your Story based on the image!")
            st.download_button('Download story as text file', story, 'story.txt')

            story_lines = story.split('\n')
            formatted_story = "\n".join(["##### " + line for line in story_lines])
            
            with st.expander("View story", expanded=True):
                st.markdown(formatted_story)
            
            with st.status("Generating audio...", expanded=True) as status_audio:

                st.write("Generating your audio file...")
                st.write("This may take about 10-20 seconds")

                generate_audio_from_story(story)
                
                status_audio.update(label="Audio generated...")
            
            st.audio("story.mp3")
            # Create download button for the audio file
            with open("story.mp3", "rb") as f:
                audio_bytes = f.read()
            
            st.download_button('Download story as audio file', audio_bytes, 'story.mp3')