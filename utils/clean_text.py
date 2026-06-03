import re

def clean_text(text):

    text=re.sub(r'Volume:.*?Page \d+', '', text)
    text=re.sub(r'www\..*?\n', '', text)
    text=re.sub(r'© 2023.*?\n', '', text)
    text = re.sub(r'REFERENCES.*', '', text, flags=re.DOTALL)
    return text