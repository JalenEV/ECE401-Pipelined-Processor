# Pipelined RISC-V Processor Implementation

## Project Description
This project involves designing a pipelined processor that implements the RISC-V Instruction Set (RV32I or RV64I). We started by using an open-source processor repository and made improvements, focusing on pipeline efficiency and cache optimizations.

## Features
- 64-bit RISC-V processor with support for RV64I.
- 5-stage pipelined architecture.
- Cache support with L1 and L2 levels.
- Implemented optimization: Branch prediction accuracy improvements.

## Requirements
- Verilog (for hardware description).
- Logisim-Evolution or GEM5 for simulation.
- [RISC-V Specification](https://riscv.org/wp-content/uploads/2017/05/riscv-spec-v2.2.pdf)

## Installation
```bash
# Clone the repository
git clone https://github.com/JalenEV/ECE401-Pipelined-Processor.git

# Necessary set up for gem5
https://www.gem5.org/documentation/general_docs/building

# Navigate to the project directory

# Follow the setup instructions in the project

```

## Optimization Task Lists

- [ ] # Branch Prediction
- [ ] # Add L2 Cache
- [ ] # Pipeline Bypass/Forwarding
- [ ] # Memory Tuning

## Optimization Task Lists

Performance output can be identify using output-filter.py