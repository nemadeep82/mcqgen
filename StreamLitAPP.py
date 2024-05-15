import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv

from src.mcqgenerator.utils import read_file, get_quiz_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

from langchain.callbacks import get_openai_callback

import streamlit as st

with open("C:\genaipjts\mcqgen\experiment\Response.json","r") as file:
    response_json = json.load(file)

# title of the ap
st.title("MCQ Generator")

# input form
with st.form("user_input_form"):
    file_upload = st.file_uploader("Please upload a PDF or text file") #upload file
    mcq_count = st.number_input("Please enter number of MCQs",min_value=3,max_value=5) #input MCQ number
    subject = st.text_input("Please enter subject",max_chars=50)
    cmplx_level = st.text_input("Enter complexity level",max_chars=50,placeholder="Simple")
    submit_but = st.form_submit_button("Generate MCQ")

    #code handling submit

    if submit_but and file_upload is not None and mcq_count and subject and cmplx_level:
        with st.spinner("loading..."):
            try:
                text = read_file(file_upload)

                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject":subject,
                            "tone": cmplx_level,
                            "response_json": json.dumps(response_json)
                        }
                    )

            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error happened")
            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")

                if isinstance(response,dict):
                    quiz = response.get("quiz",None)

                    if quiz is not None:
                        table_data = get_quiz_data(quiz)
                        
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)
                            st.text_area("Review",response["review"])
                        else:
                            st.error("Error in the table")

                else:
                    st.write(response)
                    









