# honemsg

### Sharpen your messages with a local LLM

> `honemsg` is a CLI tool that improves your draft messages and give you suggestions using a local LLM. Set the context and tone, get back a sharpen text.

## Features

- **Context**
  - Slack message
  - E-mail
  - Documentation
  - General text

- **Tone**
  - Professional
  - Technical
  - Instructions

- **Grammar**
  - Concise
  - Clarity

## Flow
1. The user starts the util typing `honemsg`
2. User selects the context
3. User selects the tone
4. User selects the gramar
5. The user starts to type the text
6. The user tabs Enter to continue
7. A loading state shows, while process the prompt with the LLM
8. The improve text and suggestions appears.

## Requirements
- Python
- Ollama
- LLM model (recommended _translategemma_)
