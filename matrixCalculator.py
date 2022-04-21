#!/usr/bin/python

from datetime import datetime


class Matrix:
    def __init__(self, matrix_array):
        self.matrix_array = matrix_array
        self.height = len(matrix_array)
        self.width = len(matrix_array[0])

    def update_matrix(self, matrix):
        self.set_matrix_array(matrix.get_matrix_array())
        self.set_height(len(matrix.get_matrix_array()))
        self.set_width(len(matrix.get_matrix_array()[0]))

    def get_matrix_array(self):
        return self.matrix_array

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def set_matrix_array(self, array):
        self.matrix_array = array

    def set_height(self, height):
        self.height = height

    def set_width(self, width):
        self.width = width

    # DET command
    # Function that returns the determinant of self matrix provided it can be calculated
    def determinant_of_self(self):
        if self.height != self.width:
            return "Determinant can only be calculated for square matrices."
        elif self.height == 1:
            return self.matrix_array[0][0]
        else:
            return determinant_helper(self.matrix_array)

    # INV command
    # Function that returns whether the matrix is invertible (aka determinant exists and is not 0)
    def invertibility_of_self(self):
        determinant = self.determinant_of_self()
        try:
            determinant = int(determinant)
            return determinant != 0
        except ValueError:
            return False

    # PRI command and others
    # Function that converts the matrix into a presentable array of string lines (per each row) for later processing and printing
    def string_self_array(self):
        strings_of_matrix = []
        for row in self.matrix_array:
            row_string = "|"
            for item in row:
                row_string += f"\t{item}"
            row_string += "\t|"
            strings_of_matrix.append(row_string)
        return strings_of_matrix


# Helper function to find the determinant recursively
def determinant_helper(matrix_array, total=0):
    indexes = list(range(len(matrix_array)))
    # Base case of recursion: determinant of 2x2 matrix
    if len(matrix_array) == 2 and len(matrix_array[0]) == 2:
        determinant = matrix_array[0][0] * matrix_array[1][1] - matrix_array[1][0] * matrix_array[0][1]
        return determinant
    # Inductive step of recursion: Find determinant of sub-matrix excluding current row and current column
    for focus_column in indexes:  # A) for each focus column, ...
        coppied_array = matrix_array[:]
        coppied_array = coppied_array[1:]
        height = len(coppied_array)
        for i in range(height):
            coppied_array[i] = coppied_array[i][0:focus_column] + coppied_array[i][focus_column + 1:]
        sign_of_permutation = (-1) ** (focus_column % 2)  # F)
        sub_det = determinant_helper(coppied_array)
        total += sign_of_permutation * matrix_array[0][focus_column] * sub_det
    return total


# SCA command
# Function that returns a scalar multiple of given matrix
def multiply_by_scalar(matrix, scalar):
    m = [[] for _ in range(matrix.get_height())]
    for row_index, row in enumerate(m):
        for column_index in range(matrix.get_width()):
            row.append(matrix.matrix_array[row_index][column_index] * scalar)
    return Matrix(m)


# TRA command
# Function that returns a transpose of a given matrix
def transpose(matrix):
    m = [[] for _ in range(len(matrix.matrix_array[0]))]
    for column_index, row in enumerate(m):
        for row_index in range(matrix.get_height()):
            row.append(matrix.matrix_array[row_index][column_index])
    return Matrix(m)


# POW command
# Function that returns matrix raised to the given power (employs multiply_matrix())
def raise_to_power(matrix, power):
    resulting_matrix = matrix
    original_matrix = matrix
    for current_power in range(power-1):
        resulting_matrix = multiply_matrices(resulting_matrix, original_matrix)
    return resulting_matrix


# MUL command
# Function that returns the product of two given matrices
def multiply_matrices(matrix_left, matrix_right):
    number_of_columns_a = matrix_left.get_width()
    number_of_rows_b = matrix_right.get_height()
    compatibility_check = number_of_columns_a == number_of_rows_b
    if not compatibility_check:
        return "To multiply matrices, the left matrix width must equal the right matrix height."
    resulting_height = matrix_left.get_height()
    resulting_width = matrix_right.get_width()
    m = [[0 for _ in range(resulting_width)] for _ in range(resulting_height)]
    for row_index in range(resulting_height):
        for column_index in range(resulting_width):
            s = 0
            for i in range(number_of_columns_a):
                s += matrix_left.matrix_array[row_index][i] * matrix_right.matrix_array[i][column_index]
            m[row_index][column_index] = s
    return Matrix(m)


# ADD command
# Function that returns the sum of two given matrices
def add_matrices(matrix_a, matrix_b):
    matrix_a_width = matrix_a.get_width()
    matrix_a_height = matrix_a.get_height()
    matrix_b_width = matrix_b.get_width()
    matrix_b_height = matrix_b.get_height()
    compatibility_check_1 = matrix_a_height == matrix_b_height
    compatibility_check_2 = matrix_a_width == matrix_b_width
    if not compatibility_check_1 or not compatibility_check_2:
        return "Matrix addition/subtraction is not defined for matrices of different dimensions."
    resulting_height = matrix_a_height
    resulting_width = matrix_b_width
    m = [[0 for _ in range(resulting_width)] for _ in range(resulting_height)]
    for row_index in range(resulting_height):
        for column_index in range(resulting_width):
            s = 0
            if row_index < matrix_a_height and column_index < matrix_a_width:
                s += matrix_a.matrix_array[row_index][column_index]
            if row_index < matrix_b_height and column_index < matrix_b_width:
                s += matrix_b.matrix_array[row_index][column_index]
            m[row_index][column_index] = s
    return Matrix(m)


# SUB command (subtraction)
# Function that returns the difference of two given matrices (employs add_matrices() and multiply_by_scalar())
def subtract_matrices(matrix_a, matrix_b):
    return add_matrices(matrix_a, multiply_by_scalar(matrix_b, -1))


# Function that verifies, that the matrix command entered by user is valid:
# 1. supported operation
# 2. right number of arguments
# 3. valid arguments
#    a) existing matrix
#    b) integer as scalar for scaling a matrix
#    c) positive integer as power for raising a matrix to a power
def verify_command(list):
    operations = {"ADD": 4, "SUB": 4, "MUL": 4, "SCA": 4, "POW": 4, "TRA": 3, "DET": 2, "INV": 2, "PRI": 2, "END": 1}
    list_length = len(list)
    if list_length == 0:
        print("Your command was empty. Try again.")
        return False
    operation = list[0]
    if operation not in operations:
        print("We don't support that operation. Try again.")
        return False
    if list_length != operations[operation]:
        print("Incorrect number of arguments. Try again.")
        return False
    if operation in "ADD SUB MUL DET INV PRI TRA":
        for argument in list[1:]:
            if argument not in "A B X":
                print("Only valid argument values are A, B, and X.")
                return False
    if operation == "SCA" or operation == "POW":
        for argument in list[1:3]:
            if argument not in "A B X":
                print("Only valid values for 2nd and 3rd argument are A, B, and X.")
                return False
        try:
            number = int(list[3])
            if operation == "POW" and number < 1:
                print("You can raise a matrix only to positive integer values.")
                return False
        except ValueError:
            if operation == "SCA":
                print("4th argument of SCA operation must be an integer.")
                return False
            elif operation == "POW":
                print("4th argument of POW operation must be an integer.")
                return False
    print("Valid command.")
    return True


# Function that takes in: record_file, any number of strings and matrices.
# It transforms each argument to an overall presentable output with elements of each line well aligned above and below.
# Then it prints the result to output and append it to the record (calculator history) file.
def format_output(file, *arguments):
    # Firstly we create the first line of the output and check the depth (desired_number_of_lines) of each argument and also the width of each argument
    desired_number_of_lines = 1
    argument_lengths = []
    first_line = ""
    for argument in arguments:
        if type(argument) is list:
            its_length = len(argument)
            desired_number_of_lines = max(desired_number_of_lines, its_length)
            list_item_string = argument[0].expandtabs(4)
            argument_lengths.append(len(list_item_string))
            first_line += argument[0].expandtabs(4)
            continue
        argument_lengths.append(len(argument))
        first_line += argument
    # Then we create the remaining lines
    outputs = [first_line + "\n"]
    line_index = 1
    while line_index < desired_number_of_lines:
        remaining_line = ""
        for index, argument in enumerate(arguments):
            if type(argument) is not list:
                remaining_line += " " * argument_lengths[index]
            else:
                if line_index < len(argument):
                    list_item_string = argument[line_index].expandtabs(4)
                    remaining_line += list_item_string
                else:
                    remaining_line += " " * argument_lengths[index]
        outputs.append(remaining_line + "\n")
        line_index += 1
    # Finally, output them.
    file.writelines(outputs)
    print(*outputs, sep="")


# Function that reads one matrix from the input file starting at a given line (index)
# It also checks that each matrix row has the same number of elements.
# Other errors are handled by try-except in the main() (only place, where this function is used)
def read_one_matrix(index, lines):
    matrix_array = list()
    length = len([int(i) for i in lines[index][:-1].split()])
    while index < len(lines):
        line = lines[index]
        if len(line) > 1:
            line = lines[index][:-1]
            numbers_in_row = [int(i) for i in line.split()]
            new_length = len(numbers_in_row)
            if new_length != length:
                return False
            else:
                length = new_length
            matrix_array.append(numbers_in_row)
            index += 1
            continue
        index += 1
        break
    return (Matrix(matrix_array), index)


def main():

    # Initialize 3 matrix objects which will be the only 3 available matrices to work with
    matrix_A = None
    matrix_B = None
    matrix_X = Matrix([[0]])

    # Load matrix_A and matrix_B from the input.txt file
    try:
        with open("input.txt", "r") as file:
            lines = file.readlines()
            result1 = read_one_matrix(0, lines)
            matrix_A = result1[0]
            result2 = read_one_matrix(result1[1], lines)
            matrix_B = result2[0]
    except:
        print("Input file does not follow the required format.")
        exit(0)

    matrix_matcher = {"A": matrix_A, "B": matrix_B, "X": matrix_X}
    print("WELCOME TO MATRIX CALCULATOR")
    # Open the record.txt file and start recording calculator history
    record_file = open("record.txt", "a")
    record_file.write(f"\n\n### Session | {datetime.now()} | ###\n")
    format_output(record_file, "Starting Matrices: Matrix A = ", matrix_A.string_self_array(), "     Matrix B = ",
                  matrix_B.string_self_array(), "     Matrix X = ", matrix_X.string_self_array())


    counter = 0

    # For each single command one iteration. The loop ends, when user writes: END
    while True:

        # Getting user command
        message = input("\n\nWrite your command: ").upper()
        command_list = message.split()

        # Verifying that the user command is valid
        if not verify_command(command_list):
            continue
        print("Working...")

        operation = command_list[0]

        # Recording the command into calculator history in record.txt
        counter += 1
        record_file.write(f"\nCOMMAND #{counter}: {message}\n")

        # OPERATIONS WITH 1 ARGUMENT (COMMAND):

        # END outputs the final state of all matrices, closes the file and breaks the loop.
        if operation == "END":
            format_output(record_file, "Final Matrices: Matrix A = ", matrix_A.string_self_array(), "     Matrix B = ", matrix_B.string_self_array(), "     Matrix X = ", matrix_X.string_self_array())
            print("Goodbye.")
            record_file.close()
            break

        # OPERATIONS WITH 2 ARGUMENTS ( COMMAND,
        #                               MATRIX A/B/X TO PERFORM THE OPERAION ON):
        matrix1 = matrix_matcher[command_list[1]]

        # PRI outputs the current state of the matrix.
        if operation == "PRI":
            format_output(record_file, f"Matrix {command_list[1]} = ", matrix1.string_self_array())
            continue

        # DET outputs the determinant of the given matrix.
        if operation == "DET":
            determinant_output = matrix1.determinant_of_self()
            try:
                determinant = int(determinant_output)
                format_output(record_file, "det(", matrix1.string_self_array(), ") = ", str(determinant))
            except ValueError:
                format_output(record_file, determinant_output)
            continue

        # INV outputs the invertibility of a given matrix.
        if operation == "INV":
            invertibility_output = matrix1.invertibility_of_self()
            end_string = ""
            if invertibility_output:
                end_string = " is invertible."
            else:
                end_string = " is not invertible."
            format_output(record_file, matrix1.string_self_array(), end_string)
            continue

        # OPERATIONS WITH 3 ARGUMENTS ( COMMAND,
        #                               MATRIX A/B/X WHERE THE RESULT SHOULD BE SAVED,
        #                               MATRIX A/B/X TO PERFORM THE OPERATION ON):
        save_at = matrix_matcher[command_list[1]]
        matrix2 = matrix_matcher[command_list[2]]

        # TRA outputs the transpose of a given matrix and saves it into save_at.
        if operation == "TRA":
            final_matrix = transpose(matrix2)
            format_output(record_file, "transpose(", matrix2.string_self_array(), ") = ", final_matrix.string_self_array())
            save_at.update_matrix(final_matrix)
            continue

        # SCA OPERATION WITH 3 SAME ARGUMENTS AND 4TH INTEGER SCALAR
        # SCA outputs scaled version of a given matrix by a given scalar and saves it into save_at.
        if operation == "SCA":
            scalar = int(command_list[3])
            final_matrix = multiply_by_scalar(matrix2, scalar)
            format_output(record_file, str(scalar), " * ", matrix2.string_self_array(), " = ", final_matrix.string_self_array())
            save_at.update_matrix(final_matrix)
            continue

        # POW OPERATION WITH 3 SAME ARGUMENTS AND 4TH POSITIVE INTEGER POWER
        # POW outputs given matrix raised to a given power and saves it into save_at.
        if operation == "POW":
            power = int(command_list[3])
            final_matrix = raise_to_power(matrix2, power)
            format_output(record_file, matrix2.string_self_array(), " raised to the power of ", str(power), " = ", final_matrix.string_self_array())
            save_at.update_matrix(final_matrix)
            continue

        # OPERATIONS WITH 3 ARGUMENTS ( COMMAND,
        #                               MATRIX A/B/X WHERE THE RESULT SHOULD BE SAVED,
        #                               MATRIX A/B/X AS THE 1ST ARGUMENT OF AN OPERATION,
        #                               MATRIX A/B/X AS THE 2ND ARGUMENT OF AN OPERATION):
        matrix3 = matrix_matcher[command_list[3]]

        # ADD outputs the sum of two given matrices and saves it into save_at.
        if operation == "ADD":
            final_matrix = add_matrices(matrix2, matrix3)
            if type(final_matrix) is not Matrix:
                format_output(record_file, final_matrix)
            else:
                format_output(record_file, matrix2.string_self_array(), " + ", matrix3.string_self_array(), " = ", final_matrix.string_self_array())
                save_at.update_matrix(final_matrix)
            continue

        # SUB outputs the difference of two given matrices and saves it into save_at.
        elif operation == "SUB":
            final_matrix = subtract_matrices(matrix2, matrix3)
            if type(final_matrix) is not Matrix:
                format_output(record_file, final_matrix)
            else:
                format_output(record_file, matrix2.string_self_array(), " - ", matrix3.string_self_array(), " = ", final_matrix.string_self_array())
                save_at.update_matrix(final_matrix)
            continue

        # MUL (multiplication) outputs the product of two given matrices and saves it into save_at.
        if operation == "MUL":
            final_matrix = multiply_matrices(matrix2, matrix3)
            if type(final_matrix) is not Matrix:
                format_output(record_file, final_matrix)
            else:
                format_output(record_file, matrix2.string_self_array(), " . ", matrix3.string_self_array(), " = ", final_matrix.string_self_array())
                save_at.update_matrix(final_matrix)


if __name__ == "__main__":
    main()






