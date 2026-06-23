import faiss
import numpy as np
import pickle
import os
from config import EMBED_DIM
from modules.affect_engine import infer_affect
from modules.embedding_client import get_embedding
from modules.salience import salience_score

# ─── Resolve memory path relative to this file, not cwd ───
_HERE = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(_HERE, '..', 'memory')
FAISS_PATH = os.path.join(MEMORY_DIR, 'faiss_index.bin')
RECORDS_PATH = os.path.join(MEMORY_DIR, 'memory_records.pkl')

# ─── Load persisted memory on startup (FIX: was never loaded) ───
def _load_memory():
    """Load FAISS index and memory records from disk if they exist."""
    index = faiss.IndexFlatL2(EMBED_DIM)
    records = []

    if os.path.exists(FAISS_PATH) and os.path.exists(RECORDS_PATH):
        try:
            loaded_index = faiss.read_index(FAISS_PATH)
            with open(RECORDS_PATH, 'rb') as f:
                loaded_records = pickle.load(f)

            # Validate they are in sync
            if loaded_index.ntotal == len(loaded_records):
                index = loaded_index
                records = loaded_records
                print(f"[Memory] Loaded {len(records)} memories from disk.")
            else:
                print(f"[Memory] Index/records mismatch — starting fresh.")
        except Exception as e:
            print(f"[Memory] Load failed ({e}) — starting fresh.")
    else:
        print("[Memory] No saved memory found — starting fresh.")

    return index, records

index, memory_records = _load_memory()


def store_memory(text):
    emb = np.array(
        [get_embedding(text)],
        dtype='float32'
    )
    index.add(emb)

    record = {
        'text': text,
        'affect': infer_affect(text),
        'trace_pointers': ['semantic', 'episodic']
    }
    memory_records.append(record)


def retrieve_memory(query, k=5):
    if index.ntotal == 0:
        return []

    # Don't ask for more than we have
    k = min(k, index.ntotal)

    q = np.array(
        [get_embedding(query)],
        dtype='float32'
    )

    D, I = index.search(q, k)

    results = []
    for i in I[0]:
        if i != -1 and i < len(memory_records):
            rec = memory_records[i]
            if rec != '[DELETED]':
                results.append(rec['text'])

    return results


def delete_memory(idx):
    global memory_records
    memory_records[idx] = '[DELETED]'
    print('Memory deleted.')


def restore_memory(text):
    print('Reconsolidating memory...')
    store_memory(text)


def save_memory():
    os.makedirs(MEMORY_DIR, exist_ok=True)
    faiss.write_index(index, FAISS_PATH)
    with open(RECORDS_PATH, 'wb') as f:
        pickle.dump(memory_records, f)
    print(f'[Memory] Saved {len(memory_records)} memories to disk.')
