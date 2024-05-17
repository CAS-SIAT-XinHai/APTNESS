import json
import os
import os.path
import re

from llama_index.core import Settings, VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.readers import StringIterableReader
from llama_index.embeddings.ollama import OllamaEmbedding
from more_itertools import flatten

from .base import BaseEvaluator


class RAGEvaluator(BaseEvaluator):

    def __init__(self,
                 model_name,
                 model_api_key,
                 model_api_base,
                 evaluator_name,
                 evaluator_api_key,
                 evaluator_api_base,
                 data_dir,
                 prompts_dir):
        super().__init__(model_name, model_api_key, model_api_base, evaluator_name, evaluator_api_key,
                         evaluator_api_base, data_dir, prompts_dir)

        print("Loading data from database and constructing vector store: ")
        with open(f"{data_dir}/database.json") as fd:
            data_for_retrieval = json.load(fd)

        responses = []
        self.reversed_responses = {}
        for item in data_for_retrieval:
            retrieve_conv = item['history'].copy() + [[item['instruction'], item['output']]]
            for i, (speaker, listener) in enumerate(retrieve_conv):
                responses.append(listener)
                self.reversed_responses[listener.strip()] = list(
                    flatten([["Speaker: {}".format(s), "Listener: {}".format(l)] for s, l in
                             retrieve_conv[:i]])) + ["Speaker: {}".format(speaker)]

        print("Loading index start: ")
        # nomic embedding model
        Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
        Settings.llm = None
        storage_dir = f"{data_dir}/database_index"
        if os.path.isdir(storage_dir):
            # rebuild storage context
            storage_context = StorageContext.from_defaults(persist_dir=storage_dir)

            # load index
            index = load_index_from_storage(storage_context, show_progress=True)
        else:
            documents = StringIterableReader().load_data(texts=responses)

            index = VectorStoreIndex.from_documents(documents, show_progress=True)
            index.storage_context.persist(persist_dir=storage_dir)

        self.retriever = index.as_retriever(similarity_top_k=2)
        print("Loading index end!")

        self.aug_prompt = open(f"{prompts_dir}/aug_prompt.txt").read()
        self.rag_response_pattern = re.compile(r"\[Response]([\s\S]+)\[End of Response]")
        self.rag_long_response_pattern = re.compile(r"\[Response]([\s\S]+)")

    @staticmethod
    def retrieve_augment_re(retrieve_augment_response):
        retrieve_augment_response = re.sub(r'.*?:\s*', '', retrieve_augment_response)
        retrieve_augment_response = retrieve_augment_response.replace('"','')
        retrieve_augment_response = re.sub(r'\b(?:Of course).*?[.!?]', '', retrieve_augment_response, flags=re.IGNORECASE)
        retrieve_augment_response = re.sub(r'\b(?:Sure).*?[.!?]', '', retrieve_augment_response, flags=re.IGNORECASE)
        retrieve_augment_response = retrieve_augment_response.replace('As the listener,','')
        retrieve_augment_response = retrieve_augment_response.replace('Listener:','')
        retrieve_augment_response = retrieve_augment_response.strip()
        
        return retrieve_augment_response

    def generate_rag_response(self, dialogue_context, candidate_responses, num_retries=10):
        context_history = '\n'.join(dialogue_context)
        responses = "\n".join(
            [f"[Response {i}]\n{cr}\n[End of Response {i}]\n" for i, cr in enumerate(candidate_responses)])
        retrieve_augment_prompt = self.aug_prompt.format(dialogue=context_history,
                                                         responses=responses)
        messages = [
            {
                "role": "user",
                "content": retrieve_augment_prompt,
            }
        ]

        while num_retries:
            chat_response = self.chat_completion(self.model_client, model=self.model_name, messages=messages)
            if chat_response:
                ##return chat_response
                rr = self.rag_response_pattern.findall(chat_response)
                if rr:
                    return rr[0]
                if num_retries == 1:
                    rr = self.rag_long_response_pattern.findall(chat_response)
                    if rr:
                        return rr[0]

            print(f"Error try from {self.model_name}: {num_retries}")
            num_retries -= 1

    def enhance_response(self, dialogue, response, num_retries=10):
        retrieved_responses = [r.text for r in self.retriever.retrieve(response)]
        print("Retrieved responses:", retrieved_responses)

        candidate_responses = [response] + retrieved_responses

        rag_response = None
        while not rag_response:
            rag_response = self.generate_rag_response(dialogue, candidate_responses, num_retries)

        # 增加去噪功能
        return rag_response.strip()
