from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "Contract employees get 8 days of casual leave",
    "How many casual leaves do contract staff have?",
    "The office cafeteria serves lunch at noon",
]

vectors = model.encode(sentences)
print(vectors.shape)
print(vectors[0][:5])
print(util.cos_sim(vectors[0], vectors[1]))
print(util.cos_sim(vectors[0], vectors[2]))