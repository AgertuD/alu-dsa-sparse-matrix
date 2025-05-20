class CompressedMatrix:
    def __init__(self, row_cnt, col_cnt):
        """
        Initializes an empty compressed matrix of given dimensions.

        Parameters: row_cnt (int): Number of rows, col_cnt (int): Number of columns.
        """
        self.num_rows = row_cnt
        self.num_cols = col_cnt
        self.sparse_data = {}

    @staticmethod
    def _read_file(file_path):
        """
        Reads and returns non-empty lines from a file.

        Parameters: file_path (str): Path to the input file.
        Returns: list of str: Lines from the file.
        """
        try:
            with open(file_path.replace("\\", "/"), "r") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    @classmethod
    def load_from_file(cls, file_path):
        """
        Creates and returns a CompressedMatrix instance from a file.

        Parameters: file_path (str): Path to the matrix file.
        Returns: CompressedMatrix: Loaded matrix.
        """
        lines = cls._read_file(file_path)

        if len(lines) < 2:
            raise ValueError(f"File {file_path} must contain at least two lines for matrix dimensions.")

        try:
            r = int(lines[0].split('=')[1])
            c = int(lines[1].split('=')[1])
        except (IndexError, ValueError):
            raise ValueError(f"Invalid matrix dimensions in {file_path}.")

        instance = cls(r, c)

        for entry in lines[2:]:
            if not entry.startswith("(") or not entry.endswith(")"):
                raise ValueError(f"Invalid format: {entry}")
            try:
                i, j, v = map(lambda x: int(x.strip()), entry[1:-1].split(','))
            except:
                raise ValueError(f"Invalid entry: {entry}")
            instance.set_cell(i, j, v)
        return instance

    def set_cell(self, r, c, v):
        """
        Sets the value of a cell in the matrix.

        Parameters: r (int): Row index, c (int): Column index, v (int): Value to set.
        """
        if r >= self.num_rows:
            self.num_rows = r + 1
        if c >= self.num_cols:
            self.num_cols = c + 1
        self.sparse_data[f"{r},{c}"] = v

    def get_cell(self, r, c):
        """
        Retrieves the value of a cell; returns 0 if not explicitly set.

        Parameters: r (int): Row index, c (int): Column index.
        Returns: int: Cell value.
        """
        return self.sparse_data.get(f"{r},{c}", 0)

    def export_to_file(self, out_path):
        """
        Saves the matrix to a file in sparse format.

        Parameters: out_path (str): Path to output file.
        """
        with open(out_path, 'w') as f:
            f.write(f"rows={self.num_rows}\n")
            f.write(f"cols={self.num_cols}\n")
            for k, v in self.sparse_data.items():
                r, c = k.split(',')
                f.write(f"({r}, {c}, {v})\n")

    def add_with(self, other):
        """
        Returns the sum of this matrix and another matrix.

        Parameters: other (CompressedMatrix): Matrix to add.
        Returns: CompressedMatrix: Sum result.
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices must have the same dimensions.")

        result = CompressedMatrix(self.num_rows, self.num_cols)

        for k, v in self.sparse_data.items():
            i, j = map(int, k.split(','))
            result.set_cell(i, j, v)

        for k, v in other.sparse_data.items():
            i, j = map(int, k.split(','))
            result.set_cell(i, j, result.get_cell(i, j) + v)

        return result

    def subtract_with(self, other):
        """
        Returns the difference between this matrix and another matrix.

        Parameters: other (CompressedMatrix): Matrix to subtract.
        Returns: CompressedMatrix: Difference result.
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices must have the same dimensions.")

        result = CompressedMatrix(self.num_rows, self.num_cols)

        for k, _ in self.sparse_data.items():
            i, j = map(int, k.split(','))
            result.set_cell(i, j, self.get_cell(i, j))

        for k, v in other.sparse_data.items():
            i, j = map(int, k.split(','))
            result.set_cell(i, j, result.get_cell(i, j) - v)

        return result

    def multiply_with(self, other):
        """
        Returns the product of this matrix with another matrix.

        Parameters: other (CompressedMatrix): Matrix to multiply with.
        Returns: CompressedMatrix: Multiplication result.
        """
        if self.num_cols != other.num_rows:
            raise ValueError("Invalid dimensions for multiplication.")

        result = CompressedMatrix(self.num_rows, other.num_cols)

        for k1, v1 in self.sparse_data.items():
            r1, c1 = map(int, k1.split(','))
            for k2, v2 in other.sparse_data.items():
                r2, c2 = map(int, k2.split(','))
                if c1 == r2:
                    result.set_cell(r1, c2, result.get_cell(r1, c2) + v1 * v2)

        return result


def get_input(prompt_msg):
    """
    Wrapper for input() to allow easier testing and potential UI redirection.

    Parameters: prompt_msg (str): Prompt to display to the user.
    Returns: str: User input.
    """
    return input(prompt_msg)

def run_operations():
    """
    Command-line interface to perform matrix operations based on user input.
    """
    try:
        ops_map = {
            '1': ('addition', lambda a, b: a.add_with(b)),
            '2': ('subtraction', lambda a, b: a.subtract_with(b)),
            '3': ('multiplication', lambda a, b: a.multiply_with(b))
        }

        print("Matrix Operations:\n(1) Addition\n(2) Subtraction\n(3) Multiplication")
        choice = get_input("Select operation (1, 2, 3): ")
        if choice not in ops_map:
            raise ValueError("Invalid option selected.")

        path1 = get_input("Enter path for first matrix: ")
        path2 = get_input("Enter path for second matrix: ")

        print(f"Loading from {path1}...")
        mat_a = CompressedMatrix.load_from_file(path1)
        print(f"Size: {mat_a.num_rows}x{mat_a.num_cols}")

        print(f"Loading from {path2}...")
        mat_b = CompressedMatrix.load_from_file(path2)
        print(f"Size: {mat_b.num_rows}x{mat_b.num_cols}")

        op_name, op_func = ops_map[choice]
        print(f"Performing {op_name}...")
        result_mat = op_func(mat_a, mat_b)

        output_file = f"{op_name}_result.txt"
        result_mat.export_to_file(output_file)
        print(f"{op_name.capitalize()} complete. Saved to {output_file}.")

    except Exception as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    run_operations()
