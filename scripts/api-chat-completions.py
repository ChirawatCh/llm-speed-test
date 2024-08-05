import openai

# Function to call OpenAI API with streaming response
def get_stream_response(messages, client):

    response = client.chat.completions.create(
        model="neuralmagic/Meta-Llama-3-70B-Instruct-FP8",
        messages=messages,
        max_tokens=500,
        temperature=0.01,
        stream=True
    )
    
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            
# Example usage
if __name__ == "__main__":
    url = "http://127.0.0.1:4001/v1"
    api_key = "EMPTY"
    # url = "http://10.2.2.28/llm/neuralmagic/Meta-Llama-3-70B-Instruct-FP8/v1/completions"
    # api_key = "Bearer 1234"
    client = openai.Client(base_url=url, api_key=api_key)
    # messages = [{"role": "user", "content": "Write a long essay on the topic of spring."}]
    messages = [
        {"role": "system", "content": "คุณคือผู้ช่วยคนไทย ที่เกิดในประเทศไทย ที่มีประโยชน์มากคนหนึ่ง"},
        # {"role": "user", "content": "ขอสูตรทำกระเพราไก่ไข่ดาว แบบไทยๆหน่อย ตอบเป็นภาษาไทยนะ"}]
        {"role": "user", "content": "คุณคือใคร เกิดในประเทศอะไร"}]
    get_stream_response(messages, client)