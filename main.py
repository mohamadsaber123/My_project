import csv
import numpy as np
from sentence_transformers import SentenceTransformer
from numpy.linalg import norm
import random

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

def load_mcq_data(filepath="MCQ1.csv"):
    questions = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append({
                "question": row["Question"].strip(),
                "A": row["Option A"].strip(),
                "B": row["Option B"].strip(),
                "C": row["Option C"].strip(),
                "D": row["Option D"].strip(),
                "correct_answer": row["Correct Answer"].strip()
            })
    return questions

def cosine_sim(a, b):
    return np.dot(a, b) / (norm(a) * norm(b) + 1e-10)

questions_data = load_mcq_data()
question_texts = [q["question"] for q in questions_data]
question_embeddings = model.encode(question_texts, normalize_embeddings=True)

def get_similar_questions(topic, num_questions=15):
    if not topic:
        return []

    topic_embedding = model.encode([topic], normalize_embeddings=True)[0]


    similarities = [cosine_sim(topic_embedding, emb) for emb in question_embeddings]


    top_50_indices = np.argsort(similarities)[-50:][::-1]
    selected_indices = random.sample(list(top_50_indices), num_questions)

    return [questions_data[i] for i in selected_indices]
