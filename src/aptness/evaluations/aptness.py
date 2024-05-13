import re

from more_itertools import flatten
from openai import OpenAI

from .rag import RAGEvaluator
from ..strategies import STRATEGIES


class APTNESSEvaluator(RAGEvaluator):

    def __init__(self,
                 model_name,
                 model_api_key,
                 model_api_base,
                 strategy_name,
                 strategy_api_key,
                 strategy_api_base,
                 evaluator_name,
                 evaluator_api_key,
                 evaluator_api_base,
                 strategy,
                 data_dir,
                 prompts_dir):
        super().__init__(model_name, model_api_key, model_api_base,
                         evaluator_name, evaluator_api_key, evaluator_api_base, data_dir, prompts_dir)
        self.strategy_name = strategy_name
        self.strategy_client = OpenAI(
            api_key=strategy_api_key,
            base_url=strategy_api_base,
        )
        self.strategies = STRATEGIES[strategy]

        self.strategy_prediction_prompt = open(f"{prompts_dir}/strategy_prediction_prompt.txt").read()
        self.aug_prompt_with_strategies = open(f"{prompts_dir}/aug_prompt_with_strategies.txt").read()

    def generate_response_strategy(self, dialogue, num_retries=5):
        strategy_generate_prompt = self.strategy_prediction_prompt.format(dialogue_context=dialogue)
        messages = [
            {
                "role": "user",
                "content": strategy_generate_prompt,
            }
        ]

        strategies = "|".join(self.strategies.keys())

        while num_retries:
            chat_response = self.chat_completion(self.strategy_client, model=self.strategy_name, messages=messages)
            if chat_response:
                chat_strategy = re.findall(rf'\b(?:{strategies})\b', chat_response)
                return chat_strategy
            num_retries -= 1

    def generate_rag_response_with_strategies(self, dialogue_context, strategy_retrieve_responses, num_retries=5):
        context_history = '\n'.join(dialogue_context)
        responses = "\n".join([f"[Response {i}]\n{cr['response']}\n[End of Response {i}]\n" for i, cr in
                               enumerate(strategy_retrieve_responses)])
        strategies = "\n".join(
            [f"[Strategy {i}]\n{st}: {self.strategies[st]}\n[End of Strategy {i}]\n" for i, st in
             enumerate(set(flatten([cr['strategy'] for cr in strategy_retrieve_responses])))])

        messages = [
            {
                "role": "user",
                "content": self.aug_prompt_with_strategies.format(dialogue=context_history,
                                                                  responses=responses,
                                                                  strategies=strategies),
            }
        ]

        while num_retries:
            chat_response = self.chat_completion(self.model_client, model=self.model_name, messages=messages)
            if chat_response:
                rr = self.rag_response_pattern.findall(chat_response)
                if rr:
                    return rr[0]

            print(f"Error try from {self.strategy_name}: {num_retries}")
            num_retries -= 1

    def enhance_response(self, dialogue, response, num_retries=5):
        retrieved_responses = self.retriever.retrieve(response)
        candidate_responses_with_strategies = []
        for d, r in [(dialogue, response)] + [(self.reversed_responses[r.text], r.text) for r in retrieved_responses]:
            s = None
            while not s:
                s = self.generate_response_strategy(d)
            candidate_responses_with_strategies.append({"strategy": s, "response": r})

        rag_response = None
        while not rag_response:
            rag_response = self.generate_rag_response_with_strategies(dialogue,
                                                                      candidate_responses_with_strategies,
                                                                      num_retries)

        # 增加去噪功能
        return rag_response.strip()
