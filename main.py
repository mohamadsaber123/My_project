import pandas as pd
import sentence_transformers as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random

df = pd.read_csv("MCQ1.csv")
df.columns = df.columns.str.strip()
model = st.SentenceTransformer("paraphrase-MiniLM-L6-v2")

questions = list(df["Question"])
question_embeddings = model.encode(questions, normalize_embeddings=True)

def get_similar_questions(topic, num_questions=15):
    if not topic:
        return []

    topic_embedding = model.encode([topic], normalize_embeddings=True)
    similarities = cosine_similarity(topic_embedding, question_embeddings)[0]

    top_50_indices = np.argsort(similarities)[-50:][::-1]
    selected_indices = random.sample(list(top_50_indices), num_questions)

    result = []
    for i in selected_indices:
        question_data = {
            "question": df["Question"][i],
            "A": df["Option A"][i],
            "B": df["Option B"][i],
            "C": df["Option C"][i],
            "D": df["Option D"][i],
            "correct_answer": df["Correct Answer"][i]
        }
        result.append(question_data)

    return result
