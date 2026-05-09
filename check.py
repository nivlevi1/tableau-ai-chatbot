import chromadb
from collections import Counter

c = chromadb.HttpClient(host="chroma", port=8000)
col = c.get_collection("tableau_knowledge")

print("=== Chunk counts by source ===")
for src in ["book", "reddit", "stackoverflow"]:
    r = col.get(where={"source_type": src}, include=[])
    print(f"  {src}: {len(r['ids'])} chunks")

print("\n=== Duplicate check (same document ID) ===")
all_ids = col.get(include=[])["ids"]
counts = Counter(all_ids)
dupes = {k: v for k, v in counts.items() if v > 1}
if dupes:
    print(f"  {len(dupes)} duplicate IDs found!")
    for id_, count in list(dupes.items())[:5]:
        print(f"  {id_}: {count}x")
else:
    print("  No duplicates found.")
