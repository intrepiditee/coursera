'''
Algorithmic Thinking Project 4

1) build_scoring_matrix
2) compute_alignment_matrix
3) compute_global_alignment
4) compute_local_alignment
'''

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    '''
    Takes a set of characters, and three scores.
    Returns a scoring matrix as a dictionary of dictionaries whose entries are indexed by pairs of characters.
    '''
    scoring_matrix = {}
    scoring_matrix['-'] = {'-': dash_score}

    for char1 in alphabet:
        scoring_matrix[char1] = {}
        scoring_matrix[char1]['-'] = dash_score
        scoring_matrix['-'][char1] = dash_score

        for char2 in alphabet:
            if char1 == char2:
                scoring_matrix[char1][char2] = diag_score
            else:
                scoring_matrix[char1][char2] = off_diag_score

    return scoring_matrix

    # new_alphabet = set(alphabet)
    # new_alphabet.add('-')

    # for char1 in new_alphabet:
    #     if char1 not in scoring_matrix:
    #         scoring_matrix[char1] = {}

    #     for char2 in new_alphabet:
    #         if char1 == '-' or char2 == '-':
    #             scoring_matrix[char1][char2] = dash_score
    #         else:
    #             if char1 == char2:
    #                 scoring_matrix[char1][char2] = diag_score
    #             else:
    #                 scoring_matrix[char1][char2] = off_diag_score

    # return scoring_matrix


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    '''
    Takes two strings, a scoring matrix, and a Boolean indicating global or local.
    Returns the alignment matrix.
    '''
    x_len = len(seq_x)
    y_len = len(seq_y)
    alignment_matrix = [[0 for dummy in range(y_len + 1)] for dummy in range(x_len + 1)]

    for x_sub_len in range(1, x_len + 1):
        alignment_matrix[x_sub_len][0] = alignment_matrix[x_sub_len - 1][0] + scoring_matrix[seq_x[x_sub_len - 1]]['-']
        if not global_flag and alignment_matrix[x_sub_len][0] < 0:
            alignment_matrix[x_sub_len][0] = 0

    for y_sub_len in range(1, y_len + 1):
        alignment_matrix[0][y_sub_len] = alignment_matrix[0][y_sub_len - 1] + scoring_matrix['-'][seq_y[y_sub_len - 1]]
        if not global_flag and alignment_matrix[0][y_sub_len] < 0:
            alignment_matrix[0][y_sub_len] = 0

    for x_sub_len in range(1, x_len + 1):
        for y_sub_len in range(1, y_len + 1):

            alignment_matrix[x_sub_len][y_sub_len] = \
            max([alignment_matrix[x_sub_len - 1][y_sub_len - 1] + scoring_matrix[seq_x[x_sub_len - 1]][seq_y[y_sub_len - 1]],
                 alignment_matrix[x_sub_len - 1][y_sub_len] + scoring_matrix[seq_x[x_sub_len - 1]]['-'],
                 alignment_matrix[x_sub_len][y_sub_len - 1] + scoring_matrix['-'][seq_y[y_sub_len - 1]]])

            if not global_flag and  alignment_matrix[x_sub_len][y_sub_len] < 0:
                alignment_matrix[x_sub_len][y_sub_len] = 0
    
    return alignment_matrix


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Implementation of ComputeAlignment.

    Takes two strings, a scoring matrix, and the alighment matrix.
    Returns a tuple containing the score, and the two optimal global alignments.
    '''
    x_len = len(seq_x)
    y_len = len(seq_y)
    score = alignment_matrix[x_len][y_len]
    x_alignment = ''
    y_alignment = ''

    while x_len != 0 and y_len != 0:
        if alignment_matrix[x_len][y_len] == alignment_matrix[x_len -1][y_len - 1] + scoring_matrix[seq_x[x_len - 1]][seq_y[y_len - 1]]:
            x_alignment = seq_x[x_len - 1] + x_alignment
            y_alignment = seq_y[y_len - 1] + y_alignment
            x_len -= 1
            y_len -= 1
        else:
            if alignment_matrix[x_len][y_len] == alignment_matrix[x_len - 1][y_len] + scoring_matrix[seq_x[x_len - 1]]['-']:
                x_alignment = seq_x[x_len - 1] + x_alignment
                y_alignment = '-' + y_alignment
                x_len -= 1
            else:
                x_alignment = '-' + x_alignment
                y_alignment = seq_y[y_len - 1] + y_alignment
                y_len -= 1

    while x_len != 0:
        x_alignment = seq_x[x_len - 1] + x_alignment
        y_alignment = '-' + y_alignment
        x_len -= 1

    while y_len != 0:
        x_alignment = '-' + x_alignment
        y_alignment = seq_y[y_len - 1] + y_alignment
        y_len -= 1

    return (score, x_alignment, y_alignment)


def find_max(matrix):
    '''
    Takes a list of lists.
    Returns the maximum value, and the indices as a tuple of the entry that has the maximum value.
    '''
    max_row_index = 0
    max_column_index = 0
    max_value = matrix[max_row_index][max_column_index]

    for row_index in range(len(matrix) - 1, -1, -1):
        for column_index in range(len(matrix[row_index]) - 1, -1, -1):

            if matrix[row_index][column_index] > max_value:
                max_value = matrix[row_index][column_index]
                max_row_index = row_index
                max_column_index = column_index

    return (max_value, max_row_index, max_column_index)


# print find_max([[1, 2, 3], [4, 5, 6]])


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Implementation of modified ComputeAlignment.

    Takes two strings, a scoring matrix, and the alighment matrix.
    Returns a tuple containing the score, and the two optimal local alignments.
    '''
    max_value = find_max(alignment_matrix)
    x_len = max_value[1]
    y_len = max_value[2]
    x_alignment = ''
    y_alignment = ''

    while x_len != 0 and y_len != 0:

        if alignment_matrix[x_len][y_len] == 0:
            break

        if alignment_matrix[x_len][y_len] == alignment_matrix[x_len -1][y_len - 1] + scoring_matrix[seq_x[x_len - 1]][seq_y[y_len - 1]]:
            x_alignment = seq_x[x_len - 1] + x_alignment
            y_alignment = seq_y[y_len - 1] + y_alignment
            x_len -= 1
            y_len -= 1
        else:
            if alignment_matrix[x_len][y_len] == alignment_matrix[x_len - 1][y_len] + scoring_matrix[seq_x[x_len - 1]]['-']:
                x_alignment = seq_x[x_len - 1] + x_alignment
                y_alignment = '-' + y_alignment
                x_len -= 1
            else:
                x_alignment = '-' + x_alignment
                y_alignment = seq_y[y_len - 1] + y_alignment
                y_len -= 1

    while x_len != 0:

        if alignment_matrix[x_len][y_len] == 0:
            break

        x_alignment = seq_x[x_len - 1] + x_alignment
        y_alignment = '-' + y_alignment
        x_len -= 1

    while y_len != 0:

        if alignment_matrix[x_len][y_len] == 0:
            break

        x_alignment = '-' + x_alignment
        y_alignment = seq_y[y_len - 1] + y_alignment
        y_len -= 1

    score = 0
    for index in range(len(x_alignment)):
        score += scoring_matrix[x_alignment[index]][y_alignment[index]]

    return (score, x_alignment, y_alignment)

# Test   

# scoring_matrix = build_scoring_matrix({'a', 'b', 'c'}, 10, 3, -2)
# for i in scoring_matrix.items():
#     print i

# print

# alignment_matrix = compute_alignment_matrix('cabba', 'bbaac', scoring_matrix, False)
# print alignment_matrix

# print compute_local_alignment('cabba', 'bbaac', scoring_matrix, alignment_matrix)



