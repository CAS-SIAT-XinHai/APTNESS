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
def has_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    return bool(pattern.search(text))

with open('', 'r') as file:
    data = json.load(file)

with open('', 'r') as file:
    prompt_stage2 = file.read()

with open('', 'r') as file:
    prompt_stage3 = file.read()
dataset = []
for emotion_data in data:
    emotion = emotion_data['emotinon']
    factors = []
    for factor_data in emotion_data['factors']:
        factor = factor_data['factor']  
        situations = []      
        for situation_data in factor_data['situations']:
            situation = situation_data['situation']
            stage2_generate_dialogues = situation_data['stage2_generate_dialogues']
            stage3_generate_dialogues = []
            dialogue_historys = []
            baseline_dialogues = []
            for stage2_generate_dialogue in stage2_generate_dialogues:
                dialogue_history = stage2_generate_dialogue.replace('\n\n', '\n')
                dialogue_history = dialogue_history.split('\n')  
                if "####" in dialogue_history[0]:
                    dialogue_history = dialogue_history[1:]
                for dialogue_sentence in dialogue_history:
                    #print(dialogue_sentence)
                    if dialogue_sentence == '':
                        value_to_remove = ''
                        dialogue_history = [x for x in dialogue_history if x != value_to_remove]    
                    first_sentence = dialogue_history[0]
                    stage2_prompt = prompt_stage2.replace('{situation}', situation)
                    stage2_prompt = stage2_prompt.replace('{factor}', factor)
                    stage2_prompt = stage2_prompt.replace('{emotion}', emotion)
                    stage2_prompt = stage2_prompt.replace('{first_sentence}', first_sentence)  
                    stage2_generate_dialogue = ask_gpt(stage2_prompt)
                    dialogue_history = stage2_generate_dialogue.replace('\n\n', '\n')
                    dialogue_history = dialogue_history.split('\n')
                baseline_dialogue = '\n'.join(dialogue_history)
                baseline_dialogues.append(baseline_dialogue)
                if len(dialogue_history) % 2 == 1:
                    dialogue_history = '\n'.join(dialogue_history[:-2])
                else:
                    dialogue_history = '\n'.join(dialogue_history[:-1])
                dialogue_historys.append(dialogue_history)
                stage3_prompt = prompt_stage3.replace('{situation}', situation)
                stage3_prompt = stage3_prompt.replace('{factor}', factor)
                stage3_prompt = stage3_prompt.replace('{emotion}', emotion)
                stage3_prompt = stage3_prompt.replace('{dialogue}', dialogue_history)
                stage3_generate_response = ask_gpt(stage3_prompt) 
                if stage3_generate_response == '':   
                    stage3_generate_response = ask_gpt(stage3_prompt) 
                stage3_generate_dialogues.append(stage3_generate_response)
            situations.append({
                'situation': situation,
                'dialogue_historys': dialogue_historys,
                'stage3_generate_responses': stage3_generate_dialogues,
                'baseline_dialogues': baseline_dialogues,
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

           