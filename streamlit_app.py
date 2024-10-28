import streamlit as st
from copilot import Copilot
import os
### set openai key, first check if it is in environment variable, if not, check if it is in streamlit secrets, if not, raise error

import streamlit as st
from PIL import Image

# Load and display the Columbia GSAS logo
logo_path = "columbia_gsas_logo.png"  # Ensure this matches the actual path to your logo image

try:
    logo_image = Image.open(logo_path)
    st.image(logo_image, caption="Columbia University Graduate School of Arts and Sciences", use_column_width=True)
except FileNotFoundError:
    st.error("Logo image not found. Please ensure the file is in the correct directory.")

st.title("Chat with GSAS Copilot")
st.write(
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key: ### get openai key from user input
    openai_api_key = st.text_input("Please enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    if "messages" not in st.session_state.keys():  # Initialize the chat messages history
        st.session_state.messages = [
            {"role": "assistant", "content": "I am GSAS Copilot, your personal assistant. You can ask me about Columbia University."}
        ]

    @st.cache_resource
    def load_copilot():
        return Copilot()



    if "chat_copilot" not in st.session_state.keys():  # Initialize the chat engine
        st.session_state.chat_copilot = load_copilot()

    if prompt := st.chat_input(
        "Ask a question"
    ):  # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:  # Write message history to UI
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):

            retrived_info, answer = st.session_state.chat_copilot.ask(prompt, messages=st.session_state.messages[:-1], openai_key=openai_api_key)
            ### answer can be a generator or a string

            #print(retrived_info)
            if isinstance(answer, str):
                st.write(answer)
            else:
                ### write stream answer to UI
                def generate():
                    for chunk in answer:
                        content = chunk.choices[0].delta.content
                        if content:
                            yield content
                answer = st.write_stream(generate())

            st.session_state.messages.append({"role": "assistant", "content": answer})

import datetime

# Display today's date
today_date = datetime.date.today()
st.write(f"Today's date: {today_date.strftime('%B %d, %Y')}")

import datetime
import pytz

# Define the time zone for New York
ny_timezone = pytz.timezone('America/New_York')

# Get the current time in New York
ny_time = datetime.datetime.now(ny_timezone).strftime("%I:%M:%S %p")

# Display the current time in New York
st.write(f"Current time in New York: {ny_time}")

import streamlit as st
from PIL import Image

# Load and display the Columbia University map
map_path = "map.png"  # Make sure map.png is in the same directory as this script or provide the correct path

try:
    map_image = Image.open(map_path)
    st.image(map_image, caption="Columbia University Campus Map", use_column_width=True)
except FileNotFoundError:
    st.error("Map image not found. Please ensure the file path is correct.")
    
# Embed the New York weather widget
widget_code = """
<!-- Weather Widget BEGIN -->
<a class="weatherwidget-io" href="https://forecast7.com/en/40d71n74d01/new-york/" data-label_1="NEW YORK" data-label_2="WEATHER" data-theme="original" >New York Weather</a>
<script>
!function(d,s,id){
    var js,fjs=d.getElementsByTagName(s)[0];
    if(!d.getElementById(id)){
        js=d.createElement(s);
        js.id=id;
        js.src='https://weatherwidget.io/js/widget.min.js';
        fjs.parentNode.insertBefore(js,fjs);
    }
}(document,'script','weatherwidget-io-js');
</script>
<!-- Weather Widget END -->
"""

# Display the widget in Streamlit
st.components.v1.html(widget_code, height=250)
