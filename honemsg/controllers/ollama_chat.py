from ollama import chat


def send_message_to_ollama(message):
    response = chat(
        model="translategemma:latest",
        messages=[
            {
                'role': 'user',
                'content': f"Improve the following message \n {message}"
            }
        ],
        stream=False
    )
    return response['message']['content']
