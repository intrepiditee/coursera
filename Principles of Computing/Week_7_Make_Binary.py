def make_binary(length):
	if length == 0:
		return ['']
	else:
		temp = make_binary(length - 1)
		ans = []
		for bit in temp:
			ans.append(bit + '0')
			ans.append(bit + '1')
		return ans

'''
Solution
def make_binary(length):
    """
    Function that generates ordered list of binary numbers in 
    ascending order
    """
    if length == 0:
        return [""]
    
    all_but_first = make_binary(length - 1)
    
    answer = []
    for bits in all_but_first:
        answer.append("0" + bits)
    for bits in all_but_first:
        answer.append("1" + bits)
    return answer
'''

print make_binary(5)