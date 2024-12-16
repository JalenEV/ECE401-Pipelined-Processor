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
cd gem5

# stats output 
cd m5out
-> stats.txt
-> config.json
```

## Optimization Task Lists

- [x] # Branch Prediction
- [x] # Add L2 Cache
- [x] # Clock Cycles Increase

## Performance identify

>[!TIP]
>Performance output can be identify using output-filter.py
> - python output-filter.py stats-<name>.txt

 ## Reference

 The gem5 Simulator: Version 20.0+. Jason Lowe-Power, Abdul Mutaal Ahmad, Ayaz Akram, Mohammad Alian, Rico Amslinger, Matteo Andreozzi, Adrià Armejach, Nils Asmussen, Brad Beckmann, Srikant Bharadwaj, Gabe Black, Gedare Bloom, Bobby R. Bruce, Daniel Rodrigues Carvalho, Jeronimo Castrillon, Lizhong Chen, Nicolas Derumigny, Stephan Diestelhorst, Wendy Elsasser, Carlos Escuin, Marjan Fariborz, Amin Farmahini-Farahani, Pouya Fotouhi, Ryan Gambord, Jayneel Gandhi, Dibakar Gope, Thomas Grass, Anthony Gutierrez, Bagus Hanindhito, Andreas Hansson, Swapnil Haria, Austin Harris, Timothy Hayes, Adrian Herrera, Matthew Horsnell, Syed Ali Raza Jafri, Radhika Jagtap, Hanhwi Jang, Reiley Jeyapaul, Timothy M. Jones, Matthias Jung, Subash Kannoth, Hamidreza Khaleghzadeh, Yuetsu Kodama, Tushar Krishna, Tommaso Marinelli, Christian Menard, Andrea Mondelli, Miquel Moreto, Tiago Mück, Omar Naji, Krishnendra Nathella, Hoa Nguyen, Nikos Nikoleris, Lena E. Olson, Marc Orr, Binh Pham, Pablo Prieto, Trivikram Reddy, Alec Roelke, Mahyar Samani, Andreas Sandberg, Javier Setoain, Boris Shingarov, Matthew D. Sinclair, Tuan Ta, Rahul Thakur, Giacomo Travaglini, Michael Upton, Nilay Vaish, Ilias Vougioukas, William Wang, Zhengrong Wang, Norbert Wehn, Christian Weis, David A. Wood, Hongil Yoon, Éder F. Zulian. ArXiv Preprint ArXiv:2007.03152, 2021.
