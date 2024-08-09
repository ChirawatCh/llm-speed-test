import openai

url = "http://10.2.2.28/llm/neuralmagic/Meta-Llama-3-70B-Instruct-FP8/v1"
api_key = "1234"

# url = "http://127.0.0.1:4001/v1"
# api_key = "EMPTY"

client = openai.Client(
    base_url=url, api_key=api_key)

response = client.completions.create(
	model="default",
	prompt="Write a long essay on the topic of spring.",
	temperature=0.01,
	max_tokens=500,
)
print(response)

# Chat completion
response = client.chat.completions.create(
    model="default",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant"},
        {"role": "user", "content": "Write a long essay on the topic of spring."},
    ],
    temperature=0.01,
    max_tokens=500,
)
print(response)