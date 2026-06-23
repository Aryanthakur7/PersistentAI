# Embedding Server — Google Colab

This notebook runs the **semantic embedding server** for Persistent AI. It loads the `multi-qa-mpnet-base-dot-v1` model from HuggingFace, exposes it as a FastAPI endpoint on port `8000`, and tunnels it publicly via ngrok so your local backend can reach it.

> **Run this notebook first, before starting the local backend.**

---

## What It Does

| Step | What happens |
|---|---|
| Cell 1 | Installs `sentence-transformers`, `fastapi`, `uvicorn`, `nest-asyncio`, `pyngrok` |
| Cell 2 | Imports all libraries |
| Cell 3 | Downloads and loads `multi-qa-mpnet-base-dot-v1` (~438MB, runs on T4 GPU) |
| Cell 4 | Defines the FastAPI app with a `POST /embed` endpoint |
| Cell 5 | Applies `nest_asyncio` for async support inside Colab |
| Cell 6 | Authenticates ngrok with your authtoken |
| Cell 7 | Opens a public ngrok tunnel on port `8000` and prints the URL |
| Cell 8 | Starts the uvicorn server — **keep this cell running** |

---

## Prerequisites

- A Google account with access to [Google Colab](https://colab.research.google.com)
- A free ngrok account and authtoken — get one at [https://dashboard.ngrok.com](https://dashboard.ngrok.com)
- Runtime set to **T4 GPU** (recommended for faster model load)

---

## Step-by-Step Setup

### Step 1 — Open in Colab

Upload `embedding_server.ipynb` to Google Drive, then open it in Colab. Or go to:

### Step 2 — Set Runtime to GPU

### Step 3 — Add your ngrok authtoken

In **Cell 6**, replace the existing token with your own:

```python
!ngrok config add-authtoken YOUR_NGROK_TOKEN_HERE
```

Get your token from: [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)

### Step 4 — Run all cells in order

Wait for the model to finish loading — you'll see `Model loaded.` printed in Cell 3. This takes about 30–60 seconds on T4 GPU.

### Step 5 — Copy the ngrok URL

After Cell 7 runs, you'll see output like:

Copy the `https://xxxx-xxxx-xxxx.ngrok-free.app` part.

### Step 6 — Paste URL into backend config

Open `backend/config.py` on your local machine and update:

```python
EMBED_URL = "https://xxxx-xxxx-xxxx.ngrok-free.app/embed"
```

### Step 7 — Keep the notebook running

Cell 8 runs the uvicorn server — **do not close the browser tab or stop this cell** while using Persistent AI. Every request from your local backend will hit this server.

---

## API Reference

**Endpoint:** `POST /embed`

**Request:**
```json
{ "text": "your sentence here" }
```

**Response:**
```json
{
  "embedding": [0.023, -0.14, ...],
  "dimension": 768
}
```

**Health check:** `GET /` → `{"status": "Embedding server running"}`

---

## Important Notes

| Note | Detail |
|---|---|
| **ngrok URL changes every restart** | Each time you restart the Colab session, a new ngrok URL is generated. Update `config.py` each time. |
| **Free ngrok limit** | Free tier allows 1 active tunnel and has a request rate limit. Sufficient for development. |
| **Colab session timeout** | Free Colab sessions disconnect after ~90 minutes of inactivity. If the backend starts returning embedding errors, restart the Colab and update the URL. |
| **Embedding dimension** | Model outputs **768-dimensional** vectors. This must match `EMBED_DIM = 768` in `backend/config.py`. |
| **Model** | `multi-qa-mpnet-base-dot-v1` — optimized for semantic similarity and retrieval tasks. |

---

## ⚠️ Security Note

Never commit your real ngrok authtoken to GitHub. Before pushing, replace it in the notebook with a placeholder:

```python
!ngrok config add-authtoken YOUR_NGROK_TOKEN_HERE
```