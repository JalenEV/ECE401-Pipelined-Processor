import re
import sys

def extract_metrics(file_path):
    metrics = {
        "l1_hit_rate": None,
        "l2_hit_rate": None,
        "dram_accesses": None,
        "execution_ticks": None,
        "avg_memory_latency": None,
        "branch_lookups": None,
        "branch_mispredictions": None,
        "branch_accuracy": None,
        "instructions_executed": None,
        "cpi": None
    }

    with open(file_path, 'r') as file:
        content = file.read()

        # Cache hit rates
        l1_hits = int(re.search(r'system\.cpu\.icache\.overallHits::total\s+(\d+)', content).group(1))
        l1_accesses = int(re.search(r'system\.cpu\.icache\.overallAccesses::total\s+(\d+)', content).group(1))
        l2_hits = int(re.search(r'system\.cpu\.dcache\.overallHits::total\s+(\d+)', content).group(1))
        l2_accesses = int(re.search(r'system\.cpu\.dcache\.overallAccesses::total\s+(\d+)', content).group(1))

        metrics["l1_hit_rate"] = l1_hits / l1_accesses if l1_accesses else None
        metrics["l2_hit_rate"] = l2_hits / l2_accesses if l2_accesses else None

        # DRAM accesses
        dram_accesses = re.search(r'system\.mem_ctrl\.dram\.numReads::total\s+(\d+)', content)
        if dram_accesses:
            metrics["dram_accesses"] = int(dram_accesses.group(1))

        # Execution ticks
        execution_ticks = re.search(r'system\.cpu\.numCycles\s+(\d+)', content)
        if execution_ticks:
            metrics["execution_ticks"] = int(execution_ticks.group(1))

        # Instructions executed
        instructions_executed = re.search(r'system\.cpu\.commitStats0\.numInsts\s+(\d+)', content)
        if instructions_executed:
            metrics["instructions_executed"] = int(instructions_executed.group(1))

        # Calculate CPI
        if metrics["execution_ticks"] and metrics["instructions_executed"]:
            metrics["cpi"] = metrics["execution_ticks"] / metrics["instructions_executed"]

        # Average memory latency
        memory_latency = re.search(r'system\.cpu\.dcache\.overallAvgMissLatency::total\s+(\d+)', content)
        if memory_latency:
            metrics["avg_memory_latency"] = int(memory_latency.group(1))

        # Branch prediction metrics
        branch_lookups = re.search(r'system\.cpu\.branchPred\.lookups\s+(\d+)', content)
        if branch_lookups:
            metrics["branch_lookups"] = int(branch_lookups.group(1))

        branch_mispredictions = re.search(r'system\.cpu\.branchPred\.condIncorrect\s+(\d+)', content)
        if branch_mispredictions:
            metrics["branch_mispredictions"] = int(branch_mispredictions.group(1))

        if metrics["branch_lookups"] and metrics["branch_mispredictions"]:
            metrics["branch_accuracy"] = (
                1 - (metrics["branch_mispredictions"] / metrics["branch_lookups"])
            ) * 100

    return metrics

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 output-filter.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    metrics = extract_metrics(file_path)

    print(file_path)
    print("Extracted Metrics:")
    print(f"L1 Cache Hit Rate: {metrics['l1_hit_rate']:.2%}") if metrics['l1_hit_rate'] else print("L1 Cache Hit Rate: Data not found")
    print(f"L2 Cache Hit Rate: {metrics['l2_hit_rate']:.2%}") if metrics['l2_hit_rate'] else print("L2 Cache Hit Rate: Data not found")
    print(f"DRAM Accesses: {metrics['dram_accesses']}") if metrics['dram_accesses'] else print("DRAM Accesses: Data not found")
    print(f"Execution Ticks: {metrics['execution_ticks']}") if metrics['execution_ticks'] else print("Execution Ticks: Data not found")
    print(f"Instructions Executed: {metrics['instructions_executed']}") if metrics['instructions_executed'] else print("Instructions Executed: Data not found")
    print(f"CPI: {metrics['cpi']:.2f}") if metrics['cpi'] else print("CPI: Data not found")
    print(f"Average Memory Latency: {metrics['avg_memory_latency']} ticks") if metrics['avg_memory_latency'] else print("Average Memory Latency: Data not found")
    print(f"Branch Prediction Lookups: {metrics['branch_lookups']}") if metrics['branch_lookups'] else print("Branch Prediction Lookups: Data not found")
    print(f"Branch Mispredictions: {metrics['branch_mispredictions']}") if metrics['branch_mispredictions'] else print("Branch Mispredictions: Data not found")
    print(f"Branch Prediction Accuracy: {metrics['branch_accuracy']:.2f}%") if metrics['branch_accuracy'] else print("Branch Prediction Accuracy: Data not found")
