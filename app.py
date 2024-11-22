import streamlit as st
from langchain_groq import ChatGroq  # Import ChatGroq from langchain_groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser  # Import StrOutputParser

# Load GROQ_API_KEY from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]

# Initialize the ChatGroq model (replace with your actual Groq model)
llm = ChatGroq(groq_api_key=groq_api_key, model="Gemma2-9b-It")

# Prompt Template for Translation
generic_template = "Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages(
    [("system", generic_template), ("user", "{text}")]
)

# Streamlit UI
st.title("Language Translator with ChatGroq")

# Dropdown for selecting language (Added English and Urdu)
language = st.selectbox(
    "Select a language to translate into:",
    ["French", "Spanish", "German", "Chinese", "Italian", "Japanese", "English", "Urdu"]
)

# Initialize the text input and manage its value using session state
if "text_to_translate" not in st.session_state:
    st.session_state.text_to_translate = ""

text_to_translate = st.text_input("Enter text to translate:", value=st.session_state.text_to_translate)

# Variable to hold the translation output
translation = ""

# Translate button
if st.button("Translate"):
    if not text_to_translate.strip():
        st.error("Please enter some text to translate!")
    else:
        try:
            # Generate the formatted prompt as a list of BaseMessages
            formatted_prompt = prompt.format_messages(language=language, text=text_to_translate)
            
            # Use ChatGroq to generate a response
            response = llm.invoke(formatted_prompt)  # Pass formatted_prompt directly
            
            # Access the content from the AIMessage object
            translation = response.content  # Access the 'content' attribute of the AIMessage object
            
            # Display the translation
            st.success(f"Translation in {language}:")
            st.write(translation)

            # Clear the text input by resetting session state
            st.session_state.text_to_translate = ""  # This clears the input field

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display translated text if available
if translation:
    st.text_area("Translation Output", translation, height=150)
