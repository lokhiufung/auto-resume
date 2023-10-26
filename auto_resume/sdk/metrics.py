import re
from collections import Counter


def calculate_keyword_freq_score(text, keywords):
    # Convert the text to lowercase to make the search case-insensitive
    text = text.lower()

    # Initialize a Counter to count the frequency of each keyword
    keyword_counter = Counter()

    # Iterate through the keywords and count their occurrences using regular expressions
    for keyword in keywords:
        pattern = re.compile(r'\b' + re.escape(keyword.lower()) + r'\b')
        matches = pattern.findall(text)
        keyword_counter[keyword] += len(matches)

    return keyword_counter


