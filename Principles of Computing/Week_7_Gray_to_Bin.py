def gray_to_bin(gray_code):
	gray_code = str(gray_code)
	first = int(gray_code[0])
	second = int(gray_code[1])
	if len(str(gray_code)) == 2:
		return str(first) + str((first + second) % 2)
	else:
		gray_code = str((first + second) % 2) + gray_code[2:]
		return str(first) + gray_to_bin(gray_code)


'''
Solution
def gray_to_bin(gray_code):
    """
    Convert a Gray code to a binary number
    """
    if len(gray_code) <= 1:
        return gray_code
    else:
        significant_bits = gray_to_bin(gray_code[:-1])
        last_bit = (int(gray_code[-1]) + int(significant_bits[-1])) % 2
        return significant_bits + str(last_bit)
'''

print gray_to_bin('0011')