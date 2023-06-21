import tiktoken

openai_model = "gpt-3.5-turbo-0613"

def reportTokens(prompt, role = ""):
    encoding = tiktoken.encoding_for_model(openai_model)
    message_tokens = len(encoding.encode(prompt))
    # print number of tokens in light gray, with first 10 characters of prompt in green
    print(
        "\033[37m"
        + str(message_tokens)
        + " tokens\033[0m"
        + " in role: "
        + "\033[92m"
        + role
        + "\033[0m"
        + " in prompt: "
        + "\033[92m"
        + prompt[:100]
        + "\033[0m"
    )
    
    return message_tokens

def reportMessageTokens(system_prompt, user_prompt):
    messages = []
    message_tokens = 0
    messages.append({"role": "system", "content": system_prompt})
    message_tokens += reportTokens(system_prompt, "system")
    messages.append({"role": "user", "content": user_prompt})
    message_tokens += reportTokens(user_prompt, "user  ")

def count_tokens(text):
    encoding = tiktoken.encoding_for_model(openai_model)
    tokens = len(encoding.encode(text))
    return tokens
