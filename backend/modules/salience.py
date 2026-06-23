from modules.embedding_client import get_embedding
from config import SALIENCE_THRESHOLD
from modules.affect_engine import infer_affect
import json
import numpy as np


def cosine(a,b):

    a=np.array(a)
    b=np.array(b)

    return np.dot(a,b)/(
        np.linalg.norm(a)*
        np.linalg.norm(b)
    )


def salience_score(
    text,
    recent_embeddings,
    goal_embedding
):

    e=get_embedding(text)


    # -------------------------
    # Semantic novelty
    # -------------------------

    if not recent_embeddings:

        novelty=1.0

    else:

        novelty=1-max(
            cosine(e,r)
            for r in recent_embeddings
        )


    # -------------------------
    # Goal relevance
    # -------------------------

    goal_rel=cosine(
        e,
        goal_embedding
    )


    # -------------------------
    # Information density
    # crude proxy for now
    # -------------------------

    info_density=min(
       len(text.split())/25,
       1.0
    )


    # -------------------------
    # Weighted salience score
    # -------------------------
    
    affect=json.loads(infer_affect(text))
    aff_intensity=max(
        affect["fear"],
        affect["joy"],
        affect["sadness"],
        affect["surprise"],
        affect["urgency"]
        )


    score=(
        0.3*novelty +
        0.3*goal_rel +
        0.2*info_density +
        0.2*aff_intensity
        )


    return score



def should_store(
    text,
    recent_embeddings,
    goal_embedding
):

    return (
        salience_score(
            text,
            recent_embeddings,
            goal_embedding
        )
        > SALIENCE_THRESHOLD
    )
    
#Important upgrade for later stage-
"""
Tiny optional hardening (not required tonight)

For numerical safety:

np.linalg.norm(a)

could theoretically be zero.

Could add epsilon guard someday.
"""
