# Matrix Calculator

This is my final programming project of the first class in programming [NPRG030](https://is.cuni.cz/studium/eng/predmety/index.php?do=predmet&kod=NPRG030) as part of my Computer Science undergraduate curriculum at Charles University, Prague, CZ, EU. 

Designed, developed and programmed by [Matyas Urban](https://www.linkedin.com/in/matyasurban/) in March 2020.

## Goal and Task

The goal of this project is to create a program that supports commong matrix operations and allows the user to manipulate matrices and investigate them (using a terminal/command prompt).

### Detailed Description
The program will load two matrices from a text file. Then the user will interact within the terminal by performing operations on the matrices. Each user request and each request result will be printed and will be appended to another text file, which will serve as calculator history. The matrices resulting from the operations will have to be stored for continuation of other calculations. Either overwriting the starting matrices or overwriting a third matrix available as a storage variable.

## Input Structure

For the program to function correctly there must be 3 files in the same directory:
- matrixCalculator.py 
- input.txt 
- record.txt 

### input.txt

In this file must be two matrices as text form in the following format:

- First matrix starts on the first line
- First row are numbers (negative with a minus sum in front of them) seperated by a space character
- Every other row in the same format on a consecutive line 
- Second matrix is divided from the first line by an empty line 
- Same rules apply to the second matrix 

Example of a correctly formatted input.txt file

```
0 0 3
3 5 1
1 0 2

1 1 -1 -1
1 -2 3 4
1 3 -6 10
1 4 10 20
```

Please use single or double digit number for pleasant experience with the program. When length of a matrix element exceeds 3 digits, the output structure gets messy (all results are perfectly readable, though not perfectly aligned columns).
###Important Assumption

For simplicity and precision I decided to restrict my program only to integer values, be it matrix elements, or scaling a matrix, user input must always be integer.

### matrixCalculator.py 

When the input.txt is correctly formatted, you are ready to go and run matrixCalculator.py.

For the sake of simplicity of this guide and connected output formats, this is my input.txt:

```
-1 2
5 -3

3
4
```
Now matrixCalculator.py saves the first matrix into variable of a Matrix object as matrix_A (referred as `A` in the input), the second one as `B` and creates also a placeholder matrix `X`, so that when you calculate for example the sum of A + B and you don't want the result to override one of the original matrices, you can save it into X. There are however no other placeholder matrices (though it is easy to add them in matrixCalculator.py) and keep in mind that most operations require you to choose a matrix A/B/X at which you'd like to save the resulting matrix.

When you run the program ...

```
matyasurban@Matyass-MacBook-Air MatrixCalculator % python3 matrixCalculator.py
```

you'll be greeted with these words:

```
WELCOME TO MATRIX CALCULATOR
Starting Matrices: Matrix A = |   -1  2   |     Matrix B = |   3   |     Matrix X = |   0   |
                              |   5   -3  |                |   4   |                         


Write your command:
```
And now comes the fun part: writing the commands (calculations).

There are 10 of them:

```
END outputs the final state of all matrices and ends the session
PRI (print) outputs the current state of the matrix (aka prints it)
DET (determinant) outputs the determinant of the given matrix
INV (invertibility) outputs the invertibility of a given matrix
TRA (transpose) outputs the transpose of a given matrix and saves it into save_at_matrix
SCA (scaling) outputs scaled version of a given matrix by a given scalar and saves it into save_at_matrix
--- the scalar must be an integer
POW (power) outputs given matrix raised to a given power and saves it into save_at_matrix
--- the power must be a positive integer
ADD (addition) outputs the sum of two given matrices and saves it into save_at_matrix
SUB (subtraction) outputs the difference of two given matrices and saves it into save_at_matrix
MUL (multiplication) outputs the product of two given matrices and saves it into save_at_matrix
```
Now I will introduce the command structure

#### PRI matrix

Matrix can only be A/B/X. For example, let's find out what matrix A holds now by typing 'PRI A'':
```
Write your command: PRI A
Valid command.
Working...
Matrix A = |   -1  2   |
           |   5   -3  |
```

#### DET matrix

Matrix can only be A/B/X. For example, let's find out what the determinant of matrix A is by typing 'DET A'':
``` 
Write your command: DET A
Valid command.
Working...
det(|   -1  2   |) = -7
    |   5   -3  |      
```

#### INV matrix

Matrix can only be A/B/X. For example, let's find out whether A is invertible by typing 'INV A':
``` 
Write your command: INV A
Valid command.
Working...
|   -1  2   | is invertible.
|   5   -3  |    
```

#### TRA save_at_matrix given_matrix
This transposes the given matrix and saves the result into save at matrix. Both arguments must be A/B/X. Let's transpose A and overwrite its value. Then, let's print A to check that it has been indeed overwritten.

``` 
Write your command: TRA A A
Valid command.
Working...
transpose(|   -1  2   |) = |   -1  5   |
          |   5   -3  |    |   2   -3  |



Write your command: PRI A
Valid command.
Working...
Matrix A = |   -1  5   |
           |   2   -3  |
```

#### SCA save_at_matrix given_matrix scalar
This scales the given matrix by integer scalar and saves it into save at matrix. Both arguments must be A/B/X and the third one an integer. Let's scale B by -2 and save it to X. We will verify again by printing relevant matrices.

``` 
Write your command: SCA X B -2
Valid command.
Working...
-2 * |   3   | = |   -6  |
     |   4   |   |   -8  |



Write your command: PRI B
Valid command.
Working...
Matrix B = |   3   |
           |   4   |



Write your command: PRI X
Valid command.
Working...
Matrix X = |   -6  |
           |   -8  |
```

#### POW save_at_matrix given_matrix power

This raises given matrix to an integer power and save it into save at matrix. Both arguments must be A/B/X and the third one a positive integer. Let's raise A to the power of 2 and save it into X.

``` 
Write your command: POW X A 2
Valid command.
Working...
|   -1  5   | raised to the power of 2 = |   11  -20 |
|   2   -3  |                            |   -8  19  |



Write your command: PRI A
Valid command.
Working...
Matrix A = |   -1  5   |
           |   2   -3  |



Write your command: PRI X
Valid command.
Working...
Matrix X = |   11  -20 |
           |   -8  19  |
```

#### MUL save_at_matrix matrix_1 matrix_2
This multiplies matrix 1 and matrix 2 and saves the result into save at matrix. All three arguments must be A/B/X. Let's multiply A and B and store it into A.

``` 
Write your command: MUL A A B
Valid command.
Working...
|   -1  5   | . |   3   | = |   17  |
|   2   -3  |   |   4   |   |   -6  |



Write your command: PRI A
Valid command.
Working...
Matrix A = |   17  |
           |   -6  |
```

#### ADD save_at_matrix matrix_1 matrix_2
This adds matrix 1 and matrix 2 and saves the result into save at matrix. All three arguments must be A/B/X. Let's sum A and B up and store it into A.

``` 
Write your command: ADD A A B
Valid command.
Working...
|   17  | + |   3   | = |   20  |
|   -6  |   |   4   |   |   -2  |



Write your command: PRI A
Valid command.
Working...
Matrix A = |   20  |
           |   -2  |
```
#### SUB save_at_matrix matrix_1 matrix_2
This subtracts matrix 1 and matrix 2 and saves the result into save at matrix. All three arguments must be A/B/X. Let's subract A and B and store it into B.

``` 
Write your command: SUB B A B
Valid command.
Working...
|   20  | - |   3   | = |   17  |
|   -2  |   |   4   |   |   -6  |



Write your command: PRI B
Valid command.
Working...
Matrix B = |   17  |
           |   -6  |
```

#### END 
This prints the final state of all three matrices and ends the program. 

```
Write your command: END
Valid command.
Working...
Final Matrices: Matrix A = |   20  |     Matrix B = |   17  |     Matrix X = |   11  -20 |
                           |   -2  |                |   -6  |                |   -8  19  |

Goodbye.
```
### record.txt 

This file does not require any action on your part. However, it includes useful information about your session with the calculating, outlining every request and every result in a very organized way. The history of a session is available after you write the `END` command or after you kill the program from IDE controls.
If you are interested, here is the history of operations described above:

``` 
### Session | 2022-03-25 03:13:23.155021 | ###
Starting Matrices: Matrix A = |   -1  2   |     Matrix B = |   3   |     Matrix X = |   0   |
                              |   5   -3  |                |   4   |                         

COMMAND #1: PRI A
Matrix A = |   -1  2   |
           |   5   -3  |

COMMAND #2: DET A
det(|   -1  2   |) = -7
    |   5   -3  |      

COMMAND #3: INV A
|   -1  2   | is invertible.
|   5   -3  |               

COMMAND #4: TRA A A
transpose(|   -1  2   |) = |   -1  5   |
          |   5   -3  |    |   2   -3  |

COMMAND #5: PRI A
Matrix A = |   -1  5   |
           |   2   -3  |

COMMAND #6: SCA X B -2
-2 * |   3   | = |   -6  |
     |   4   |   |   -8  |

COMMAND #7: PRI B
Matrix B = |   3   |
           |   4   |

COMMAND #8: PRI X
Matrix X = |   -6  |
           |   -8  |

COMMAND #9: POW X A 2
|   -1  5   | raised to the power of 2 = |   11  -20 |
|   2   -3  |                            |   -8  19  |

COMMAND #10: PRI A
Matrix A = |   -1  5   |
           |   2   -3  |

COMMAND #11: PRI X
Matrix X = |   11  -20 |
           |   -8  19  |

COMMAND #12: MUL A A B
|   -1  5   | . |   3   | = |   17  |
|   2   -3  |   |   4   |   |   -6  |

COMMAND #13: PRI A
Matrix A = |   17  |
           |   -6  |

COMMAND #14: ADD A A B
|   17  | + |   3   | = |   20  |
|   -6  |   |   4   |   |   -2  |

COMMAND #15: SUB B A B
|   20  | - |   3   | = |   17  |
|   -2  |   |   4   |   |   -6  |

COMMAND #16: PRI B
Matrix B = |   17  |
           |   -6  |

COMMAND #17: END
Final Matrices: Matrix A = |   20  |     Matrix B = |   17  |     Matrix X = |   11  -20 |
                           |   -2  |                |   -6  |                |   -8  19  |
```
Note that history is appended to the end of the file so all your previous sessions are still recorded in the file.

## Features and concepts used in my implementation of the solution 

- Lists (Dynamic Array) and Dictionaries (Hash Table)
- Object Oriented Programming
- Getters and Setters
- String Manipulation 
- Array Slicing
- List Comprehension 
- Functional Decomposition 
- Recursive Approach
- File I/O (Reading and Writing)
- Literal String Interpolation
- Datetime Module
- Control Flow 
- Unknown Count of Function Parameters
- Exception Handling

## Final Assessment 

Thanks to tight restrictions of the user input, this program provides a seamless user experience and allows for convenient matrix calcuations. However, this aspect can be limiting. In future iterations allowing real numbers as matrix elements and scalars would be a good step forward. Another extremely useful matrix operation would be gaussian elimination and connected matrix transformation into reduced/not-reduced row echolen form. That would require handling also floating point arithmetic.
