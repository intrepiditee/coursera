def number_of_threes(num):
	num = str(num)
	if num == '0':
		return 0
	elif num[0] == '3' and len(num) == 1:
		return 1
	elif num[0] == '3':
		num = int(num[1:])
		return 1 + number_of_threes(num)
	elif len(num) == 1:
		return 0
	else:
		num = int(num[1:])
		return number_of_threes(num)

'''
Solution
def number_of_threes(num):
    """
    Takes a non-negative integer num and compute the 
    number of threes in its decimal form
    Returns an integer
    """
    if num == 0:
        return 0
    else:
        unit_digit = num % 10
        threes_in_rest = number_of_threes(num // 10)
        if unit_digit == 3:
            return threes_in_rest + 1
        else:
            return threes_in_rest
'''

print number_of_threes(334533)
def test_number_of_threes():
    """
    Some test cases for number_of_threes
    """
    print "Computed:", number_of_threes(0), "Expected: 0"
    print "Computed:", number_of_threes(5), "Expected: 0"
    print "Computed:", number_of_threes(3), "Expected: 1"
    print "Computed:", number_of_threes(33), "Expected: 2"
    print "Computed:", number_of_threes(34534), "Expected: 2"
    
test_number_of_threes()