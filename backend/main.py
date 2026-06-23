from modules.conversation_engine import(normal_chat)
from modules.memory_engine import (store_memory,retrieve_memory,delete_memory,restore_memory)
from modules.prior_occurrence import (prior_occurrence_check)
from modules.reconstruction_engine import (reconstruct_memory)

# --------------------------------
# seed episodic memory
# --------------------------------
store_memory("User proposed trace-based memory reconstruction.")
store_memory("User discussed context beyond time and identity.")
store_memory("User suggested reconstructing memories from residual traces.")

# --------------------------------
# normal retrieval
# --------------------------------
query=input("Ask memory question: ")
results=retrieve_memory(query)
print("Retrieved candidates:")
print(results)

# --------------------------------
# If you manually damage the main memory
# before running or during demo,
# retrieval may return degraded traces.
# Then reconstruction path activates.
# --------------------------------

prior_event, candidates = prior_occurrence_check(query)

if prior_event:
    hypothesis=reconstruct_memory(query,results)
    print("Reconstruction hypothesis:")
    print(hypothesis)
    confirm=input("Was this what you meant? (y/n): ")
    if confirm.lower()=="y":
        restore_memory(hypothesis)
        print("Memory reconsolidated.")
else:
    print("No prior event inferred.")
