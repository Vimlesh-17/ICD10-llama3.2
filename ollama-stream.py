import streamlit as st
import pandas as pd
import ollama

def generate_response(prompt, model_name):
    """Generate response using Ollama model"""
    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )
        return response['message']['content']
    except Exception as e:
        st.error(f"Error during generation: {str(e)}")
        return "Error generating response. Please try again."

def generate_soap_note(transcript, model_name):
    # Chief Complaint
    ICD_prompt = f"""
    You are a medical coder. Based on the following medical chart, generate the icd10_diag codes in the given format:
    [LIST OF ICD-10 CODES]
   
    Medical Chart:
    {transcript}
    """
   
    # Generate ICD-10 codes from the transcript using the model
    icd10_codes = generate_response(ICD_prompt, model_name)
   
    return icd10_codes

# Streamlit app
st.title("Medical Coding with Ollama")

# Input for the model name
model_name = st.text_input("Enter the model name", value="llama3.2:3b")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file with 'id' and 'text' columns", type="csv")

# Only proceed if file and model name are available
if uploaded_file and model_name:
    try:
        # Read the uploaded CSV file
        transcript_df = pd.read_csv(uploaded_file)
        
        # Check for required columns
        if '_id' not in transcript_df.columns or 'text' not in transcript_df.columns:
            st.error("CSV file must contain '_id' and 'text' columns.")
        else:
            # Display the CSV content
            st.write("Uploaded CSV Data:")
            st.dataframe(transcript_df)

            # Display the button and process data when clicked
            if st.button("Generate Responses"):
                # Process each row in the CSV
                results = []
                for index, row in transcript_df.iterrows():
                    transcript = row['text']  # Get the text for the current row
                    row_id = row['_id']  # Get the id for the current row

                    st.write(f"Processing ID: {row_id}...")

                    # Generate ICD-10 codes for each transcript
                    icd10_codes = generate_soap_note(transcript, model_name)

                    # Display the result
                    st.write(f"ID: {row_id}")
                    st.write("Generated ICD-10 Codes:", icd10_codes)
                    st.write("---")

                    # Append the result to the list for display (optional)
                    results.append({
                        '_id': row_id,
                        'icd10_codes': icd10_codes
                    })

                st.success("Processing completed.")
    except Exception as e:
        st.error(f"Error loading or processing file: {e}")
else:
    # Display information if inputs are missing
    st.info("Please upload a CSV file and enter the model name to begin.")
