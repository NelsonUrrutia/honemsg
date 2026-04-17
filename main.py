# TODO
# On the next session I will import the ollama module an implement the basic
# methods to send the prompt to the model
context_options = ["slack message", "e-mail", "documentation", "general text"]
tone_options = ["professional", "technical", "instructions"]
grammar_options = ["concise", "clarity"]


print("Context")
print("1. Slack Message")
print("2. E-mail")
print("3. Documentation")
print("4. General Text")
print("\n")
context = input("Select an option: ")

print("\nTone")
print("1. Professional")
print("2. Technical")
print("3. Instructions")
print("\n")
tone = input("Select an option: ")

print("\nGrammar")
print("1. Concise")
print("2. Clarity")
print("\n")
grammar = input("Select and option: ")

print("\nMessage")
message = input("")

context = context_options[int(context) - 1]
tone = tone_options[int(tone) - 1]
grammar = grammar_options[int(grammar) - 1]

prompt = f"Please improve the follwing message. Is a {context}; with a {tone}. The grammar should be {grammar}. Give up to 3 suggestions. First give the suggestions, then some additional recommedations. This is the message: {message}"

print(prompt)
