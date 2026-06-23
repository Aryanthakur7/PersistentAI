import numpy as np
from modules.affect_engine import infer_affect
import json
from modules.embedding_client import get_embedding
from modules.memory_engine import retrieve_memory


def cosine(a, b):
    a = np.array(a, dtype='float32')
    b = np.array(b, dtype='float32')
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def prior_occurrence_check(query):
    candidates = retrieve_memory(query, k=5)

    if len(candidates) == 0:
        return False, []

    query_emb = get_embedding(query)

    try:
        query_affect = json.loads(infer_affect(query))
    except Exception:
        query_affect = {'fear': 0, 'joy': 0, 'sadness': 0, 'surprise': 0, 'urgency': 0, 'neutral': 1}

    # ─── Score each candidate ───
    similarities = []

    for c in candidates:
        c_emb = get_embedding(c)
        sim = cosine(query_emb, c_emb)

        try:
            cand_affect = json.loads(infer_affect(c))
        except Exception:
            cand_affect = {'fear': 0, 'joy': 0, 'sadness': 0, 'surprise': 0, 'urgency': 0, 'neutral': 1}

        emotion_overlap = (
            query_affect['fear']     * cand_affect['fear']     +
            query_affect['joy']      * cand_affect['joy']      +
            query_affect['sadness']  * cand_affect['sadness']  +
            query_affect['surprise'] * cand_affect['surprise'] +
            query_affect['urgency']  * cand_affect['urgency']
        )

        combined_score = 0.7 * sim + 0.3 * emotion_overlap
        similarities.append(combined_score)

    # ─── Confidence = weighted max + mean ───
    confidence = 0.7 * max(similarities) + 0.3 * np.mean(similarities)

    # ─── Dynamic threshold — but lowered floor to 0.55 (was 0.72, too strict) ───
    # Personal identity queries ("remember me?", "who am I?") are semantically
    # distant from stored facts ("name is Aryan"), so 0.72 always failed them.
    dynamic_threshold = np.mean(similarities) + 0.3 * np.std(similarities)
    FLOOR_THRESHOLD = 0.55  # lowered from 0.72

    if confidence > dynamic_threshold and confidence > FLOOR_THRESHOLD:
        return True, candidates

    return False, []
