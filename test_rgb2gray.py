import cocotb
from cocotb.triggers import Timer, FallingEdge
from cocotb.clock import Clock
from kitty import kitty

@cocotb.test()
async def rgb2gray_test(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    gray_kitty = []

    # Let pipeline fill before saving data
    for i in range(3):
        await Timer(10, 'us')
        dut.rgb_pixel.value = kitty[i]

    # Simultaneously load and save pixels
    for i in range(len(kitty)):
        await Timer(10, 'us')

        # Input is delayed by 3 cycles
        if (i + 3) < len(kitty):
            dut.rgb_pixel.value = kitty[i + 3]

        # Save output
        gray_kitty.append(dut.gray_pixel.value)

    gray_kitty = bytes(gray_kitty)
    with open("gray_kitty.gray", "wb") as f:
        f.write(gray_kitty)
