import openai
import os
# 建立 GPT 3.5-16k 模型
def get_reply(messages):
  openai.api_key = os.getenv('OPENAI_API_KEY')
 
  try:
    response = openai.ChatCompletion.create(
      # 由於新聞資料量常常超越gpt-3.5-turbo模型的token限制,所以將模型替換成16K,以處理更大的文本量
      model="gpt-3.5-turbo-1106",
      messages=messages)
    reply = response["choices"][0]["message"]["content"]
  except openai.OpenAIError as err:
    reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
  return reply