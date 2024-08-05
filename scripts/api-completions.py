import openai

# client = openai.Client(
#     base_url="http://127.0.0.1:4001/v1", api_key="EMPTY")

client = openai.Client(
    base_url="http://10.2.2.28/llm/neuralmagic/Meta-Llama-3-70B-Instruct-FP8/v1/completions", api_key="Bearer 1234")

# Text completion
response = client.completions.create(
	model="neuralmagic/Meta-Llama-3-70B-Instruct-FP8",
	prompt="Write a long essay on the topic of spring.",
	temperature=0.01,
	max_tokens=500,
)
print(response)
