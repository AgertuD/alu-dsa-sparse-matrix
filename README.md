# Sparse Matrix Operations

This project implements **sparse matrix operations** (addition, subtraction, and multiplication) using a **dictionary-based compression format** in Python.

Sparse matrices store only **non-zero elements**, making them memory-efficient for large matrices with few values.

---

##  Requirements

- Python 3.6+
- No external libraries required

---

## How to Use

1. Clone the repository:
   ```
   git clone https://github.com/AgertuD/alu-dsa-sparse-matrix.git
   cd alu-dsa-sparse-matrix
   ```

2. Run the program:

```
cd src
python3 SparseMatrix.py
```
The program will ask you to choose the operation from 3 provided choices

```
(1) Addition
(2) Subtraction
(3) Multiplication
```

Depending on your chice you will be asked to enter a path to your matrix files

## File Format

Input matrices should be stored in text files with the following format:

```
rows=<number_of_rows>
cols=<number_of_columns>
(row, column, value)
(row, column, value)
...
```

Example:
```
rows=3
cols=3
(0, 0, 1)
(1, 1, 2)
(2, 2, 3)
```

## Supported Operations

1. **Addition**: Adds two sparse matrices element-wise.
2. **Subtraction**: Subtracts the second matrix from the first element-wise.
3. **Multiplication**: Performs matrix multiplication of the two input matrices.

## Output

The result of the operation is saved to a file named `operation_results.txt` in the same format as the input files.

## Error Handling

The program includes error handling for:

- Invalid file formats
- Mismatched matrix dimensions for operations
- File read/write errors

If an error occurs, an appropriate error message will be displayed.
