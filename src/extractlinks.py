import re

def extract_markdown_images(text):

    if not isinstance(text, str):
        raise ValueError("text must be a string")
    
    return re.findall(r"!\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(((?:\\[\(\)]|[^\(\)])*)\)", text)

def extract_markdown_links(text):
    
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    return re.findall(r"\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(((?:\\[\(\)]|[^\(\)])*)\)", text) 
