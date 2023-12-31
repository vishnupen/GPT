"""
This file implements prompt template for llama based models. 
Modify the prompt template based on the model you select. 
This seems to have significant impact on the output of the LLM.
"""

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# this is specific to Llama-2.

# system_prompt = """You are a helpful assistant, you will use the provided context to answer user questions.
# Read the given context before answering questions and think step by step. If you can not answer a user question based on 
# the provided context, inform the user. Do not use any other information for answering user. The answers must be completely
# dependant on the document provided."""

system_prompt = """
You are a versatile helpful assistant capable of extracting various details based on user requests.
Generate a JSON representation containing the relevant data points based on the user's query.
Ensure the JSON structure is dynamic, adapting to the actual data available in the context.
Output/answer by deafult must always be printed in json format specified irrespective of whether it is specified in query or not.

Output format: JSON
{{
  "answer": {{
    "message": "No relevant information found.",
    "details": null
  }},
  "confidence": 0.95
}}
"""

# system_prompt = """
# Demonstrate your ability to intelligently infer the following details from document and provide the output in JSON format:
 
# {{
#   "RenterNames": null,        // Extract if Name of consultant or consultant name or name of person given in file or name of the render else None.
#   "Address": null,            // Extract if address given in the file else none.
#   "LeaseStartDate": null,     // Extract if lease start date in the file else None.
#   "LeaseEndDate": null,       // Extract if lease end date in the file else None
#   "MonthlyRentCost": null,    // Extract if rent cost in the file monthly based. if has multiple value then create array and add that in that array.
#   "MoveOutDate": null         // Extract if move out date in the file else None.
# }}
 
# Your task is to showcase an automated system that can make educated guesses and extract these details from documents. 

# Ensure that your system is capable of handling various document formats and structures . Provide the extracted information in the specified JSON format.

# Test your system with a sample document to showcase its ability to make educated guesses and infer the required details, setting values to `None` when information is missing.
# """


def get_prompt_template(system_prompt=system_prompt, promptTemplate_type=None, history=False):
    if promptTemplate_type == "llama":
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
        if history:
            instruction = """
            Context: {history} \n {context}
            User: {question}"""

            prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            instruction = """
            Context: {context}
            User: {question}"""

            prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    elif promptTemplate_type == "mistral":
        B_INST, E_INST = "<s>[INST] ", " [/INST]"
        if history:
            prompt_template = (
                B_INST
                + system_prompt
                + """
    
            Context: {history} \n {context}
            User: {question}"""
                + E_INST
            )
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            prompt_template = (
                B_INST
                + system_prompt
                + """
            
            Context: {context}
            User: {question}"""
                + E_INST
            )
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    else:
        # change this based on the model you have selected.
        if history:
            prompt_template = (
                system_prompt
                + """
    
            Context: {history} \n {context}
            User: {question}
            Answer:"""
            )
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            prompt_template = (
                system_prompt
                + """
            
            Context: {context}
            User: {question}
            Answer:"""
            )
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

    memory = ConversationBufferMemory(input_key="question", memory_key="history")

    return (
        prompt,
        memory,
    )
