from openai import OpenAI
import sys, time, json, os
from datetime import datetime

# --- API setup ---
try:
    with open("config.json", "r") as f:
        config = json.load(f)
        a4f_api_key = config["API_KEY"]
except FileNotFoundError:
    print("❌ Error: config.json not found. Please create it from config.example.json and add your API key.")
    sys.exit()
except KeyError:
    print("❌ Error: 'API_KEY' not found in config.json. Please make sure it is set correctly.")
    sys.exit()

a4f_base_url = "https://api.a4f.co/v1"

client = OpenAI(
    api_key=a4f_api_key,
    base_url=a4f_base_url,
)

# --- typing effect ---
def slow_print(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# --- memory system ---
def load_memory():
    if os.path.exists("memory_clean.json"):
        with open("memory_clean.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_memory(memory):
    with open("memory.json", "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

memory = load_memory()

models = [
    ("provider-1/llama-3.2-3b-instruct-fp-16", "fast"),
    ("provider-5/gpt-4o-mini", "balanced"),
    ("provider-6/llama-3.2-1b-instruct", "fast & smart"),
    ("provider-3/gemini-2.5-flash-lite-preview-09-2025", "large context"),
    ("provider-1/llama-3.2-1b-instruct-fp-16", "lightweight")
]

indications = []



# --- print models ---


print("welcome to my ai chat system, this is a demo of ai api 2.0 ")



print("\n_______________________________")
print("Available AI models:")

for m, desc in models:
    try:
        test = client.chat.completions.create(
            model=m,
            messages=[
                {"role": "system", "content": "Quick test to check if you're online"},
                {"role": "user", "content": "Hi, say hello!"}
            ]
        )
        indications.append("✅ Online")
    except:
        indications.append("❌ Offline")

    # print right after checking
    print(f"* {m:45} ({desc}) {indications[-1]}")





# --- select model ---

try:
    ai_model_name = input(f"give me a model name: ").strip()
except:
    print("Invalid input, using default model gemma-3-4b-it")
    ai_model_name = "provider-1/gemma-3-4b-it"





# --- test model before chat ---
print(f"\n🔍 Testing model: {ai_model_name} ...")
try:
    test = client.chat.completions.create(
        model=ai_model_name,
        messages=[
            {"role": "system", "content": "Quick test for if you are working or you can say online or not "},
            {"role": "user", "content": "Hi, say hello!"}
        ]
    )
    print("✅ Model is working!")
    print("Response:", test.choices[0].message.content)
except Exception as e:
    print("❌ Error connecting to model:", e)
    sys.exit()
    
    
    
    

# --- chat loop ---
while True:
    use_input = input("\nYou: ")
    if use_input.lower() in ["exit", "quit", "off", "stop", "end", "done"]:
        print("Saving chat & exiting...")
        save_memory(memory)
        break

    print("Analyzing input...")

    # prepare context
    messages = [{"role": "system", "content": "You are a helpful assistant. Be short and efficient. and try to understand human and be empathetic.dont give me too many answers only one but it needs to be efficent and understandable"}]
    for pair in memory[-10:]:  # load last 10 chats only
        messages.append({"role": "user", "content": pair["you"]})
        messages.append({"role": "assistant", "content": pair["ai"]})
    messages.append({"role": "user", "content": use_input})

    # ask AI
    try:
        completion = client.chat.completions.create(
            model=ai_model_name,
            messages=messages
        )
        ai_reply = completion.choices[0].message.content
        slow_print("AI: " + ai_reply)

        # save memory
        memory.append({
            "you": use_input,
            "ai": ai_reply,
            "time": datetime.now().strftime("%A, %B %d, %Y - %I:%M %p")
        })
        save_memory(memory)

    except Exception as e:
        print("❌ API Error:", e)
