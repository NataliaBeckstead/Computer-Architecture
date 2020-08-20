"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0]*8
        self.ram = [0]*256
        self.pc = 0
        self.reg[7] = 244 #SP
        self.program_length = 0
        self.fl = 0b00000000

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

            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    val = int(n, 2)
                    self.ram[address] = val

                    address += 1
            
            self.program_length = address

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
        return self.reg[address]

    def ram_write(self, address, value):
        self.reg[address] = value

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            command = self.ram[self.pc]

            # LDI
            if command == 0b10000010:
                self.ram_write(self.ram[self.pc+1], self.ram[self.pc+2])
                self.pc += 2
                # print("LDI")

            # PRN
            if command == 0b01000111:
                # print(bin(self.ram_read(self.ram[self.pc+1])))
                print(self.ram_read(self.ram[self.pc+1]))
                self.pc += 1
                # print("PRN")

            # MUL
            if command == 0b10100010:
                self.ram_write(self.ram[self.pc+1], (self.reg[self.ram[self.pc+1]] * self.reg[self.ram[self.pc+2]]))
                self.pc += 2
                # print("MUL")

            # PUSH
            if command == 0b01000101:
                if self.reg[7] > self.program_length:
                    self.reg[7] -= 1
                    self.ram[self.reg[7]] = self.reg[self.ram[self.pc+1]]
                    self.pc += 1
                else:
                    print("Stack is full")
                    break
                # print("PUSH")

            # POP
            if command == 0b01000110:
                if self.reg[7] == 244:
                    print("Stack is empty")
                    continue
                self.reg[self.ram[self.pc+1]] = self.ram[self.reg[7]]
                self.reg[7] += 1
                self.pc += 1
                # print("POP")

            # CALL
            if command == 0b01010000:
                self.reg[7] -= 1
                self.ram[self.reg[7]] = self.pc + 2
                self.pc = self.reg[self.ram[self.pc + 1]] - 1
                # print("CALL")

            # ADD
            if command == 0b10100000:
                self.ram_write(self.ram[self.pc+1], (self.reg[self.ram[self.pc+1]] + self.reg[self.ram[self.pc+2]]))
                self.pc += 2
                # print("ADD")

            # RET
            if command == 0b00010001:
                self.pc = self.ram[self.reg[7]] - 1
                self.reg[7] += 1
                # print("RET")

            # JMP
            if command == 0b01010100:
                self.pc = self.reg[self.ram[self.pc+1]] - 1
                # print("JMP")

            # CMP
            if command == 0b10100111:
                # 00000LGE
                if self.reg[self.ram[self.pc+1]] == self.reg[self.ram[self.pc+2]]:
                    self.fl = 0b00000001
                elif self.reg[self.ram[self.pc+1]] < self.reg[self.ram[self.pc+2]]:
                    self.fl = 0b00000100
                elif self.reg[self.ram[self.pc+1]] > self.reg[self.ram[self.pc+2]]:
                    self.fl = 0b00000010
                self.pc += 2
                # print("CMP")

            # JEQ
            if command == 0b01010101:
                # 00000LGE
                if self.fl & 0b00000001: #bitwise masking
                    self.pc = self.reg[self.ram[self.pc+1]] - 1
                else:
                    self.pc += 1
                # print("JEQ")

            # JNE
            if command == 0b01010110:
                # 00000LGE
                if not self.fl & 0b00000001: #bitwise masking
                    self.pc = self.reg[self.ram[self.pc+1]] - 1
                else:
                    self.pc += 1
                # print("JNE")

            # HLT
            if command == 0b00000001:
                # print("HLT")
                running = False

            

            self.pc += 1

