
import requests ,json
def openai_title(titles):
    # Set up your OpenAI API key
    api_key = 'sk-proj-x0Jhg1qaVTCRu5FXz0O5T3BlbkFJhQk8no3fcGZzMk5n8IBI'

    # Endpoint for OpenAI's GPT-4 API
    url = "https://api.openai.com/v1/chat/completions"

    # Headers including the authorization
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Concatenate titles into a single prompt
    prompt = f"Create a 5-6 line narrator introduction for the following post content for youtube video script:\n\n{titles}\n\nNarrator Intro:"
    

    # The data payload for the API request
    data = {
        "model": "gpt-3.5-turbo",  # Specify the model you want to use
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that generates common titles."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,  # You can adjust this value as needed
        "temperature": 0.5  # Adjust the creativity level (0.0 - 1.0)
    }

    # Making the POST request to the API
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the response JSON
        response_data = response.json()
        # Extracting and printing the assistant's response
        generated_title = response_data['choices'][0]['message']['content'].strip()
        return generated_title
 


def openai_close(titles):
    # Set up your OpenAI API key
    api_key = 'sk-proj-x0Jhg1qaVTCRu5FXz0O5T3BlbkFJhQk8no3fcGZzMk5n8IBI'

    # Endpoint for OpenAI's GPT-4 API
    url = "https://api.openai.com/v1/chat/completions"

    # Headers including the authorization
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Concatenate titles into a single prompt
    prompt = f"Create a 5-6 line narrator closing for the following post content for youtube video script:\n\n{titles}\n\nNarrator Closing:"
    

    # The data payload for the API request
    data = {
        "model": "gpt-3.5-turbo",  # Specify the model you want to use
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that generates common titles."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,  # You can adjust this value as needed
        "temperature": 0.5  # Adjust the creativity level (0.0 - 1.0)
    }

    # Making the POST request to the API
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the response JSON
        response_data = response.json()
        # Extracting and printing the assistant's response
        generated_title = response_data['choices'][0]['message']['content'].strip()
        return generated_title
 