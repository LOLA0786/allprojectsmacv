import re
import json
import os
from collections import defaultdict, Counter
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)
GRAPH_FILE = os.path.join(DATA_DIR, "behavior_graph.json")

ENTITY_RE = re.compile(r'(?:@[\w\d\-_\.]+)|(?:[A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,})*)|(?:[\\w.+-]+@[\\w-]+\\.[\\w.-]+)')

def fetch_events(top_k=500):
    try:
        r = requests.post("http://0.0.0.0:8000/search/", json={"query":"","top_k": top_k}, timeout=10)
        r.raise_for_status()
        return r.json() or []
    except Exception as e:
        return []

def extract_entities(text):
    if not text:
        return []
    # find patterns that look like names, emails or @mentions
    found = ENTITY_RE.findall(text)
    # normalize: strip, lower emails, keep person names as-is
    entities = []
    for e in found:
        e = e.strip()
        if "@" in e and not e.startswith("@"):
            entities.append(e.lower())
        else:
            entities.append(e)
    # dedupe
    seen = []
    for e in entities:
        if e not in seen:
            seen.append(e)
    return seen

def build_graph(top_k=500):
    events = fetch_events(top_k=top_k)
    nodes = Counter()
    edges = defaultdict(Counter)  # edges[src][dst] = count

    for ev in events:
        text = ev.get("document") or ""
        meta = ev.get("metadata") or {}
        # combine text + metadata values for entity mining
        meta_text = " ".join(str(v) for v in meta.values() if isinstance(v, (str,int)))
        combined = f"{text}\n{meta_text}"
        ents = extract_entities(combined)
        for a in ents:
            nodes[a] += 1
        # co-occurrence
        for i in range(len(ents)):
            for j in range(i+1, len(ents)):
                edges[ents[i]][ents[j]] += 1
                edges[ents[j]][ents[i]] += 1

    # serialize to dict
    graph = {
        "nodes": [{"id": n, "count": c} for n,c in nodes.most_common()],
        "edges": []
    }
    for a, dsts in edges.items():
        for b, c in dsts.items():
            graph["edges"].append({"source": a, "target": b, "weight": c})
    # sort edges by weight desc
    graph["edges"] = sorted(graph["edges"], key=lambda x: x["weight"], reverse=True)

    # save file
    with open(GRAPH_FILE, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    return graph

def load_graph():
    if not os.path.exists(GRAPH_FILE):
        return {"nodes":[], "edges":[]}
    with open(GRAPH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def query_node(node_id, top_k=10):
    graph = load_graph()
    neighbors = []
    for e in graph.get("edges", []):
        if e["source"] == node_id:
            neighbors.append(e)
    # return node info + top neighbors
    nodes = {n["id"]: n for n in graph.get("nodes", [])}
    node = nodes.get(node_id, {"id":node_id, "count":0})
    neighbors = sorted(neighbors, key=lambda x: x["weight"], reverse=True)[:top_k]
    return {"node": node, "neighbors": neighbors}

if __name__ == "__main__":
    g = build_graph()
    print("Graph built:", len(g["nodes"]), "nodes;", len(g["edges"]), "edges")
