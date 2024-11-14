from m5.objects import *
from m5.util import addToPath
import os

addToPath(os.path.join(os.environ['G5'], 'configs'))  # Using G5 as per your updated environment variable

from common import SimpleOpts

# SimpleOpts is used for command-line argument parsing
SimpleOpts.add_option('--cpu-type', nargs='?', type=str, default='RV64I',
                      help='Specify CPU type to simulate: RV32I or RV64I.')

options = SimpleOpts.parse_args()

# Define L1 Instruction Cache
class L1ICache(Cache):
    assoc = 2
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    size = '16kB'
    tgts_per_mshr = 20
    writeback_clean = True

# Define L1 Data Cache
class L1DCache(Cache):
    assoc = 2
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    size = '16kB'
    tgts_per_mshr = 20
    writeback_clean = True

# Define the system
system = System()

# Set up the clock and voltage domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Memory subsystem
system.mem_mode = 'timing'  # Use 'timing' mode for more accurate timing of memory accesses
system.mem_ranges = [AddrRange('8192MB')]  # Define the size of memory

# Configure CPU type (generic model with RISC-V target)
system.cpu = [TimingSimpleCPU()]  # Define CPU as a list (even if it's a single CPU)

# Configure memory for the CPU
system.cpu[0].icache = L1ICache()  # Instruction cache
system.cpu[0].dcache = L1DCache()  # Data cache

# Memory Bus
system.membus = SystemXBar()

# Connecting CPU and caches to the memory bus
system.cpu[0].icache_port = system.membus.cpu_side_ports
system.cpu[0].dcache_port = system.membus.cpu_side_ports

# Configure the memory controller and DRAM
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()  # Use DDR3 memory as a component of MemCtrl
system.mem_ctrl.dram.range = system.mem_ranges[0]  # Set the memory range
system.mem_ctrl.port = system.membus.mem_side_ports  # Connect to memory bus

# Create a system port for console I/O
system.system_port = system.membus.cpu_side_ports

# Process (executable) to run on the simulated CPU
if options.cpu_type == 'RV32I':
    binary = 'tests/test-progs/hello/bin/riscv/linux/hello_rv32.elf'  # The 32-bit version
elif options.cpu_type == 'RV64I':
    binary = 'tests/test-progs/hello/bin/riscv/linux/hello'  # The 64-bit version
else:
    raise ValueError("Unsupported CPU type. Please use RV32I or RV64I.")


# Create a process to represent the workload
process = Process()
process.cmd = ['/home/gjl/gem5/tests/test-progs/hello/bin/riscv/linux/hello']   # Set the binary file to be run

# Assign workload to CPU
system.cpu[0].workload = process
system.cpu[0].createThreads()

# Root system
root = Root(full_system=False, system=system)

# Instantiate simulation
m5.instantiate()

print("Starting simulation of a RISC-V processor with type: ", options.cpu_type)
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
