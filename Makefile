TOPLEVEL_LANG ?= verilog
SIM ?= verilator

VERILOG_SOURCES = $(shell pwd)/src/rgb2gray.sv

MODULE = test_rgb2gray
TOPLEVEL = RGB2GRAY

include $(shell cocotb-config --makefiles)/Makefile.sim
