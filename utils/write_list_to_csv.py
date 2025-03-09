import os

def write_list_to_file(llm_answers: list[str], file_path: str):
    """
    Writes a list of strings to a specified file, each on a new line.
    Ensures that the directory for the file path exists; creates it if it doesn't.

    :param llm_answers: List of strings to be written to the file.
    :param file_path: Path to the file where the answers will be saved.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as file:
            for answer in llm_answers:
                file.write(answer + '\n')
        print(f"LLM answers have been successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
