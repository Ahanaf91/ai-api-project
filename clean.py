import json
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# --- MODIFIED: Load memory function to prioritize memory_clean.json ---
def load_memory():
    # Always load from the raw memory file
    try:
        with open("memory.json", "r", encoding="utf-8") as f:
            print("Loading raw memory from memory.json")
            return json.load(f)
    except FileNotFoundError:
        print("No memory.json found!")
        return []

# --- Save cleaned memory ---
def save_clean(memory, filename="memory_clean.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)
    print(f"Cleaned memory saved to {filename}")

# --- MODIFIED: is_useful function now uses semantic similarity ---
def is_useful(entry, model, useful_phrases_embeddings):
    user_msg = entry["you"].strip().lower()

    # --- First-pass filter for obvious junk (less aggressive now) ---
    trash_keywords = ["hlw", "hello", "hi", "hey", "what??????", "ahhh", "ok", "test"] # MODIFIED: Removed model names
    if len(user_msg) < 10:  # MODIFIED: Lowered minimum length
        return False
    if any(word in user_msg for word in trash_keywords):
        return False
    if user_msg.startswith("python -u"):
        return False  # skip code run commands

    # --- NEW: Semantic similarity check ---
    # Encode the user's message
    message_embedding = model.encode(user_msg, convert_to_tensor=True)

    # Calculate cosine similarity against the "useful" phrases
    cosine_scores = util.cos_sim(message_embedding, useful_phrases_embeddings)

    # Check if the highest similarity score is above a threshold
    if max(cosine_scores[0]) > 0.2:  # Lowered threshold
        return True

    return False

# --- MAIN CLEANER ---
print("Initializing advanced memory cleaner...")

# --- NEW: Load the sentence-transformer model ---
# This model runs locally, no API key needed. It will be downloaded on the first run.
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- NEW: Define "useful" phrases for semantic comparison ---
useful_phrases = [
    "how do I", "can you explain", "what is the best way to", "write a script for",
    "help me with", "give me an example of", "I want to build", "fix this code",
    "explain the difference between", "what are the advantages of", "generate a function that"
]

# --- NEW: Encode the useful phrases once ---
useful_phrases_embeddings = model.encode(useful_phrases, convert_to_tensor=True)

print("Cleaning your AI chat memory using semantic analysis...")

memory = load_memory()
original_count = len(memory)

cleaned = []
for entry in memory:
    # --- MODIFIED: Pass the model and embeddings to the function ---
    if is_useful(entry, model, useful_phrases_embeddings):
        cleaned.append(entry)

save_clean(cleaned, "memory_clean.json")

print(f"Done! {original_count} → {len(cleaned)} messages kept.")
print("Useful chats saved. Junk removed!")
