import re
import sys

def extract_and_filter_metrics(content):
    # Define metrics and their regex patterns
    metrics_patterns = {
        "Simulated Time (Seconds)": r"simSeconds\s+([\d\.e\-]+)",
        "L1 Cache Hit Rate": r"system\.cpu\.icache\.overallHits::total\s+(\d+)",
        "L2 Cache Hit Rate": r"system\.cpu\.dcache\.overallHits::total\s+(\d+)",
        "DRAM Accesses": r"system\.mem_ctrl\.dram\.numReads::total\s+(\d+)",
        "Execution Ticks": r"system\.cpu\.numCycles\s+(\d+)",
        "Instructions Executed": r"system\.cpu\.commitStats0\.numInsts\s+(\d+)",
        "CPI": r"system\.cpu\.cpi\s+([\d\.]+)",
        "Average Memory Latency": r"system\.cpu\.dcache\.overallAvgMissLatency::total\s+(\d+)",
        "Branch Prediction Lookups": r"system\.cpu\.branchPred\.lookups\s+(\d+)",
        "Branch Mispredictions": r"system\.cpu\.branchPred\.condIncorrect\s+(\d+)",
    }

    # Extract metrics from content
    metrics = {}
    for metric, pattern in metrics_patterns.items():
        match = re.search(pattern, content)
        metrics[metric] = match.group(1) if match else "Not Found"

    # Calculate derived metrics
    try:
        l1_hits = int(re.search(metrics_patterns["L1 Cache Hit Rate"], content).group(1))
        l1_accesses = int(re.search(r"system\.cpu\.icache\.overallAccesses::total\s+(\d+)", content).group(1))
        metrics["L1 Cache Hit Rate"] = f"{(l1_hits / l1_accesses) * 100:.2f}%" if l1_accesses else "Not Found"
    except:
        metrics["L1 Cache Hit Rate"] = "Not Found"

    try:
        l2_hits = int(re.search(metrics_patterns["L2 Cache Hit Rate"], content).group(1))
        l2_accesses = int(re.search(r"system\.cpu\.dcache\.overallAccesses::total\s+(\d+)", content).group(1))
        metrics["L2 Cache Hit Rate"] = f"{(l2_hits / l2_accesses) * 100:.2f}%" if l2_accesses else "Not Found"
    except:
        metrics["L2 Cache Hit Rate"] = "Not Found"

    # Calculate Branch Prediction Accuracy
    try:
        branch_lookups = int(re.search(metrics_patterns["Branch Prediction Lookups"], content).group(1))
        branch_mispredictions = int(re.search(metrics_patterns["Branch Mispredictions"], content).group(1))
        metrics["Branch Prediction Accuracy"] = f"{(1 - (branch_mispredictions / branch_lookups)) * 100:.2f}%" if branch_lookups else "Not Found"
    except:
        metrics["Branch Prediction Accuracy"] = "Not Found"

    return metrics

# Example usage with the provided input data
with open(sys.argv[1], 'r') as file:  # Replace with your actual file
    content = file.read()

results = extract_and_filter_metrics(content)

# Print results
for metric, value in results.items():
    print(f"{metric}: {value}")
