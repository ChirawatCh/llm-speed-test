import time
import threading
import os
import openai
import csv

client = openai.Client(
    base_url="http://127.0.0.1:4001/v1", api_key="EMPTY")

# Create a lock for synchronizing print statements and file writes
write_lock = threading.Lock()

# Open the CSV file and write the header
with open('csv-result/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Request Number", "Total Time Taken", "Prompt Tokens", "Tokens Generated", "Tokens per Second"])

def chat_completion_request(messages, client, request_number):
    start_time = time.time()
    chat_response = client.chat.completions.create(
        model="default",
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
    tokens_generated = chat_response.usage.completion_tokens if completion_text else 0
    tokens_per_second = tokens_generated / response_time if response_time > 0 else 0

    with write_lock:
        # Print the results
        print("")
        print(f"---------- Request #{request_number} ----------")
        print(f"Total Time Taken: {response_time:.2f} seconds")
        print(f"Prompt tokens: {prompt_tokens:.2f}")
        print(f"Tokens generated: {tokens_generated:.2f}")
        print(f"Tokens per second: {tokens_per_second:.2f}")

        # Write the results to the CSV file
        with open('csv-result/results.csv', 'a', newline='') as file:
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
    chat_completion_request(messages, client, request_number)
    

if __name__ == "__main__":
    num_requests = 64  # Specify the number of requests here
    send_request_every_x_seconds(num_requests)
    