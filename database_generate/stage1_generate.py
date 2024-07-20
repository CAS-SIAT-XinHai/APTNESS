import json
import requests
import re

def ask_gpt(context):
    api_key = "sk-"  # OPENAI_API_KEY
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
###stage1####
with open('', 'r') as file:
    data = json.load(file)
with open('', 'r') as file:
    prompt_stage1 = file.read()
dataset = []
for emotion_data in data:
    emotion = emotion_data['emotinon']
    factors = []
    for factor_data in emotion_data['factors']:
        factor = factor_data['factor']
        situations = factor_data['situations']
        situations = re.sub(r'Situation\d+\: ', '', situations)
        situations = situations.replace('"', '')
        situations = situations.replace('\n\n', '\n')
        situations = situations.split('\n')
        if 'Emotion' in situations[0]:
            situations = situations[2:] 
            
        #print(situations)
        situation_dataset = []           
        for situation in situations:
            if "[" in situation:
                continue
            #print(emotion,factor,situation)
            stage1_prompt = prompt_stage1.replace('{situation}', situation)
            stage1_prompt = stage1_prompt.replace('{factor}', factor)
            stage1_prompt = stage1_prompt.replace('{emotion}', emotion)
            #print(emotion,factor,situation)
            #print(stage1_prompt)
            generated_first_sentence = ask_gpt(stage1_prompt)
            situation_dataset.append({
                'situation': situation,
                'first_sentence': generated_first_sentence,
            })
        
        factors.append({
                'factor': factor,
                'situations': situation_dataset,
            })
    dataset.append({
                'emotinon': emotion,
                'factors': factors,
            })
with open('', 'w') as file:
    json.dump(dataset, file, indent=4)