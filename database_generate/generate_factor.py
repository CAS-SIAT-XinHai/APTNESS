import json
import requests
import re

def ask_gpt(context):
    api_key = ""  # OPENAI_API_KEY
    headers = {'Content-Type': f'application/json', 'Authorization': f'Bearer {api_key}'}

    try:
        messages = [
            {
                'role': 'system',
                'content': ''
            },
            {
                'role': 'user',
                'content': context

            }
        ]
        params = {'model': "gpt-3.5-turbo",
                    'messages': messages,
                    'temperature': 0.9,
                    'max_tokens': 3000,
                    'top_p': 1,
                    'frequency_penalty': 0,
                    'presence_penalty': 0}

        r = requests.post(url="", headers=headers,
                            json=params)  
        print(r)
        openai_result = json.loads(r.text)
        #print(openai_result)
        ans = openai_result["choices"][0]["message"]["content"]
        print(ans)
    except:
        return ''
    
    return ans

with open('', 'r') as file:
    data = json.load(file)


with open('', 'r') as file:
    prompt_factor = file.read()
dataset = []
for emotion in data:
    factor_prompt = prompt_factor.replace('{emotion}', emotion)
    generated_factors = ask_gpt(factor_prompt)
    dataset.append({
            'emotinon': emotion,
            'factors': generated_factors,
        })

with open('', 'w') as file:
    json.dump(dataset, file, indent=4)