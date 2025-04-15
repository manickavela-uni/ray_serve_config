#!/bin/bash

PROTO="gliner_protos.proto"
CALL="Gliner.infer"
TARGET="localhost:9000"
DATA_FILE="payload.json"
INSECURE="--insecure"
REPORT_DIR="./reports"

mkdir -p "$REPORT_DIR"

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RESET='\033[0m'

run_test() {
    local name=$1
    local concurrency=$2
    local requests=$3
    local schedule=$4
    local output_file="$REPORT_DIR/${name// /_}.json"

    echo -e "${CYAN}▶ Running $name...${RESET}"

    # echo "ghz --insecure \
    #     --proto \"$PROTO\" \
    #     --call \"$CALL\" \
    #     --data-file \"$DATA_FILE\" \
    #     -c \"$concurrency\" \
    #     -n \"$requests\" \
    #     --name \"$name\" \
    #     --format json \
    #     --output \"$output_file\" \
    #     $schedule \
    #     \"$TARGET\"" 

    ghz --insecure \
        --proto "$PROTO" \
        --call "$CALL" \
        --data-file "$DATA_FILE" \
        -c "$concurrency" \
        -n "$requests" \
        --name "$name" \
        --format json \
        --output "$output_file" \
        $schedule \
        "$TARGET"

    if [[ ! -f "$output_file" || ! -s "$output_file" ]]; then
        echo -e "${RED}✖ Failed to generate output for $name. ghz may have crashed or no data returned.${RESET}"
        return
    fi


    echo -e "${GREEN}✔ Completed $name${RESET}"

    echo -e "${YELLOW}📊 Summary for $name:${RESET}"
    
    duration_ns=$(jq '.total' "$output_file")
    duration_ms=$((duration_ns / 1000000))
    duration_s=$((duration_ns / 1000000000))
    duration_min=$((duration_s / 60))
    duration_rem_s=$((duration_s % 60))
    duration_rem_ms=$((duration_ms % 1000))
    duration_readable="${duration_min}m:${duration_rem_s}s:${duration_rem_ms}ms"

    jq --arg duration_readable "${duration_readable}" \
    '{
        "Total Requests": .count,
        "Concurrency": (.options.concurrency // "N/A"),
        "Duration": $duration_readable,
        "RPS": (.rps // "N/A"),
        "Fastest Latency (ms)": (.fastest/1e6 // "N/A"),
        "Average Latency (ms)": (.average/1e6 // "N/A"),
        "Slowest Latency (ms)": (.slowest/1e6 // "N/A"),
        "Latency Percentiles": {
            "p10 (ms)": (.latencyDistribution[] | select(.percentage == 10).latency / 1e6),
            "p25 (ms)": (.latencyDistribution[] | select(.percentage == 25).latency / 1e6),
            "p50 (ms)": (.latencyDistribution[] | select(.percentage == 50).latency / 1e6),
            "p75 (ms)": (.latencyDistribution[] | select(.percentage == 75).latency / 1e6),
            "p90 (ms)": (.latencyDistribution[] | select(.percentage == 90).latency / 1e6),
            "p95 (ms)": (.latencyDistribution[] | select(.percentage == 95).latency / 1e6),
            "p99 (ms)": (.latencyDistribution[] | select(.percentage == 99).latency / 1e6),
        },
        "Status Codes": (.statusCodes // {})
    }' "$output_file"
}

# Test Cases
run_test "Load Test" 10 500 ""

run_test "Soak Test" 5 2000 ""

# 🔼 Spike Test - rapid increase in RPS to test burst handling
run_test "Spike Test" 10 10000 "--load-schedule=step --load-start=50 --load-end=250 --load-step=100 --load-step-duration=2s"

# 📈 Stress Test - gradual ramp-up until system breaks
run_test "Stress Test" 10 20000 "--load-schedule=step --load-start=50 --load-end=300 --load-step=25 --load-step-duration=5s --load-max-duration=90s"

echo -e "${GREEN}✅ All benchmarks completed. Raw reports are in ${REPORT_DIR}${RESET}"
