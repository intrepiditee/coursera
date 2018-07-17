def bin_to_dec(bin_num):
	bin_num = str(bin_num)
	if len(bin_num) == 0:
		return 0
	else:
		left_most = int(bin_num[0])
		bin_num = bin_num[1:]
		val = left_most * (2 ** len(bin_num))
		return val + bin_to_dec(bin_num)
'''
Solution
def bin_to_dec(bin_num):
    """
    Convert a binary number to decimal
    """
    if len(bin_num) == 0:
        return 0
    else:
        return 2* bin_to_dec(bin_num[:-1]) + int(bin_num[-1])
'''

print bin_to_dec(1011)