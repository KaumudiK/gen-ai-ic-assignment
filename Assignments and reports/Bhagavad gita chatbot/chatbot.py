import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Chatbot:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.questions = [item["question"] for item in knowledge_base]
        self.answers = [item["answer"] for item in knowledge_base]

        # Turn every known question into a numerical vector
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            lowercase=True,
            ngram_range=(1, 2)
        )
        self.question_vectors = self.vectorizer.fit_transform(self.questions)

    def clean_input(self, text):
        # Lowercase and strip punctuation
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def get_response(self, user_input, threshold=0.2):
        cleaned = self.clean_input(user_input)
        if not cleaned:
            return "Could you please type your question again?"

        # Convert the user's input into the same kind of vector
        user_vector = self.vectorizer.transform([cleaned])

        # Compare against every known question
        similarities = cosine_similarity(user_vector, self.question_vectors).flatten()

        best_idx = similarities.argmax()
        best_score = similarities[best_idx]

        # If nothing matches well enough, politely admit it
        if best_score < threshold:
            return ("I'm not sure I understood that. I can help with topics from the "
                    "Bhagavad Gita — its teachings, characters, chapters, and how its "
                    "wisdom applies to daily life. Could you rephrase your question?")

        return self.answers[best_idx]
