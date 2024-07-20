import json
import requests
import re
def ask_gpt4(context):
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
        params = {'model': "gpt-4",
                    'messages': messages,
                    'temperature': 0,
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
                    'max_tokens': 2500,
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
###stage2####
with open('', 'r') as file:
    data = json.load(file)

with open('', 'r') as file:
    prompt_stage2 = file.read()
dataset = []
for emotion_data in data:
    emotion = emotion_data['emotinon']
    factors = []
    for factor_data in emotion_data['factors']:
        factor = factor_data['factor']  
        situations = []      
        for situation_data in factor_data['situations']:
            situation = situation_data['situation']
            first_sentences = situation_data['first_sentence']
            first_sentences = re.sub(r'\d+\.', '', first_sentences)
            first_sentences = first_sentences.replace('"', '')
            first_sentences = first_sentences.replace('\n\n', '\n')
            first_sentences = first_sentences.split('\n')
            #print(first_sentences)
            stage2_generate_dialogues = []
            for first_sentence in first_sentences: 
                if first_sentence == '':
                    continue
                stage2_prompt = prompt_stage2.replace('{situation}', situation)
                stage2_prompt = stage2_prompt.replace('{factor}', factor)
                stage2_prompt = stage2_prompt.replace('{emotion}', emotion)
                stage2_prompt = stage2_prompt.replace('{first_sentence}', first_sentence)    
                #print(stage2_prompt)
                stage2_generate_dialogue = ask_gpt(stage2_prompt)

                if stage2_generate_dialogue == '':  
                    stage2_generate_dialogue = ask_gpt(stage2_prompt)
                stage2_generate_dialogue_len = stage2_generate_dialogue.replace('\n\n', '\n')
                stage2_generate_dialogue_len = stage2_generate_dialogue_len.split('\n')     
                if len(stage2_generate_dialogue_len) < 4: 
                    stage2_generate_dialogue = ask_gpt(stage2_prompt) 
                stage2_generate_dialogues.append(stage2_generate_dialogue)
            situations.append({
                'situation': situation,
                'stage2_generate_dialogues': stage2_generate_dialogues,
            })
        factors.append({
                'factor': factor,
                'situations': situations,
            })
    dataset.append({
                'emotinon': emotion,
                'factors': factors,
            })

with open('', 'w') as file:
    json.dump(dataset, file, indent=4)