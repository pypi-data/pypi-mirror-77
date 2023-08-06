# ------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
# ------------------------------------------------------------------------------
# Xilinx User Guide UG903 provides a good example of this type of constraints
# ------------------------------------------------------------------------------

set stable_registers [get_cells counter_in_gray_reg*]
set first_resync_registers [get_cells counter_in_gray_p1_reg*]
set clk_in [get_clocks -of_objects [get_ports clk_in]]
set clk_out [get_clocks -of_objects [get_ports clk_out]]

if {${clk_in} == {} || ${clk_out} == {}} {
    # In some cases the clock might not be created yet, most likely during synthesis.
    # Use 1 nanosecond (1000 MHz) as default, which should be safe for all FPGA applications.
    # Hopefully the clocks are defined when this constraint file is applied again during
    # implementation. That would make the constraint more correct.
    set min_period 1
    puts "WARNING tsfpga resync_counter.tcl: Could not auto detect frequencies. Using default value."
} else {
    set clk_out_period [get_property -min PERIOD ${clk_out}]
    set clk_in_period [get_property -min PERIOD ${clk_in}]
    set min_period [expr {((${clk_in_period} < ${clk_out_period}) ? ${clk_in_period} : ${clk_out_period})} ]
    puts "INFO tsfpga resync_counter.tcl: Using min period ${min_period}"
}

# Add bus skew constraint to make sure that multiple bit changes on one clk_in cycle are detected
# with maximum one clk_out cycle skew.
set_bus_skew ${min_period} -from ${stable_registers} -to ${first_resync_registers}

# Help router by adding an arbitrary max delay. The bus skew constraint is the important part.
set_max_delay -datapath_only 5 -from ${stable_registers} -to ${first_resync_registers}
