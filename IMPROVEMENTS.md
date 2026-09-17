# Improvements

Findings from manually testing the message actions (`honemsg/controllers/ollama_chat.py`) against `translategemma:latest`.

## Issue: no system prompt / per-action instructions

`send_message_to_ollama` builds a single flat prompt with no system message:

```python
actions_text = ", ".join(actions) if actions else "none"
prompt_message = f"Context: {context} \n Actions: {actions_text} \n Message: {message}"
```

The model has no guidance on what each action (`shorten`, `summarize`, `improve`, etc.) should actually mean, or on the expected output format. Observed effects:

- **Shorten** returned three alternate options plus a "Key Changes Made" recap and a closing sentence ("Choose the option that best suits...") instead of a single shortened message — ironically bloated for an action meant to reduce length.
- **Summarize** occasionally opened with meta-commentary ("Okay, here's a summary of the Slack message:") instead of just the summary.
- Actions can blur together (shorten behaving like summarize) since there's no explicit definition distinguishing them.

## Proposed fix

1. Add a system message constraining output: return only the transformed message, no preamble, no multiple options, no explanation, no sign-off.
2. Add a per-action instruction map (e.g. `shorten` → "reduce length while preserving tone/meaning, don't restructure into a different format unless the original used one") and include the relevant instructions for whichever actions are selected.
3. Restructure the prompt to clearly separate: system instruction / message type context / action instructions / message to transform.
4. Re-test all five actions (improve, shorten, simplify, fix grammar, summarize) with the same sample inputs to confirm single, clean outputs.

Note: since each call to `chat()` is stateless (fresh `messages` list, no history), the system + per-action instructions need to be included on **every** request — there's nothing to bake in at the app level that persists across calls automatically.

## Alternative: Ollama Modelfile

A custom Modelfile can bake a general `SYSTEM` prompt into a derived model so it doesn't need to be sent on every request:

```
FROM translategemma:latest

SYSTEM """
You are a writing assistant. Apply the requested action(s) to the message and return only the resulting message. Do not include preamble, explanations, multiple options, or sign-offs.
"""

PARAMETER temperature 0.3
PARAMETER top_p 0.9
```

Build with `ollama create honemsg-writer -f ./Modelfile`, then swap `model="translategemma:latest"` for `model="honemsg-writer"` in `ollama_chat.py`.

This only covers the *general* behavior constraint — per-action instructions still vary by selection and would need to be included per-request regardless.
