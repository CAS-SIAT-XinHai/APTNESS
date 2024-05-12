#!/usr/bin/env bash
WORK_DIR=$(dirname $(readlink -f $0))
echo "${WORK_DIR}"
UUID=$(uuidgen)
echo "${UUID}"
PID=$BASHPID
echo "$PID"

METHOD=$1
DATASET=$2
#BACKEND_PORT=$2
#FRONTEND_PORT=$3
#
#start_webui_script=$(echo "LLM_CONFIG_YAML_PATH=${WORK_DIR}/backend/config.yaml PYTHONPATH=${WORK_DIR}/src \
#  BACKENBD_PORT=$BACKEND_PORT streamlit run webui.py --server.port $FRONTEND_PORT")
#echo $start_webui_script
#screen -dmS start_webui_$PID bash -c "$start_webui_script"

OUTPUT_DIR="${WORK_DIR}"/output/${UUID}
mkdir -p "${OUTPUT_DIR}"
log_file="${OUTPUT_DIR}"/logs.txt
exec &> >(tee -a "$log_file")

PYTHONPATH="${WORK_DIR}"/src python "${WORK_DIR}"/evaluate.py --dataset "${DATASET}" --method "${METHOD}" \
  --data_dir "${WORK_DIR}"/data --prompts_dir "${WORK_DIR}"/prompts \
  --model_name gpt-3.5-turbo-0301 \
  --model_api_key sk-1 \
  --model_api_base https://api.nbfaka.com/v1 \
  --strategy_name gpt-3.5-turbo-0301 \
  --strategy_api_key sk-1 \
  --strategy_api_base https://api.nbfaka.com/v1 \
  --evaluator_name gpt-4 \
  --evaluator_api_key sk-2 \
  --evaluator_api_base https://kkkc.net/v1
