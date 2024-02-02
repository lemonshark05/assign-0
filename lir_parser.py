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
num_locals_and_globals_pointer_int_type = 0
num_locals_and_globals_pointer_struct_type = 0
num_locals_and_globals_pointer_function_type = 0
num_locals_and_globals_pointer_pointer_type = 0


def parse_lir_file(file_path):
    with open(file_path, 'r') as file:
        is_struct = False
        is_function = False
        for line in file:
            line = line.strip()
            if line.startswith('struct '):
                is_struct = True
            elif is_struct and line == '}':
                is_struct = False
            elif is_struct:
                parse_struct(line)
            elif line.startswith('fn '):
                is_function = True
                parse_function(line)
            elif is_function:
                parse_function_content(line)
            elif is_function and line.startswith('}'):
                is_function = False
            elif line.startswith('extern '):
                parse_extern_function(line)
            elif not is_function and not is_struct and ':' in line:
                parse_global_line(line)

def parse_struct(line):
    global num_struct_fields
    field_match = re.match(r'\s*(\w+):(.+)', line)
    if field_match:
        num_struct_fields += 1

def parse_extern_function(line):   
    pass

def parse_function_content(line):
    global num_local_variables, num_basic_blocks, num_instructions, num_terminals
    local_var_match = re.match(r'let\s+(.*)', line)
    instruction_pattern = re.compile(r'\$(store|load|alloc|cmp|gep|copy|call_ext|addrof|arith|gfp)')
    terminal_pattern = re.compile(r'\$(branch|jump|ret|call_dir|call_idr)')

    if local_var_match:
        all_vars = local_var_match.group(1)
        vars = all_vars.split(',')
        for var in vars:
            if '&(' in var and '->' in var:
                print(var)
            if ':' in var:
                num_local_variables += 1
                var_type = var.split(':')[1].strip()
                count_variable_types(var_type)

    if re.match(r'^\w+:', line):
        num_basic_blocks += 1

    if instruction_pattern.search(line):
        num_instructions += 1

    if terminal_pattern.search(line):
        # print(line)
        num_terminals += 1

def parse_function(line):
    global num_functions_with_return, num_function_parameters
    if '->' in line:
        # Counting functions with a return value
        if not line.__contains__('-> _'):
            num_functions_with_return += 1

        # Counting function parameters
        params = line.split('(')[1].split(')')[0]
        if params:
            num_params = len(params.split(','))
            num_function_parameters += num_params

def parse_global_line(line):
    global_line_match = re.match(r'(\w+):\s*(&?[\w&() ->]+)', line)
    if global_line_match:
        if line.__contains__('&(') and line.__contains__('->'):
            print(line)
        var_type = global_line_match.group(2)
        count_variable_types(var_type)

def count_variable_types(var_type):
    global num_locals_and_globals_int_type, num_locals_and_globals_struct_type
    global num_locals_and_globals_pointer_int_type, num_locals_and_globals_pointer_struct_type
    global num_locals_and_globals_pointer_function_type, num_locals_and_globals_pointer_pointer_type

    if var_type == 'int':
        num_locals_and_globals_int_type += 1
    elif var_type.startswith('struct'):
        num_locals_and_globals_struct_type += 1
    elif var_type.startswith('&'):
        if var_type.startswith('&int'):
            num_locals_and_globals_pointer_int_type += 1
        elif var_type.startswith('&struct'):
            num_locals_and_globals_pointer_struct_type += 1
        elif var_type.startswith('&&'):
            num_locals_and_globals_pointer_pointer_type += 1
        elif var_type.startswith('&(') and '->' in var_type:
            num_locals_and_globals_pointer_function_type += 1

        
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
    print(f"Number of locals and globals with pointer to int type: {num_locals_and_globals_pointer_int_type}")
    print(f"Number of locals and globals with pointer to struct type: {num_locals_and_globals_pointer_struct_type}")
    print(f"Number of locals and globals with pointer to function type: {num_locals_and_globals_pointer_function_type}")
    print(f"Number of locals and globals with pointer to pointer type: {num_locals_and_globals_pointer_pointer_type}")

