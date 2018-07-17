def make_gray(length):
	if length == 0:
		return ['']
	else:
		temp = make_gray(length - 1)
		reverse_temp = temp[::-1]
		ans = []
		for bit in temp:
			ans.append('0' + bit)
		for bit in reverse_temp:
			ans.append('1' + bit)
		return ans
'''
Solution
def make_gray(length):
    """
    Function that generates ordered list of Gray codes in 
    ascending order
    """
    if length == 0:
        return [""]
    
    all_but_first = make_gray(length - 1)
    
    answer = []
    for bits in all_but_first:
        answer.append("0" + bits)
        
    all_but_first.reverse()
    
    for bits in all_but_first:
        answer.append("1" + bits)
    return answer
'''

print make_gray(3)
