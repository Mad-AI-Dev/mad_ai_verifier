import openai
import time
import json
import logging
import os
import tiktoken

#openai_model = "gpt-4"  # or 'gpt-3.5-turbo',
openai_model = "gpt-3.5-turbo-0613"  # or 'gpt-3.5-turbo',
openai_model_max_tokens = 800  # i wonder how to tweak this properly

# gpt-4
# gpt-4-0613
# gpt-3.5-turbo-16k
# gpt-3.5-turbo
# gpt-3.5-turbo-0613
# gpt-3.5-turbo-16k-0613


# Set up your OpenAI API credentials
# openai.api_key = os.getenv("OPENAI_API_KEY")

def print_response_tokens(response):
    prompt_tokens = response["usage"]["prompt_tokens"]
    completion_tokens = response["usage"]["completion_tokens"]
    total_tokens = response["usage"]["total_tokens"]

    # ANSI escape sequence for red color
    RED_COLOR = "\033[91m"
    # ANSI escape sequence to reset color
    RESET_COLOR = "\033[0m"

    print(f"Prompt Tokens: {RED_COLOR}{prompt_tokens}{RESET_COLOR}")
    print(f"Completion Tokens: {RED_COLOR}{completion_tokens}{RESET_COLOR}")
    print(f"Total Tokens: {RED_COLOR}{total_tokens}{RESET_COLOR}")


def generate_response(system_prompt, user_prompt, *args):

    retry_count = 0
    max_retries = 50
    wait_time = 5
    
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def reportTokens(prompt):
        encoding = tiktoken.encoding_for_model(openai_model)
        message_tokens = len(encoding.encode(prompt))
        # print number of tokens in light gray, with first 10 characters of prompt in green
        print(
            "\033[37m"
            + str(message_tokens)
            + " tokens\033[0m"
            + " in prompt: "
            + "\033[92m"
            + prompt[:50]
            + "\033[0m"
        )
        
        return message_tokens
  
    messages = []
    message_tokens = 0
    messages.append({"role": "system", "content": system_prompt})
    message_tokens += reportTokens(system_prompt)
    messages.append({"role": "user", "content": user_prompt})
    message_tokens += reportTokens(user_prompt)

    if openai_model == "gpt-4":
        openai_model_max_tokens = 8150
    elif openai_model == "gpt-3.5-turbo":
        openai_model_max_tokens = 4050
    else:
        openai_model_max_tokens = 4050

    max_tokens_for_message = openai_model_max_tokens - message_tokens


    # loop thru each arg and add it to messages alternating role between "assistant" and "user"
    role = "assistant"
    for value in args:
        messages.append({"role": role, "content": value})
        reportTokens(value)
        role = "user" if role == "assistant" else "assistant"

    params = {
        "model": openai_model,
        "messages": messages,
        # "max_tokens": max_tokens_for_message,
        # "max_tokens": 800,
        "temperature": 1.0,
    }

    # Generate a unique filename
    # filename = str(uuid.uuid4()) + ".txt"

    # Save the prompt and params to a file
    # with open(filename, "w") as file:
    #    file.write("Prompt:\n")
    #    file.write(prompt)
    #    file.write("\n\nParams:\n")
    #    file.write(str(params))

    # Send the API request


    while retry_count < max_retries:
        try:
            response = openai.ChatCompletion.create(**params)
            
            # print(response)
            # input("Press Enter to continue...")

            # Process the response as needed
            # ...

            break  # Exit the loop if API call succeeds
        except openai.APIError as e:
            logging.error(f"OpenAI API Error: {str(e)}")
            wait_time += 5
            print(f"OpenAI: Retrying in {wait_time} seconds, retry count: {retry_count}...")
            time.sleep(wait_time)
            retry_count += 1
        except openai.error.APIConnectionError as e:
            logging.error(f"OpenAI API Connection Error: {str(e)}")
            wait_time += 5
            print(f"OpenAI: Retrying in {wait_time} seconds, retry count: {retry_count}...")
            time.sleep(wait_time)
            retry_count += 1
        except openai.InvalidRequestError as e:
            logging.error(f"OpenAI Invalid Request Error: {str(e)}")
            break  # Exit the loop if it's an invalid request error
        except openai.error.AuthenticationError as e:
            logging.error(f"OpenAI Authentication Error: {str(e)}")
            break  # Exit the loop if it's an authentication error
        except openai.error.PermissionError as e:
            logging.error(f"OpenAI Permission Error: {str(e)}")
            break  # Exit the loop if it's a permission error
        except openai.error.RateLimitError as e:
            logging.error(f"OpenAI Rate Limit Error: {str(e)}")
            wait_time += 5
            print(f"OpenAI: Retrying in {wait_time} seconds, retry count: {retry_count}...")
            time.sleep(wait_time)
            retry_count += 1
        except openai.error.ServiceUnavailableError as e:
            logging.error(f"OpenAI Service Unavailable Error: {str(e)}")
            wait_time += 5
            print(f"OpenAI: Retrying in {wait_time} seconds, retry count: {retry_count}...")
            time.sleep(wait_time)
            retry_count += 1
        except openai.error.InvalidAPIType as e:
            logging.error(f"OpenAI Invalid API Type Error: {str(e)}")
            break  # Exit the loop if it's an invalid API type error
        except openai.error.SignatureVerificationError as e:
            logging.error(f"OpenAI Signature Verification Error: {str(e)}")
            break  # Exit the loop if it's a signature verification error
        except openai.error.TryAgain as e:
            logging.error(f"OpenAI Try Again Error: {str(e)}")
            wait_time += 5
            print(f"OpenAI: Retrying in {wait_time} seconds, retry count: {retry_count}...")
            time.sleep(wait_time)
            retry_count += 1
        except openai.error.Timeout as e:
            logging.error(f"OpenAI Timeout Error: {str(e)}")
            wait_time += 5
            print(f"OpenAI: Retrying in {wait_time} seconds, retry count: {retry_count}...")
            time.sleep(wait_time)
            retry_count += 1
        except Exception as e:
            logging.error(f"Unexpected Error: {str(e)}")
            wait_time += 5
            print(f"OpenAI: Retrying in {wait_time} seconds, retry count: {retry_count}...")
            time.sleep(wait_time)
            retry_count += 10
        retry_count += 1

    if retry_count == max_retries:
        print("OpenAI: Maximum number of retries reached. Exiting...")

    # Extract items from the API response
    response_message = response['choices'][0]['message']['content']
    
    print_tokens = True
    if print_tokens:
        print_response_tokens(response)
    
    
    ## response.choices[0].text.strip()
    return response_message


# Function to process a parent item
def get_response(prompt_text, assistant_text):

    # Prepare messages for chat completion
    chat_messages = [{'role': 'system', 'content': f'{assistant_text}.'}]
    chat_messages.append({'role': 'user', 'content': prompt_text})
    
    ## print ('Chat_messages: ', chat_messages)
    
    response_message = generate_response(assistant_text, prompt_text)
    

    return response_message