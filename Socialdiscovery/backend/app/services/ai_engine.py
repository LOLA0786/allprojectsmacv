import openai

def summarize(messages: list[str]) -> str:
    if len(messages) < 5:
        return ""

    text = "\n".join(messages[-20:])

    res = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize key insights briefly."},
            {"role": "user", "content": text}
        ]
    )
    return res.choices[0].message.content
