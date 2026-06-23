Embedding Server — Google Colab
This notebook runs the semantic embedding server for Persistent AI. It loads the multi-qa-mpnet-base-dot-v1 model from HuggingFace, exposes it as a FastAPI endpoint on port 8000, and tunnels it publicly via ngrok so your local backend can reach it.

Run this notebook first, before starting the local backend.


What It Does
StepWhat happensCell 1Installs sentence-transformers, fastapi, uvicorn, nest-asyncio, pyngrokCell 2Imports all librariesCell 3Downloads and loads multi-qa-mpnet-base-dot-v1 (~438MB, runs on T4 GPU)Cell 4Defines the FastAPI app with a POST /embed endpointCell 5Applies nest_asyncio for async support inside ColabCell 6Authenticates ngrok with your authtokenCell 7Opens a public ngrok tunnel on port 8000 and prints the URLCell 8Starts the uvicorn server — keep this cell running

Prerequisites

A Google account with access to Google Colab
A free ngrok account and authtoken — get one at https://dashboard.ngrok.com
Runtime set to T4 GPU (recommended for faster model load)


Step-by-Step Setup
Step 1 — Open in Colab
Upload embedding_server.ipynb to Google Drive, then open it in Colab. Or go to:
File → Open notebook → Upload → select the .ipynb file
Step 2 — Set Runtime to GPU
Runtime → Change runtime type → Hardware accelerator → T4 GPU → Save
Step 3 — Add your ngrok authtoken
In Cell 6, replace the existing token with your own:
python!ngrok config add-authtoken YOUR_NGROK_TOKEN_HERE
Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken
Step 4 — Run all cells in order
Runtime → Run all  (Ctrl + F9)
Wait for the model to finish loading — you'll see Model loaded. printed in Cell 3. This takes about 30–60 seconds on T4 GPU.
Step 5 — Copy the ngrok URL
After Cell 7 runs, you'll see output like:
Public URL: NgrokTunnel: "https://xxxx-xxxx-xxxx.ngrok-free.app" -> "http://localhost:8000"
Copy the https://xxxx-xxxx-xxxx.ngrok-free.app part.
Step 6 — Paste URL into backend config
Open backend/config.py on your local machine and update:
pythonEMBED_URL = "https://xxxx-xxxx-xxxx.ngrok-free.app/embed"
Step 7 — Keep the notebook running
Cell 8 runs the uvicorn server — do not close the browser tab or stop this cell while using Persistent AI. Every request from your local backend will hit this server.

API Reference
Endpoint: POST /embed
Request:
json{ "text": "your sentence here" }
Response:
json{
  "embedding": [0.023, -0.14, ...],   // 768-dimensional float vector
  "dimension": 768
}
Health check: GET / → {"status": "Embedding server running"}

