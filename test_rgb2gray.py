import cocotb
from cocotb.triggers import Timer, FallingEdge
from cocotb.clock import Clock

from kitty import kitty
from gray_kitty_golden import gray_kitty_golden

# LOG_MISMATCHES = True
LOG_MISMATCHES = False


@cocotb.test()
async def rgb2gray_test(dut):
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    await FallingEdge(dut.clk)              # Synchronize with the clock

    kitty_len = len(kitty)
    gray_kitty = []
    missmatches = {
        "total" : 0,
    }
    for i in range(1, 10):
        missmatches["%d_255" % i] = 0

    # Let pipeline fill before saving data
    for i in range(3):
        await Timer(10, 'us')
        dut.rgb_pixel.value = kitty[i]

    # Simultaneously load and save pixels
    for i in range(kitty_len):
        await Timer(10, 'us')

        gray_pixel = dut.gray_pixel.value
        golden_gray_pixel = gray_kitty_golden[i]

        # Input is delayed by 3 cycles
        if (i + 3) < kitty_len:
            dut.rgb_pixel.value = kitty[i + 3]

        # Save output
        gray_kitty.append(gray_pixel)

        if gray_pixel != golden_gray_pixel:
            pix_diff = abs(golden_gray_pixel - gray_pixel)

            for j in range(1, 10):
                if pix_diff > j:
                    missmatches["%d_255" % j] += 1
            missmatches["total"] += 1

            if LOG_MISMATCHES:
                print("Pixel #%d mismatch - got: 0x%02x, golden: 0x%02x" %
                    (i, gray_pixel, golden_gray_pixel))

    print("\n===================== SUMMARY =====================")
    print("Total %d mismatches out of %d pixels:" % (missmatches["total"], kitty_len))
    for i in range(1, 10):
        print("\tErrors %d/256 and bigger: %d" % (i, missmatches["%d_255" % i]))
    print("\nGolden kitty grayscale was generated using a formula:")
    print("\tgray = 0.299r + 0.587g + 0.114b")
    print("================= END OF SUMMARY ==================\n")

    gray_kitty = bytes(gray_kitty)
    with open("gray_kitty.gray", "wb") as f:
        f.write(gray_kitty)
