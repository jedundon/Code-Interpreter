
def strip_quotes(x):
        t = x
        if t.startswith('"'):
            t = t[1:]
        if t.endswith('"'):
            t = t[:-1]
        return t

class State:
    def __init__(self):
        self.variables = {}
        self.labels = {}
        self.next_line = 0

class UserProgram:
    def __init__(self, filename):
        self.filename = filename
        self.program = []
        self.state = State()

    def load_program(self):
        try:
            with open(self.filename, 'r') as file:
                self.program = file.readlines()
                self.state = CodeInterpreter.initialize(self.state, self.program)
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")

    def execute_program(self):
        while self.state.next_line < len(self.program):
            line = self.program[self.state.next_line].strip()
            self.state = CodeInterpreter.execute_code(self.state, line)
            self.state.next_line += 1

class CodeInterpreter:
    @staticmethod
    def initialize(state, program):
        # go through each line of program and load any labels to state.labels
        current_line = 0
        while current_line < len(program):
            line = program[current_line].strip()
            operation, statement = line.split(':')
            operation = operation.strip().lower()
            statement = statement.strip()
            if operation == 'label':
                state.labels[statement] = current_line # program line of label for GOTO
            current_line +=1

        return state

    @staticmethod
    def execute_code(state, line):
        # You can access the program state variables using state.variables
        # Update the state variables and return the modified state
        operation, statement = line.split(':')
        operation = operation.strip().lower()
        statement = statement.strip()

        if operation == 'print':
            CodeInterpreter.exe_print(state, statement)
        elif operation == 'set str':
            CodeInterpreter.exe_set_str(state, statement)
        elif operation == 'set int':
            CodeInterpreter.exe_set_int(state, statement)
        elif operation == 'set float':
            var_name, value = statement.split(" ", 1)
            state.variables[var_name] = float(value)
        elif operation == 'set bool':
            var_name, value = statement.split(" ", 1)
            if value in ['true', True, 1]:
                v = True
            else:
                v = False
            state.variables[var_name] = value
        elif operation == 'label':
            # state.labels[statement] = state.next_line # program line of label for GOTO
            pass
        elif operation == 'goto':
            state.next_line = state.labels[statement] # set next line to the label's line 
        elif operation == 'add':
            var_name, value = statement.split(' ', 1)
            if var_name in state.variables:
                if isinstance(state.variables[var_name], int):
                    state.variables[var_name] += int(value)
                elif isinstance(state.variables[var_name], float):
                    state.variables[var_name] += float(value)
                else:
                    print(f"Variable '{var_name}' is not a number.")
            else:
                print(f"Variable '{var_name}' not found.")

        return state
    
    @staticmethod
    def exe_print(state: State, statement: str):
        # PRINT operation
        if statement.startswith('"') and statement.endswith('"'):
            print(strip_quotes(statement))
        elif statement in state.variables:
            print(state.variables[statement])
        else:
            print(f"Variable '{statement}' not found.")

    @staticmethod
    def exe_set_str(state: State, statement: str):
        # SET STR operation
        try:
            var_name, value = statement.split(" ", 1)
            state.variables[var_name] = strip_quotes(value)
        except ValueError:
            print(f"Invalid syntax in 'set str' operation: {statement}")

    @staticmethod
    def exe_set_int(state: State, statement: str):
        # SET INT operation
        try:
            var_name, value = statement.split(" ", 1)
            state.variables[var_name] = int(value)
        except ValueError:
            print(f"Invalid syntax in 'set int' operation: {statement}")

program = UserProgram(r'Code Interpreter\\usercode.txt')
program.load_program()
program.execute_program()

# if : blah blah blah [
#   
# ]

# if : condition
# stuff
# if : condition
# stuff 2
# end :
# stuff 3
# else :
# other stuff
# end :