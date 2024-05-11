import json
import re
from collections import Counter

from openai import OpenAI, OpenAIError


class BaseEvaluator(object):

    def __init__(self,
                 model_name, model_api_key, model_api_base,
                 evaluator_name, evaluator_api_key, evaluator_api_base, data_dir, prompts_dir):
        self.model_name = model_name
        self.model_client = OpenAI(
            api_key=model_api_key,
            base_url=model_api_base,
        )

        self.evaluator_name = evaluator_name
        self.evaluator_client = OpenAI(
            api_key=evaluator_api_key,
            base_url=evaluator_api_base,
        )

        self.data_dir = data_dir
        self.prompts_dir = prompts_dir

        self.score_prompt = open(f"{self.prompts_dir}/score_prompt.txt").read()

        self.all_evaluate_results = {}
        self.evaluate_results = Counter()

    @staticmethod
    def chat_completion(client, model, messages):
        try:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(f"Sending messages to {model}: {messages}")
            chat_response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print(f"Get response from {model}: {chat_response.choices[0].message.content}")
            return chat_response.choices[0].message.content
        except OpenAIError as e:
            # Handle all OpenAI API errors
            print("*****************************************")
            print(f"Error response from {model}: {e}")

    def complete_conversation(self, conversation, num_retries=5):
        dialogue_context = []
        messages = []
        for i, (speaker, listener) in enumerate(conversation):
            messages.append({
                "role": "user",
                "content": speaker
            })
            dialogue_context.append("Speaker: {}".format(speaker))

            while num_retries:
                chat_response = self.chat_completion(self.model_client, model=self.model_name, messages=messages)
                if chat_response:
                    yield dialogue_context.copy(), chat_response
                    break
                num_retries -= 1

            messages.append({
                "role": "assistant",
                "content": listener
            })
            dialogue_context.append("Listener: {}".format(listener))

    def score(self, dialogue, response, num_retries=5):
        messages = [
            {
                'role': 'system',
                'content': ''
            },
            {
                "role": "user",
                "content": self.score_prompt.format(dialogue_context="\n".join(dialogue), response=response),
            }
        ]

        while num_retries:
            chat_response = self.chat_completion(self.evaluator_client, model=self.evaluator_name, messages=messages)
            if chat_response:
                evaluate_ans = re.findall(r'\{(?:[^{}]|(?:\{(?:[^{}])*?\}))*?\}', chat_response)
                if evaluate_ans:
                    evaluate_ans = evaluate_ans[0]
                    try:
                        return json.loads(evaluate_ans)
                    except Exception as e:
                        print(f"Evaluation {evaluate_ans} error:", e)
            num_retries -= 1

    def enhance_response(self, dialogue, response, num_retries=5):
        return response

    def run(self, test_data, num_retries=5):
        for item in test_data:
            print("=============================================================")
            conv = item['history'].copy() + [[item['instruction'], item['output']]]
            evaluate_seq_results = Counter()
            print("---------------------------------------------------------------")
            for turn_num, (msg, rsp) in enumerate(self.complete_conversation(conv)):
                rsp = self.enhance_response(msg, rsp, num_retries)
                s = self.score(msg, rsp, num_retries=num_retries)
                evaluate_seq_results.update({k: v / len(conv) for k, v in s.items()})
                print("---------------------------------------------------------------")
            self.evaluate_results.update({k: v / len(test_data) for k, v in evaluate_seq_results.items()})
        print(self.evaluate_results)
