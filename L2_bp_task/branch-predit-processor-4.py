import m5
from m5.objects import *
import os

# Create the system object
system = System()

# Set up the clock domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set the memory mode and address range
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("8192MB")]

class L1ICache(Cache):
    assoc = 2
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 2
    size = '32kB'             # Slightly larger size, depending on the workload
    tgts_per_mshr = 8

class L1DCache(Cache):
    assoc = 4
    tag_latency = 1           # Reduced tag latancy to minimize delays
    data_latency = 1          # Reduce data latency to simulate forwarding
    response_latency = 1
    mshrs = 4
    size = '16kB'
    tgts_per_mshr = 16
    writeback_clean = True    # Write-back policy to reduce memory writes

# Set up the CPU with branch prediction
system.cpu = RiscvTimingSimpleCPU()
system.cpu.branchPred = TournamentBP()  # Add branch prediction

# Assign L1 instruction and data caches
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

# Create a memory bus
system.membus = SystemXBar()

# Connect the CPU caches to the memory bus
system.cpu.icache_port = system.cpu.icache.cpu_side
system.cpu.dcache_port = system.cpu.dcache.cpu_side

# Connect caches to the memory bus
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

# Create the interrupt controller for the CPU
system.cpu.createInterruptController()

# Set up the memory controller and DRAM
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Connect the system port to the memory bus
system.system_port = system.membus.cpu_side_ports

# Set up the binary to run
thispath = os.path.dirname(os.path.realpath(__file__))
binary = os.path.join(
    thispath,
    "../../../",
    "tests/test-progs/hello/bin/riscv/linux/hello",
)

# Set up the workload
system.workload = SEWorkload.init_compatible(binary)

# Create a process to represent the workload
process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# Set up the root and instantiate the system
root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause()))