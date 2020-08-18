"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0]*8
        self.ram = [0]*256
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) > 1:

            try:
                address = 0
                with open(sys.argv[1]) as f:
                    for line in f:
                        comment_split = line.split("#")
                        n = comment_split[0].strip()

                        if n == '':
                            continue

                        val = int(n, 2)
                        # store val in memory
                        self.ram[address] = val

                        address += 1

            except FileNotFoundError:
                print(f"{sys.argv[0]}: filename not found")
                sys.exit(2)

        else:
            print(f"{sys.argv[0]}: filename not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            command = self.ram[self.pc]

            # LDI
            if command == 0b10000010:
                self.ram_write(self.ram[self.pc+1], self.ram[self.pc+2])
                self.pc += 2

            # PRN
            if command == 0b01000111:
                # print(bin(self.ram_read(self.ram[self.pc+1])))
                print(self.ram_read(self.ram[self.pc+1]))
                self.pc += 1

            # MUL
            if command == 0b10100010:
                self.ram_write(self.ram[self.pc+1], (self.ram[self.ram[self.pc+1]] * self.ram[self.ram[self.pc+2]]))
                self.pc += 2

            # HLT
            if command == 0b00000001:
                running = False

            self.pc += 1

# test = CPU()
# test.__init__()
# test.load()
# test.run()