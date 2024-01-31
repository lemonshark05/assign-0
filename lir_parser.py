import sys
import re

class BasicBlock:
    def __init__(self, label):
        self.label = label
        self.instructions = []
        self.terminal = None

class Function:
    def __init__(self, name, return_type):
        self.name = name
        self.parameters = []
        self.return_type = return_type
        self.local_variables = []
        self.basic_blocks = []

    def add_basic_block(self, block):
        self.basic_blocks.append(block)

    def add_parameter(self, param):
        self.parameters.append(param)

    def add_local_variable(self, var):
        self.local_variables.append(var)

# Init
num_struct_fields = 0
num_functions_with_return = 0
num_function_parameters = 0
num_local_variables = 0
num_basic_blocks = 0
num_instructions = 0
num_terminals = 0
num_locals_and_globals_int_type = 0
num_locals_and_globals_struct_type = 0
num_locals_and_globals_pointer_to_int_type = 0
num_locals_and_globals_pointer_to_struct_type = 0
num_locals_and_globals_pointer_to_function_type = 0
num_locals_and_globals_pointer_to_pointer_type = 0


def parse_lir_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('struct'):
                parse_struct(line)
            elif line.startswith('let'):
                parse_global_variable(line)
            elif line.startswith('extern'):
                parse_extern_function(line)
            elif line.startswith('fn'):
                parse_function(line)


def parse_struct(line):
    global num_struct_fields
    match = re.match(r'struct (\w+) {', line)
    if match:
        struct_name = match.group(1)

def parse_global_variable(line):
    global num_local_variables, num_basic_blocks, num_instructions, num_terminals
    match = re.match(r'(\w+) : (.+)', line)
    if match:
        var_name, var_type = match.groups()
        num_local_variables += 1
        count_variable_types(var_type)

def parse_extern_function(line):   
    pass

def parse_function(line):
    global num_functions_with_return, num_function_parameters
    if '->' in line:
        # Counting functions with a return value
        if not line.endswith('-> _'):
            print("is not -")
            num_functions_with_return += 1

        # Counting function parameters
        params = line.split('(')[1].split(')')[0]
        if params:
            num_params = len(params.split(','))
            num_function_parameters += num_params
    

def count_variable_types(var_type):
    global num_locals_and_globals_int_type, num_locals_and_globals_struct_type
    global num_locals_and_globals_pointer_to_int_type, num_locals_and_globals_pointer_to_struct_type
    global num_locals_and_globals_pointer_to_function_type, num_locals_and_globals_pointer_to_pointer_type

    if var_type == 'int':
        num_locals_and_globals_int_type += 1
    elif 'struct' in var_type:
        num_locals_and_globals_struct_type += 1
    elif var_type.startswith('&'):
        if 'int' in var_type:
            num_locals_and_globals_pointer_to_int_type += 1
        elif 'struct' in var_type:
            num_locals_and_globals_pointer_to_struct_type += 1
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        # python3 lir_parser.py tests/test.13.2.lir
        print("Usage: python3 lir_parser.py <lir_file_path>")
        sys.exit(1)

    lir_file_path = sys.argv[1]
    parse_lir_file(lir_file_path)

    # Printing the statistics
    print(f"Number of fields across all struct types: {num_struct_fields}")
    print(f"Number of functions that return a value: {num_functions_with_return}")
    print(f"Number of function parameters: {num_function_parameters}")
    print(f"Number of local variables: {num_local_variables}")
    print(f"Number of basic blocks: {num_basic_blocks}")
    print(f"Number of instructions: {num_instructions}")
    print(f"Number of terminals: {num_terminals}")
    print(f"Number of locals and globals with int type: {num_locals_and_globals_int_type}")
    print(f"Number of locals and globals with struct type: {num_locals_and_globals_struct_type}")
    print(f"Number of locals and globals with pointer to int type: {num_locals_and_globals_pointer_to_int_type}")
    print(f"Number of locals and globals with pointer to struct type: {num_locals_and_globals_pointer_to_struct_type}")
    print(f"Number of locals and globals with pointer to function type: {num_locals_and_globals_pointer_to_function_type}")
    print(f"Number of locals and globals with pointer to pointer type: {num_locals_and_globals_pointer_to_pointer_type}")

