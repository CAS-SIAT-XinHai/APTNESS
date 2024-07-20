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
                    'max_tokens': 2500,
                    'top_p': 1,
                    'frequency_penalty': 0,
                    'presence_penalty': 0}

        r = requests.post(url="", headers=headers,
                            json=params)  
        print(r)
        openai_result = json.loads(r.text)
        print(openai_result)
        ans = openai_result["choices"][0]["message"]["content"]
        #print(ans)
    except:
        return ''
    
    return ans

with open('', 'r') as file:
    data = json.load(file)


with open('', 'r') as file:
    prompt_situation = file.read()
dataset = []
#data = random.sample(data,3)#["Anger","Anxiety","Depression"]
for emotion_data in data:
    emotion = emotion_data['emotinon']
    factors = emotion_data['factors']
    factors = re.sub(r'Factor\d+\: ', '', factors)
    factors = factors.replace('"', '')
    factors = factors.replace('\n\n', '\n')
    factors = factors.split('\n')[1:]
    if 'Emotion' in factors[0]:
        factors = factors[1:]
    if ']' in factors[-1]:
        factors = factors[:-2]
    #print(len(factors))
    dataset_factors = []
    for factor in factors:
        situation_prompt = prompt_situation.replace('{emotion}', emotion)
        situation_prompt = situation_prompt.replace('{factor}', factor)
        generated_situations = ask_gpt(situation_prompt)
        dataset_factors.append({
                'factor': factor,
                'situations': generated_situations,
            })
    dataset.append({
            'emotinon': emotion,
            'factors': dataset_factors,
        })

with open('', 'w') as file:
    json.dump(dataset, file, indent=4)