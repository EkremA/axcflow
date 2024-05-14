module adder(
    input [7:0] num1,
    input [7:0] num2,
    input clk,
    output reg [7:0] sum
);

    always @(posedge clk) begin
        sum <= num1 + num2;
    end

endmodule
