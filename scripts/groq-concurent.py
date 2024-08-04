import time
import threading
import os
import csv
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_KEY")

# Initialize the Groq client once with the api_key
client = Groq(api_key=GROQ_API_KEY)

# Create a lock for synchronizing print statements and file writes
write_lock = threading.Lock()

# Open the CSV file and write the header
with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Request Number", "Total Time Taken", "Prompt Tokens", "Tokens Generated", "Tokens per Second"])

def chat_completion_request_groq(messages, client, request_number):
    start_time = time.time()
    chat_response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        max_tokens=500,
        temperature=0.01,
    )

    response_time = time.time() - start_time  # Calculate response time
    
    if request_number == 1:
        print(chat_response)

    if chat_response.choices:
        completion_text = chat_response.choices[0].message.content
    else:
        completion_text = None

    # Extract the required values
    prompt_tokens = chat_response.usage.prompt_tokens if completion_text else 0
    queue_time = chat_response.usage.queue_time if chat_response.usage.queue_time is not None else 0
    tokens_generated = chat_response.usage.completion_tokens if completion_text else 0
    tokens_per_second = tokens_generated / response_time if response_time > 0 else 0

    with write_lock:
        # Print the results
        print("")
        print(f"---------- Request #{request_number} ----------")
        print(f"Total Time Taken: {response_time:.2f} seconds")
        print(f"Queue ttime: {queue_time:.2f}")
        print(f"Prompt tokens: {prompt_tokens:.2f}")
        print(f"Tokens generated: {tokens_generated:.2f}")
        print(f"Tokens per second: {tokens_per_second:.2f}")

        # Write the results to the CSV file
        with open('results.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([request_number, f"{response_time:.2f}", f"{prompt_tokens:.2f}", f"{tokens_generated:.2f}", f"{tokens_per_second:.2f}"])

    return chat_response

def send_request_every_x_seconds(num_requests):
    for i in range(num_requests):
        threading.Timer(0.06125 * i, send_request, args=(i + 1,)).start()

def send_request(request_number):
    messages = [
        {"role": "user", "content": "Write a long essay on the topic of spring."}
    ]
    chat_completion_request_groq(messages, client, request_number)
    

if __name__ == "__main__":
    num_requests = 64  # Specify the number of requests here
    send_request_every_x_seconds(num_requests)
    