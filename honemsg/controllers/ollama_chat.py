from ollama import chat


def send_message_to_ollama(context, actions, message):
    actions_text = ", ".join(actions) if actions else "none"
    prompt_message = f"Context: {context} \n Actions: {actions_text} \n Message: {message}"
    response = chat(
        model="translategemma:latest",
        messages=[
            {
                'role': 'user',
                'content': prompt_message
            }
        ],
        stream=False
    )
    return response['message']['content']
