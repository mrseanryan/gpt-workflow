def write_text_to_file(text, filepath):
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(text)
