
from pathlib import Path
from openai import OpenAI
import os
import streamlit as st
from dotenv import load_dotenv
import requests
from PIL import Image
from serpapi import GoogleSearch

st.title("Software Assistant App 🤖")
# Add a description under the title
st.markdown(
    """
    Welcome to the **Ai Assistant** . This magical app is here to assist you with all your software-related quests. 
    Whether you're debugging, learning, or seeking tutorials, our digital wizardry is at your service! 
    Enter the realm of code and commands, and let the enchantment begin! ✨✨✨
    """
)
# Initialize OpenAI Client
#client = OpenAI()
# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Set your SerpApi API key
#api_key = "YOUR_SERPAPI_API_KEY"
# Get the API key from the environment
api_key = os.getenv("YOUR_SERPAPI_API_KEY")

# Function to generate AI response
def generate_ai_response(user_input):
    system_prompt = """
    You are a software expert documentation.
    You'll take the description of the user.
    You will be precise on the user's software input.
    """
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=100,
        temperature=0
    ).choices[0].message.content

# Function to generate logo
def generate_logo(software_name):
    return client.images.generate(
        model="dall-e-2",
        prompt=software_name,
        size="256x256",
        quality="standard",
        n=1
    ).data[0].url

# Function to debugging code
def debugging_explainer(msg1,msg):
    system_prompt2="""
                        Based on the software given by the user,
                        You'll take the description of the user. Troubleshoot the issues.
                        Give example solution step by step in concise and fun way.
                        Make it in bullet points.
                        """
    instruction = """
                        A syntax error occurs when the code does not follow the rules of the Python language. This type of error typically prevents the code from being executed at all.

                        Python
                        print "Hello, World!"
                        Use code with caution. Learn more
                        SyntaxError: Missing parentheses in call to 'print'. Did you mean print("Hello, World!")?
                  """
    sample_answer = """
                        Sure, here is the code to print "Hello, World!" in Python:

                        Python
                        print("Hello, World!")
                        Use code with caution. Learn more
                        This code will print the following output to the console:

                        Hello, World!
                        """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt2},
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": sample_answer},
            {"role": "user", "content": f'{msg1}'f'{msg}'}
        ],
        max_tokens=500,
        temperature=1.3,
    )
    response_prompt = response.choices[0].message.content
    return response_prompt


# Function to generate tutorial explain
def assistant_explainer(msg1,msg):
    system_prompt2="""
                        Based on the software given by the user,
                        You'll take the description of the user.
                        Explain the solution step by step in concise and fun way.
                        You will then explain using a different example to help user to understand better.
                        Make it in bullet points.
                        
                    """
    instruction = """
                        Explain this me?

                        '' 
                        I'd like to create a table using Excel
                        ''

                        """
    sample_answer = """
                        To create a table in Excel, you can follow these steps:

                        1. Select the cell or range of cells that you want to include in the table.

                        2. Click on the “Home” tab in the ribbon.

                        3. Click on the “Format as Table” button.

                        4. Choose a table style from the drop-down menu.

                        5. If the first row of your data contains headers, select the “My table has headers” checkbox.

                        6. Click “OK”
                        """
    s_instruction2 = '''
                        You'll Recommend a tutorial video addressing this issue.
                        '''
    sample_answer2 = '''
                        Here a the video link for further info:
                        
                        https://www.youtube.com/watch?v=iroIA8_3soo
                        '''
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt2},
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": sample_answer},
            {"role": "system", "content": s_instruction2},
            {"role": "assistant", "content": sample_answer2},
            {"role": "user", "content": f'{msg1}'f'{msg}'}
        ],
        max_tokens=500,
        temperature=1.3,
    )
    response_prompt = response.choices[0].message.content
    return response_prompt

#Function to create text-to-speech
def voice_explainer(input_text,output_path):
    #speech_file_path = Path(__file__).parent / output_path #"speech.mp3" 
    # Define File Path
    current_directory = Path.cwd()
    speech_file_path = current_directory / output_path
    
    response1 = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    #input="Today is a wonderful day to build something people love!"
    input=input_text
    )

    voice=response1.stream_to_file(speech_file_path)
    return voice

#Function to translate bahasa
def bahasa_explainer(translate):
    translate_prompt = '''You are the multi language translator.You have many experiences talking with tourist.
    You able to translate any words to bahasa language precisely.'''
    translate_instruction = 'I love you'
    translate_answer = 'Saya sayang kamu'
    translate_response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": translate_prompt},
          {"role": "user", "content": translate_instruction},
          {"role": "assistant", "content": translate_answer},
            {"role": "user", "content": f'{translate}'}
        ],
        max_tokens=500,
        temperature=1,
    )
    trans_response_prompt = translate_response.choices[0].message.content
    return trans_response_prompt

#Function to translate mandarin
def mandarin_explainer(translate):
    translate_prompt = '''You are the multi language translator.You have many experiences talking with tourist.
    You able to translate any words to mandarin language precisely.'''
    translate_instruction = 'I love you'
    translate_answer = '我爱你'
    translate_response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": translate_prompt},
          {"role": "user", "content": translate_instruction},
          {"role": "assistant", "content": translate_answer},
            {"role": "user", "content": f'{translate}'}
        ],
        max_tokens=500,
        temperature=1,
    )
    trans_response_prompt = translate_response.choices[0].message.content
    return trans_response_prompt

#Function to translate tamil
def tamil_explainer(translate):
    translate_prompt = '''You are the multi language translator.You have many experiences talking with tourist.
    You able to translate any words to tamil language precisely.'''
    translate_instruction = 'I love you'
    translate_answer = 'நான் உன்னை காதலிக்கிறேன்'
    translate_response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": translate_prompt},
          {"role": "user", "content": translate_instruction},
          {"role": "assistant", "content": translate_answer},
            {"role": "user", "content": f'{translate}'}
        ],
        max_tokens=500,
        temperature=1,
    )
    trans_response_prompt = translate_response.choices[0].message.content
    return trans_response_prompt

# Streamlit app
user_input_software = st.text_input("Enter the software name: The image created is intended solely for educational purposes")
if st.button("Submit"):
    if user_input_software:
        # Generate AI response and logo
        ai_response = generate_ai_response(user_input_software)
        #software_logo_url = generate_logo(ai_response)

        # Display logo
        #st.image(software_logo_url, caption=f"Logo for {user_input_software}", use_column_width=True)

        # Display AI response
        st.write("AI Response:")
        st.write(ai_response)

        # User input for search query
        params = {
            "q": user_input_software + " logo",  # Append " logo" to the search query
            "api_key": api_key,
            "engine": "google_images",  # Specify Google Images as the search engine
            "num": 1,  # Number of results (in this case, only 1 logo result)
            # Add other parameters as needed
        }

        # Make the API request
        search = GoogleSearch(params)
        results = search.get_dict()

        # Access the logo image result
        logo_results = results.get("images_results", [])

        # Display the logo image in Streamlit
        if logo_results:
            logo_url = logo_results[0].get("original", "")
            st.image(logo_url, caption="Logo Image")
        else:
            st.write("No logo image found.")


st.sidebar.title("Unlock the Functions🧮")

page = st.sidebar.selectbox("Choose a Mode", ["Debugging Mode", "Tutorial Mode", "Learning Mode"])

if page == "Debugging Mode":
    st.subheader("Assistant Explanation:")
    user_input_problem = st.text_area("Enter the problem:")
    if user_input_problem:
        ai_response = generate_ai_response(user_input_software)
        additional_explaination = debugging_explainer(user_input_problem, ai_response)
        st.write(additional_explaination)

elif page == "Tutorial Mode":
    st.subheader('Tutorial Mode')
    user_input_tuto = st.text_input("Enter the problem:")
    if user_input_tuto:
        tuto_explaination = assistant_explainer(user_input_tuto, user_input_software) #ai_response
        st.write(tuto_explaination)

        #Voice Explanation
        voice_output_path = 'test_speech.mp3'
        st.write("Generating voice explanation...")
        voice_explainer(tuto_explaination, voice_output_path)
        st.audio(voice_output_path, format="audio/mp3", start_time=0)

elif page == "Learning Mode":
    st.subheader('Learning Mode')
    # Display a quote
    st.write("Keep learning and never stop exploring the world of possibilities.-SHRDC-")
    if st.button("Generate"):
        #user_input_learn = st.text_input("Enter the problem:")
        #if user_input_learn:
        #learn_explaination = learn_explainer(msg=ai_response)
        #st.write(learn_explaination)
        learn_prompt = '''
        Based on the software given by the user,
        You are the best Software teacher the world even had.
        You will give a random tips of useful tools or advance features of this software.
        Explain the the details in concise and fun way.
        Give one example.
        '''

        learn_intruction = '''
        spreadsheets offer a variety of other useful tools and advance features for data analysis and manipulation. 
        '''

        learn_answer = '''
        1. PivotTables:
        PivotTables are one of the most powerful tools in spreadsheets for summarizing and analyzing large amounts of data.
        They allow you to quickly group, sort, and filter data to identify trends and patterns.

        Here are some of the key features of PivotTables:

        Easy to use: PivotTables can be created with just a few clicks.
        Flexible: You can customize PivotTables to show the data you want to see.
        Powerful: PivotTables can perform complex calculations and analysis.
        '''
        learn_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": learn_prompt},
                {"role": "user", "content": learn_intruction},
                {"role": "assistant", "content": learn_answer},
                {"role": "user", "content": user_input_software}
            ],
            max_tokens=500,
            temperature=1,
        )
        learn_response_prompt = learn_response.choices[0].message.content
        #return learn_response_prompt
        # Display the assistant's response
        st.text("Assistant: " + learn_response_prompt)

        params = {
                "q": learn_response_prompt + 'youtube',
                "api_key": api_key,
                "engine": "google",  # You can change the search engine if needed
                "num": 3,  # Number of results per page
                "hl": "en",  # Language
                # Add other parameters as needed
                }

        # Make the API request
        search = GoogleSearch(params)
        results = search.get_dict()

        # Access the search results
        organic_results = results.get("organic_results", [])

        # Display the results in Streamlit
        #st.subheader(f"YouTube Results for: {learn_response_prompt}")
        st.subheader( "Search Results for:")

        for index, result in enumerate(organic_results, start=1):
            #if "youtube.com" in result.get("link", ""):
                st.write(f"{index}. [{result['title']}]({result['link']})")
                st.write(result["snippet"])
                st.write("---")



page1 = st.sidebar.selectbox("Choose a language", ['Bahasa','Mandarin','Tamil'], key="page_selector")

if page1 == "Bahasa":
    st.subheader("Assistant Translator:")
    user_input_text = st.text_area("Masukkan teks:")
    if user_input_text:
        bahasa_explanation = bahasa_explainer(user_input_text)
        st.write(bahasa_explanation)

elif page1 == "Mandarin":
    st.subheader("Assistant Translator:")
    user_input_text = st.text_area("输入文字:")
    if user_input_text:
        mandarin_explanation = mandarin_explainer(user_input_text)
        st.write(mandarin_explanation)

elif page1 == "Tamil":
    st.subheader("Assistant Translator:")
    user_input_text = st.text_area("உரையை உள்ளிடவும்:")
    if user_input_text:
        tamil_explanation = tamil_explainer(user_input_text)
        st.write(tamil_explanation)

#User feedback of this app
customer_feed = st.sidebar.text_area("Enter the User Feedback/Issue:")
if st.sidebar.button("Send email"):
    st.success("We're committed to providing a great experience for all our users, and your continued support means the world to us.😊")
    # Display confirmation message in the sidebar
    st.sidebar.text("Email sent successfully!")
    st.sidebar.success("Thank you for being a valued user.🙌")
    
    