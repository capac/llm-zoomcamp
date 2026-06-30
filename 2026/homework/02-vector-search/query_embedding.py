from sentence_transformers import SentenceTransformer

q1 = "How does approximate nearest neighbor search work?"
model = SentenceTransformer("all-MiniLM-L6-v2")

v1 = model.encode(q1)

print(f"First value for vector v1[0]: {v1[0]}")
