import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""

            for page in pdf_reader.pages:
                text += page.extract_text()
            
            return text
        except Exception as e:
            raise Exception("Error reading file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception("unsupported file type")


def get_quiz_data(quiz_str):
    try:
        quiz_str_dict = json.loads(quiz_str)
        quiz_mcq_list = []

        #iterate through the quiz json
        for key,value in quiz_str_dict.items():
            mcq = value["mcq"]
            correctval = value["correct"]
            optionvals = " || ".join(
                [
                f"{option} -> {option_val}" for option, option_val in value["options"].items()
                ]
            )    

            quiz_mcq_list.append({"MCQ":mcq,"Correct":correctval,"Choices":optionvals})

        return quiz_mcq_list

    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False