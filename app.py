import streamlit as st
import google.generativeai as genai

# Configure the API with your API Key
genai.configure(api_key="")

# Define the system prompt
sys_prompt = """You are a helpful AI Code Reviewer for Python.
                Users will submit their Python code for review and receive feedback on potential bugs along with suggestions for fixes.
                You should be user-friendly, efficient, and provide accurate bug reports and fixed code snippets.
                You are expected to reply in as much detail as possible in easy words.
                Make sure to take example while explaining a concept.

                The response should follow the below conditions.
                1. Response should start with a Big and bold font that says "Code Review".
                2. Then a brief report of the bug in the code, with the headline "Bug Report" (without asterisks or unnecessary symbols) and start with the sentence "The bugs in the code are:".
                3. After the bug report, a snippet of the correct code should be given as a response with the header "Fixed Code". The fixed code snippet should be inside a box with proper coding structure (no extra characters, only the fixed code).
                
                In case a user asks any question outside the Python code scope,
                politely decline the request and tell them to ask the question from the Python code domain only."""

# Initialize the generative model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash", system_instruction=sys_prompt)

# Streamlit UI Setup
st.title("Faizan's AI Code Reviewer")
st.markdown("<small>Powered by Gemini</small>", unsafe_allow_html=True)  # Subline with small fonts
st.subheader("Enter your Python code for review:")

# Code input area
user_code = st.text_area("Enter you Python code here....", height=200)

# Generate button
if st.button("Generate Review"):
    if user_code.strip():
        with st.spinner("Reviewing your code..."):
            try:
                # Generate the response using the Gemini model
                response = model.generate_content(user_code)

                # Display the response
                st.markdown("## Code Review")
                
                # Parse the response text to extract Bug Report and Fixed Code
                response_text = response.text

                # Extract the Bug Report
                if "Bug Report" in response_text:
                    bug_report = response_text.split("Bug Report")[1].split("Fixed Code")[0].strip()
                    st.markdown("### Bug Report")
                    st.write(bug_report)

                # Extract the Fixed Code
                if "Fixed Code" in response_text:
                    fixed_code = response_text.split("Fixed Code")[1].strip()

                    # Remove any unwanted formatting like ```python from the fixed code
                    fixed_code_cleaned = fixed_code.replace("```", "").replace("python", "").strip()

                    st.markdown("### Fixed Code")
                    st.code(fixed_code_cleaned)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter some Python code!")
