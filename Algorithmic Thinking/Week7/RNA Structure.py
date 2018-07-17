'''
Algorithmic Thinking RNA structure
'''

def compute_scores(input_string):
    '''
    Dynamic programming.
    Takes an RNA sequence (A, T, C, G).
    '''
    string_len = len(input_string)
    column_num = string_len / 2
    OPT = [[0 for column in range(column_num)] for row in range(string_len - column_num)]
    for k in range(5, string_len):
        for i in range(1, string_len - k):
            j = i + k
            temp = OPT[i - 1][]
            for t in range(1, string_len - 4):

            OPT[i - 1][j - 1] = max(OPT[i - 1][j - 2], max(1 + OPT[i - 1][t - 2] + OPT[t][j - 2])) 
