import requests
import json

# Set the API endpoint and headers
url = "http://10.2.2.28/llm/neuralmagic/Meta-Llama-3-70B-Instruct-FP8/v1/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 1234"
}

# Define the payload
payload = {
    "model": "neuralmagic/Meta-Llama-3-70B-Instruct-FP8",
    "prompt": "Write a long essay on the topic of spring.",
    "temperature": 0.01
}

# Function to make the request and handle streaming response
def get_stream_response(url, headers, payload):
    with requests.post(url, headers=headers, data=json.dumps(payload), stream=True) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                data = json.loads(chunk.decode('utf-8'))
                if 'choices' in data:
                    for choice in data['choices']:
                        print(choice['text'], end='', flush=True)

# Example usage
if __name__ == "__main__":
    get_stream_response(url, headers, payload)