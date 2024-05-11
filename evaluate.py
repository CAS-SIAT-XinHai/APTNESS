import argparse
import json

from aptness.evaluations.aptness import APTNESSEvaluator
from aptness.evaluations.base import BaseEvaluator
from aptness.evaluations.rag import RAGEvaluator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="APTNESS evaluator")
    datasets = ['ed', 'extes']
    parser.add_argument("-d", "--dataset", default="ed", type=str,
                        help="one of: {}".format(", ".join(sorted(datasets))))
    parser.add_argument("-dd", "--data_dir", default="data", type=str,
                        help="data directory")
    parser.add_argument("-pd", "--prompts_dir", default="prompts", type=str,
                        help="prompts directory")
    methods = ['baseline', 'rag', 'aptness']
    parser.add_argument("-m", "--method", default="data", type=str,
                        help="Methods used for generation.")

    parser.add_argument('--model_name', type=str, help='bar help')
    parser.add_argument('--model_api_key', type=str, help='bar help')
    parser.add_argument('--model_api_base', type=str, help='bar help')

    parser.add_argument('--strategy_name', type=str, help='bar help')
    parser.add_argument('--strategy_api_key', type=str, help='bar help')
    parser.add_argument('--strategy_api_base', type=str, help='bar help')

    parser.add_argument('--evaluator_name', type=str, help='bar help')
    parser.add_argument('--evaluator_api_key', type=str, help='bar help')
    parser.add_argument('--evaluator_api_base', type=str, help='bar help')

    args = parser.parse_args()

    print(args)

    with open(f"{args.data_dir}/{args.dataset}.json") as fd:
        test_data = json.load(fd)

    if args.method == 'baseline':
        evaluator = BaseEvaluator(
            model_name=args.model_name,
            model_api_key=args.model_api_key,
            model_api_base=args.model_api_base,
            evaluator_name=args.evaluator_name,
            evaluator_api_key=args.evaluator_api_key,
            evaluator_api_base=args.evaluator_api_base,
            data_dir=args.data_dir,
            prompts_dir=args.prompts_dir,
        )
    elif args.method == 'rag':
        evaluator = RAGEvaluator(
            model_name=args.model_name,
            model_api_key=args.model_api_key,
            model_api_base=args.model_api_base,
            evaluator_name=args.evaluator_name,
            evaluator_api_key=args.evaluator_api_key,
            evaluator_api_base=args.evaluator_api_base,
            data_dir=args.data_dir,
            prompts_dir=args.prompts_dir,
        )
    elif args.method == 'aptness':
        evaluator = APTNESSEvaluator(
            model_name=args.model_name,
            model_api_key=args.model_api_key,
            model_api_base=args.model_api_base,
            strategy_name=args.strategy_name,
            strategy_api_key=args.strategy_api_key,
            strategy_api_base=args.strategy_api_base,
            evaluator_name=args.evaluator_name,
            evaluator_api_key=args.evaluator_api_key,
            evaluator_api_base=args.evaluator_api_base,
            data_dir=args.data_dir,
            prompts_dir=args.prompts_dir,
        )
    else:
        raise NotImplementedError

    evaluator.run(test_data)
