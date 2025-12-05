import os
import time
import math
import requests
from collections import Counter, defaultdict
import re
import nltk
nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize, word_tokenize

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def fetch_recent_documents(top_k=200):
    """
    Fetch recent events by calling local /search/ endpoint with empty query.
    Returns list of documents (strings) and raw hits.
    """
    try:
        r = requests.post("http://0.0.0.0:8000/search/", json={"query":"", "top_k": top_k}, timeout=10)
        r.raise_for_status()
        hits = r.json() or []
        docs = [h.get("document") for h in hits if h.get("document")]
        return docs, hits
    except Exception as e:
        return [], []

def extractive_summary(texts, max_sentences=8):
    """
    Simple extractive summarizer: score sentences by word frequency.
    """
    if not texts:
        return "No documents available to summarize."

    all_text = "\n".join(texts)
    sents = sent_tokenize(all_text)
    if len(sents) <= max_sentences:
        return "\n\n".join(sents)

    # build frequency distribution
    words = [w.lower() for w in word_tokenize(all_text) if re.match(r'\w+', w)]
    freq = Counter(words)
    # score sentences
    sent_scores = []
    for s in sents:
        tokens = [w.lower() for w in word_tokenize(s) if re.match(r'\w+', w)]
        if not tokens:
            continue
        score = sum(freq[t] for t in tokens) / math.sqrt(len(tokens))
        sent_scores.append((score, s))
    # pick top sentences and return in original order
    top = sorted(sent_scores, key=lambda x: x[0], reverse=True)[:max_sentences]
    chosen = set(s for _, s in top)
    ordered = [s for s in sents if s in chosen]
    return "\n\n".join(ordered)

def call_openai_summary(prompt, max_tokens=300):
    """
    Use OpenAI if API key is available. This uses the v1/completions or chat completions if available.
    """
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        # try chat completions first (if supported)
        if hasattr(openai, "ChatCompletion"):
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini" if "gpt-4o-mini" in openai.Model.list().data else "gpt-4o",
                messages=[{"role":"system","content":"You are a concise summarizer."},
                          {"role":"user","content": prompt}],
                max_tokens=max_tokens,
                temperature=0.2,
            )
            text = resp.choices[0].message.content.strip()
            return text
        else:
            # fallback to completions
            resp = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.2
            )
            return resp.choices[0].text.strip()
    except Exception as e:
        # OpenAI call failed
        return None

def summarize_long_term(top_k=200, granular=False):
    """
    Returns multi-granularity summary:
      {
        "overall": "...",
        "by_month": { "2025-11": "...", ... }   # if granular True
      }
    """
    texts, hits = fetch_recent_documents(top_k=top_k)
    if not texts:
        return {"status":"ok", "overall": "No documents found", "by_month": {}}

    # quick extractive overall
    overall_extractive = extractive_summary(texts, max_sentences=10)

    # try OpenAI for better summary
    if OPENAI_API_KEY:
        prompt = f"Summarize the following documents concisely into 3 bullet points and one short paragraph:\n\n{overall_extractive}\n\nBullets:"
        openai_result = call_openai_summary(prompt, max_tokens=300)
        overall = openai_result if openai_result else overall_extractive
    else:
        overall = overall_extractive

    result = {"status":"ok", "overall": overall}

    if granular:
        # group documents by month if timestamp available in hits
        by_month_docs = defaultdict(list)
        for h in hits:
            ts = h.get("id") or h.get("timestamp") or None
            # fallback naive: attempt to parse timestamp in metadata or id pattern
            meta = h.get("metadata") or {}
            ts_val = None
            if isinstance(h.get("timestamp"), (int,float)):
                ts_val = int(h.get("timestamp"))
            elif isinstance(meta.get("timestamp"), (int,float)):
                ts_val = int(meta.get("timestamp"))
            # id pattern evt_173... fallback
            if ts_val:
                import datetime
                key = datetime.datetime.utcfromtimestamp(ts_val).strftime("%Y-%m")
            else:
                # try to detect year-month inside string (very loose)
                key = "misc"
            by_month_docs[key].append(h.get("document") or "")

        by_month_summary = {}
        for k, docs in by_month_docs.items():
            if not docs:
                continue
            short = extractive_summary(docs, max_sentences=4)
            # optionally call openai per month if available
            if OPENAI_API_KEY:
                prompt = f"Condense the following into 2 bullets and a 1-line summary:\n\n{short}"
                s = call_openai_summary(prompt, max_tokens=150) or short
            else:
                s = short
            by_month_summary[k] = s
        result["by_month"] = by_month_summary

    return result

# utility small test run
if __name__ == "__main__":
    print(summarize_long_term(top_k=80, granular=True))
