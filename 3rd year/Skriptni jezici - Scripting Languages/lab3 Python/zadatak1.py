import sys 

def get_matrices(input_path):
    matrices = []
    first_line = True
    matrix = {'num_rows_cols': (0, 0), 'elements': {}}
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if first_line:
                rows_cols = line.split(' ')
                rows, columns = rows_cols[0], rows_cols[1]
                matrix['num_rows_cols'] = (rows, columns)
                first_line = False
            elif line == '':
                matrices.append(matrix)
                first_line = True
                matrix = {'num_rows_cols': (0, 0), 'elements': {}}
            elif len(line.split(' ')) == 3:
                element = line.split(' ')
                line, stupac, value = int(element[0]), int(element[1]), float(element[2])
                matrix['elements'][(line, stupac)] = value
        matrices.append(matrix)

    if len(matrices) != 2:
       return -1
    
    return matrices

def print_full_form(matrix, naziv):
    print(f"{naziv}:")
    rows, columns = matrix['num_rows_cols']
    for i in range(int(rows)):
        row = []
        for j in range(int(columns)):
            if (i, j) in matrix['elements']:
                value = matrix['elements'][(i, j)]
                row.append(f"{value:.2f}")
            else:
                value = 0
                row.append(f"{value:.2f}")
        row_output = ' '.join(row)
        print(f"  {row_output}")
    print()

def multiply_matrices(A, B):
    rowsA, columnsA = A['num_rows_cols']
    rowsB, columnsB = B['num_rows_cols']

    if columnsA != rowsB:
        return -1
                                 
    result_matrix_multiply = {'num_rows_cols': (rowsA, columnsB), 'elements': {}}

    for (i, k) in A['elements']:
        v1 = A['elements'][(i, k)]
        for j in range(int(columnsB)):
            if (k, j) in B['elements']:
                v2 = B['elements'][(k, j)]
                if (i, j) in result_matrix_multiply['elements']:
                    result_matrix_multiply['elements'][(i, j)] = result_matrix_multiply['elements'][(i, j)] + v1 * v2
                else:
                    result_matrix_multiply['elements'][(i, j)] = 0 + v1 * v2

    return result_matrix_multiply

def save_matrices(matrix, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        rows, columns = matrix['num_rows_cols']
        f.write(f"{rows} {columns}\n")
        for (i, j) in matrix['elements']:
            v = matrix['elements'][(i, j)]
            f.write(f"{i} {j} {v:.2f}\n")


entry = sys.argv

input_path = entry[1]
output_path = entry[2]

matrices = get_matrices(input_path)
if matrices != -1:
    A, B = matrices[0], matrices[1]

    print_full_form(A, 'A')
    print_full_form(B, 'B')

    AB = multiply_matrices(A, B)
    if AB != -1:

        print_full_form(AB, 'A*B')
        save_matrices(AB, output_path)

    else:
        print('Dimensions are not compatible for multiplication')
else:
    print('Two matrices were not loaded')