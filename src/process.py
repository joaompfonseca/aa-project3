import utils as u


def process_file(file_path, stop_words_path, punctuations_path):
    # 1. Remove file header and footer, and make lines uppercase
    # Result: list of lines of content

    # First pass to find content start and end
    start = 0
    end = 0
    with open(file_path, "r") as file:
        for i, line in enumerate(file):
            if line.strip().startswith("***"):
                start = end
                end = i

    # Second pass to extract content lines
    lines = []
    with open(file_path, "r") as file:
        for line in file.readlines()[start + 1 : end]:
            line = line.strip()  # Remove leading and trailing whitespaces
            line = line.upper()  # Convert to upper case
            if line:  # Skip empty lines
                lines.append(line)

    # 2. Remove stop-words, punctuation and numbers
    # Result: list of words

    stop_words = set()
    with open(stop_words_path, "r") as file:
        for line in file:
            word = line.strip()  # Remove leading and trailing whitespaces
            word = line.upper()  # Convert to upper case
            if word:  # Skip empty lines
                stop_words.add(word)
    punctuations = set()
    with open(punctuations_path, "r") as file:
        for line in file:
            punctuation = line.strip()  # Remove leading and trailing whitespaces
            if punctuation:  # Skip empty lines
                punctuations.add(punctuation)
    numbers = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

    words = []
    for line in lines:
        for word in line.split():
            # Skip stop words
            if word in stop_words:
                continue
            for letter in word:
                # Remove punctuation and numbers
                if letter in punctuations or letter in numbers:
                    word = word.replace(letter, "")
            if word:
                words.append(word)

    # 3. Join all words to form a single string

    return "".join(words)


if __name__ == "__main__":
    # Stop words
    stop_words_path = "../stop_words.txt"

    # Punctuations
    punctuations_path = "../punctuations.txt"

    # 1. Othello
    othello_raw_path = "../documents/raw/othello/"
    othello_proc_path = "../documents/proc/othello/"
    othello_files = {
        "en": "pg1793.txt",
        "de": "pg7185.txt",
        "fi": "pg17529.txt",
        "fr": "pg18179.txt",
        "pt": "pg28526.txt",
    }

    for file in othello_files.values():
        data = process_file(
            f"{othello_raw_path}{file}", stop_words_path, punctuations_path
        )
        u.write_file(f"{othello_proc_path}{file}", data)
