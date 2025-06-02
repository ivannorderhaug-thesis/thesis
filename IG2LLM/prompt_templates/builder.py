from langchain.prompts import PromptTemplate

def build_prompt_template(with_examples=False) -> PromptTemplate:
    """
    Build a prompt template for generating statements.
    Args:
        with_examples (bool): Whether to include examples in the prompt.
        Returns:
            PromptTemplate: A LangChain PromptTemplate object.
    """
    input_variables = ["statement_type", "statement_information", "definitions", "guidelines"]
    
    with open("prompts/base_template.txt", "r") as file:
        template = file.read()

    if with_examples:
        input_variables.append("examples")
        template += "\n### Examples\n{examples}"

    return PromptTemplate(
        template=template,
        input_variables=input_variables,
    )

