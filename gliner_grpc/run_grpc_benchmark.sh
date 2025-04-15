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
RED='\033[0;31m'
RESET='\033[0m'

# Function to format nanoseconds to human-readable ms
format_duration_ms() {
    local ns=$1
    awk "BEGIN { printf \"%.3f\", $ns / 1e6 }"
}

run_test() {
    local name=$1
    local concurrency=$2
    local requests=$3
    local schedule=$4
    local output_file="$REPORT_DIR/${name// /_}.json"

    echo -e "${CYAN}▶ Running $name...${RESET}"

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

    jq '{
        "Total Requests": .count,
        "Concurrency": (.options.concurrency // "N/A"),
        "Duration (ms)": (.total/1e6),
        "RPS": (.rps/1e6 // "N/A"),
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
            "p99 (ms)": (.latencyDistribution[] | select(.percentage == 99).latency / 1e6)
        },
        "Status Codes": (.statusCodes // {})
    }' "$output_file"
}

# ========================
# Command Line Args
# ========================
TEST_TYPE=$1

if [[ -z "$TEST_TYPE" ]]; then
    echo -e "${RED}Usage: $0 [load|soak|spike|stress]${RESET}"
    exit 1
fi

case "$TEST_TYPE" in
    load)
        run_test "Load Test" 10 500 ""
        ;;
    soak)
        run_test "Soak Test" 5 2000 ""
        ;;
    spike)
        run_test "Spike Test" 50 500 "--load-schedule=step --load-start=20 --load-end=100 --load-step=20 --load-step-duration=2s"
        ;;
    stress)
        run_test "Stress Test" 10 20000 "--load-schedule=step --load-start=50 --load-end=300 --load-step=25 --load-step-duration=5s --load-max-duration=90s"
        ;;
    *)
        echo -e "${RED}Invalid option: $TEST_TYPE. Choose from [load|soak|spike|stress].${RESET}"
        exit 1
        ;;
esac

echo -e "${GREEN}✅ Test '$TEST_TYPE' completed. Raw reports are in ${REPORT_DIR}${RESET}"
