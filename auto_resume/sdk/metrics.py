import re
from collections import Counter

from langchain.evaluation import load_evaluator
from langchain_core.embeddings import Embeddings


def get_keyword_score(text, keywords):
    score = 0
    # Convert the text to lowercase to make the search case-insensitive
    text = text.lower()

    # # Initialize a Counter to count the frequency of each keyword
    # keyword_counter = Counter()

    # Iterate through the keywords and count their occurrences using regular expressions
    for keyword in keywords:
        pattern = re.compile(r'\b' + re.escape(keyword.lower()) + r'\b')
        matches = pattern.findall(text)
        # keyword_counter[keyword] += len(matches)
        score += len(matches)
    return score


def get_similarity_score(text, requirement_text, embedding_model: Embeddings) -> float:
    # embedding_model is a sentence embedding model
    # calcualate the similarity score using cosine similarity between text and requirement_text
    # 0 is identical, 1 is no correlation, 2 is completely different
    evaluator = load_evaluator('pairwise_embedding_distance', embedding_model=embedding_model)
    score = evaluator.evaluate_string_pairs(prediction=text, prediction_b=requirement_text)
    return score['score']


