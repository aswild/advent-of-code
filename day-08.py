import re, pprint
from dataclasses import dataclass
from enum import Enum

class OP(Enum):
    ACC = 1
    JMP = 2
    NOP = 3

    def parse(s):
        if s.lower() == 'acc':
            return OP.ACC
        elif s.lower() == 'jmp':
            return OP.JMP
        elif s.lower() == 'nop':
            return OP.NOP
        else:
            raise ValueError(f'invalid opcode "{s}"')

@dataclass
class Instruction:
    op: OP
    arg: int

    def parse(inst_str):
        if m := re.match(r'(acc|jmp|nop)\s+([+-]\d+)$', inst_str):
            return Instruction(OP.parse(m.group(1)), int(m.group(2)))
        else:
            raise ValueError(f'failed to parse instruction "{inst_str}"')

    def __str__(self):
        if self.op == OP.ACC:
            word = 'acc'
        elif self.op == OP.JMP:
            word = 'jmp'
        elif self.op == OP.NOP:
            word = 'nop'
        return f'Instruction({word} {self.arg:+})'

class VM:
    def __init__(self, code):
        self.code = [Instruction.parse(line) for line in code.splitlines()]
        assert len(self.code) > 0
        self.reset()

    def reset(self):
        self.acc = 0
        self.pc = 0
        self.visited = [False] * len(self.code)
        self.count = 0

    def step(self):
        inst = self.code[self.pc]
        #print(f'Execute instruction {self.pc}: {inst}')
        new_pc = self.pc + 1

        if inst.op == OP.ACC:
            self.acc += inst.arg
        elif inst.op == OP.JMP:
            new_pc = self.pc + inst.arg
        elif inst.op == OP.NOP:
            pass

        self.visited[self.pc] = True
        self.count += 1
        self.pc = new_pc

    def run(self):
        """ Run the VM until it terminates (True) or hits a loop (False) """
        while True:
            self.step()
            # pc now points to next instruction to run, check if we've been there before
            if self.pc >= len(self.code):
                return True
            if self.visited[self.pc]:
                return False
        raise RuntimeError('oh no')

    def flip_inst(self, pc):
        inst = self.code[pc]
        assert inst is self.code[pc]
        if inst.op == OP.NOP:
            inst.op = OP.JMP
        elif inst.op == OP.JMP:
            inst.op = OP.NOP
        else:
            return False
        assert inst is self.code[pc]
        return True

def part_1(data):
    vm = VM(data)
    vm.run()
    print(f'Ran {vm.count} instructions')
    return vm.acc

def part_2(data):
    vm = VM(data)
    # for all the instructions
    for i in range(len(vm.code)):
        # try to flip the current instruction
        if vm.flip_inst(i):
            # run the test
            vm.reset()
            if vm.run():
                # yay
                print(f'Terminated after flipping pc={i} to {vm.code[i]}')
                return vm.acc
            # it still looped, flip it back and try again
            vm.flip_inst(i)

FORMAT_1 = 'final accumulator {}'
FORMAT_2 = FORMAT_1

TEST_CODE = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

TEST_CASE_1 = [(TEST_CODE, 5)]
TEST_CASE_2 = [(TEST_CODE, 8)]
