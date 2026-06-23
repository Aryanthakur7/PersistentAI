# Persistent AI

> A conversational AI with persistent semantic memory, affect-weighted recall, and trace-based reconstruction.  
> *Context beyond time and identity.*

---

## Project Structure

```
PersistentAI/
├── backend/                   ← Python/Flask server (unchanged from original)
│   ├── app.py                 ← Flask app entry point
│   ├── config.py              ← Embedding URL, thresholds
│   ├── main.py                ← CLI interface (optional)
│   ├── requirements.txt       ← Python dependencies
│   ├── .gitignore
│   ├── modules/
│   │   ├── affect_engine.py        ← Emotion inference (Groq/LLaMA)
│   │   ├── conversation_engine.py  ← Normal chat (Groq/LLaMA)
│   │   ├── embedding_client.py     ← Vector embedding client
│   │   ├── memory_engine.py        ← FAISS memory store
│   │   ├── prior_occurrence.py     ← Similarity + affect recall
│   │   ├── reconstruction_engine.py← Degraded memory reconstruction
│   │   ├── residual_state.py       ← Semantic residue layer
│   │   └── salience.py             ← Salience gating
│   ├── memory/
│   │   ├── faiss_index.bin         ← Persisted vector index
│   │   └── memory_records.pkl      ← Persisted memory records
│   └── demo/
│       └── fault_injection_demo.py
│
└── frontend/                  ← Static HTML/CSS/JS UI
    ├── index.html             ← Main UI page
    ├── css/
    │   └── style.css          ← All styles
    └── js/
        └── app.js             ← All frontend logic
```

---

## Prerequisites

| Requirement | Details |
|---|---|
| Python | 3.9 or higher |
| pip | Latest recommended |
| Groq API Key | Free at https://console.groq.com |
| Embedding Server | Running at the URL in `config.py` |

---

## Step-by-Step Setup & Running

### Step 1 — Clone or unzip the project

If you downloaded the zip, extract it. You should see `PersistentAI/` with `backend/` and `frontend/` folders.

---

### Step 2 — Set up a Python virtual environment (recommended)

```bash
cd PersistentAI/backend

# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

---

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

This installs: Flask, faiss-cpu, sentence-transformers, groq, requests, numpy, python-dotenv.

---

### Step 4 — Configure environment variables

Create a `.env` file inside the `backend/` folder:

```bash
# backend/.env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at: https://console.groq.com

---

### Step 5 — Configure the embedding server

Open `backend/config.py` and update `EMBED_URL` to point to your embedding server:

```python
EMBED_URL = "http://localhost:5001/embed"   # local
# or your ngrok URL
# EMBED_URL = "https://your-ngrok-url.ngrok-free.app/embed"
```

The embedding server must expose a POST `/embed` endpoint that accepts `{"text": "..."}` and returns `{"embedding": [...768 floats...]}`.

> **Quick option:** Use the `sentence-transformers` library to spin up a local embedding server, or use any compatible embedding API.

---

### Step 6 — Run the backend server

```bash
# Make sure you're in backend/ with venv activated
cd PersistentAI/backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### Step 7 — Open the UI

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

The Flask server automatically serves the frontend from the `frontend/` folder.

---

## Memory Persistence

Memory is automatically saved to `backend/memory/`:
- `faiss_index.bin` — vector similarity index
- `memory_records.pkl` — raw memory records

These persist between restarts. To reset memory, delete both files.

---

## Memory Modes

| Mode | Description |
|---|---|
| **◈ Novel** | No prior event found; responds from LLM with recent context |
| **⟳ Direct Recall** | Prior event detected; recalls stored memory directly |
| **⟡ Reconstruction** | Degraded traces only; reconstructs probable memory via LLM |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `Connection refused` on `/chat` | Make sure `python app.py` is running in `backend/` |
| `GROQ_API_KEY` error | Check your `.env` file exists in `backend/` |
| Embedding errors | Verify `EMBED_URL` in `config.py` points to a running server |
| Import errors | Make sure you ran `pip install -r requirements.txt` with venv active |
| Port 5000 in use | Run with `app.run(port=5001)` in `app.py` and visit port 5001 |

---

## Notes

- The frontend is pure HTML/CSS/JS — no build step, no npm, no Node required.
- All AI calls go through the Python backend; the frontend only calls `/chat`.
- The project uses Groq's LLaMA 3.3 70B for conversation, affect inference, and reconstruction.
