`timescale 1us/1us

// Fixed fractions close to real rgb2gray formula
// gray = 0.3125r + 0.5625g + 0.125b
// 0.3125 = 0b0000_0101
// 0.5625 = 0b0000_1001
// 0.1250 = 0b0000_0010
module RGB2GRAY(
	input  logic clk,
	input  logic [23:0] rgb_pixel,
	output logic [7:0]  gray_pixel);

    logic [15:0] red;
    logic [15:0] green;
    logic [15:0] blue;

    // Colors multiplied by its formula values
    logic [15:0] mul_red;
    logic [15:0] mul_green;
    logic [15:0] mul_blue;

    // red + green, red + green + blue
    logic [8:0] rg_gray, rgb_gray;

    assign red   = {4'd0, rgb_pixel[23:16], 4'd0};
    assign green = {4'd0, rgb_pixel[15:8],  4'd0};
    assign blue  = {4'd0, rgb_pixel[7:0],   4'd0};

    always@(posedge clk)
    begin
        // Cycle 1 - Multiply colors by formula values, after multiplication
        // fraction moves to the left so an integer part is at [15:8] instead of [11:4]
        mul_red   <= red   * 8'b0000_0101;
        mul_green <= green * 8'b0000_1001;
        mul_blue  <= red   * 8'b0000_0101;

        // Cycle 2 - Add computed red and green colors together
        if (mul_red[15:8] + mul_green[15:8] > 255) begin
            rg_gray <= 255;
        end else begin
            rg_gray <= mul_red[15:8] + mul_green[15:8]; // Add without fraction
        end

        // Cycle 3 - Add red and green to blue, results in a gray pixel
        rgb_gray <= rg_gray[7:0] + mul_blue[15:8]; // Add without fraction
    end

    always@(*)
    begin

        if (rgb_gray > 255) begin
            gray_pixel = 255;
        end else begin
            gray_pixel = rgb_gray[7:0];
        end
    end

    // Dump waveform
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(1, fake_crypto);
    end

endmodule
