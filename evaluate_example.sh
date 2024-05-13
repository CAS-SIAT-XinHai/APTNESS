#!/usr/bin/env bash
WORK_DIR=$(dirname $(readlink -f $0))
echo "${WORK_DIR}"
UUID=$(uuidgen)
echo "${UUID}"
PID=$BASHPID
echo "$PID"

METHOD=$1
DATASET=$2
STRATEGY=$3

#start_webui_script=$(echo "LLM_CONFIG_YAML_PATH=${WORK_DIR}/backend/config.yaml PYTHONPATH=${WORK_DIR}/src \
#  BACKENBD_PORT=$BACKEND_PORT streamlit run webui.py --server.port $FRONTEND_PORT")
#echo $start_webui_script
#screen -dmS start_webui_$PID bash -c "$start_webui_script"

OUTPUT_DIR="${WORK_DIR}"/output/${UUID}
mkdir -p "${OUTPUT_DIR}"
log_file="${OUTPUT_DIR}"/logs.txt
exec &> >(tee -a "$log_file")

if [ -z "$STRATEGY" ]; then
  PYTHONPATH="${WORK_DIR}"/src python "${WORK_DIR}"/evaluate.py \
    --dataset "${DATASET}" --method "${METHOD}" \
    --data_dir "${WORK_DIR}"/data --prompts_dir "${WORK_DIR}"/prompts \
    --model_name mixtral \
    --model_api_key "EMPTY" \
    --model_api_base http://localhost:40001/v1 \
    --evaluator_name gpt-4 \
    --evaluator_api_key sk- \
    --evaluator_api_base
else
  PYTHONPATH="${WORK_DIR}"/src python "${WORK_DIR}"/evaluate.py \
    --dataset "${DATASET}" --method "${METHOD}" --strategy "${STRATEGY}" \
    --data_dir "${WORK_DIR}"/data --prompts_dir "${WORK_DIR}"/prompts \
    --model_name mixtral \
    --model_api_key "EMPTY" \
    --model_api_base http://localhost:40001/v1 \
    --strategy_name mixtral \
    --strategy_api_key "EMPTY" \
    --strategy_api_base http://localhost:40002/v1 \
    --evaluator_name gpt-4 \
    --evaluator_api_key sk- \
    --evaluator_api_base
fi
