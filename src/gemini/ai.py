
def words_related_to_theme(theme: str) -> str:
    words_in_array_form = ["python", "java", "kotlin", "script"]

    return format_word_array(words_in_array_form)

def format_word_array(words: list) -> str:
    return ", ".join(words).lower()