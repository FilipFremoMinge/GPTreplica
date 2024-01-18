def prompt_chatbot(specific_paragraph: int = ""):
    prompt_path = "prompt.txt"

    with open(prompt_path, "r") as file:
        full_prompt = file.read()
        paragraphs = full_prompt.split("\n\n")

    if specific_paragraph == "":
        return paragraphs

    elif specific_paragraph > len(paragraphs):
        return paragraphs

    else:
        return paragraphs[specific_paragraph]
