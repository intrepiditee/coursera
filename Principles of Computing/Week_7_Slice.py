#def slice(my_list, first, last):
#	if first == 0:
#		if len(my_list) > last:
#			my_list.pop()
#			return slice(my_list, first, last)
#		elif len(my_list) != 0 and len(my_list) == last:
#			my_list.pop()
#			return my_list
#		else:
#			return my_list
#	else:
#		my_list.pop(0)
#		first -= 1
#		return slice(my_list, first, last)

def slice(my_list, first, last):
	if len(my_list) == 0:
		return my_list
	if len(my_list) > last:
		my_list.pop()
		return slice(my_list, first, last)
	else:
		if first == 0:
			return my_list
		my_list.pop(0)
		first -= 1
		return slice(my_list, first, last)

'''
Solution
def slice(my_list, first, last):
    """
    Takes a list my_list and non-negative integer indices
    satisfying 0 <= first <= last <= len(my_list)
    Returns the slice my_list[first : last]
    """
    if my_list == []:
        return []
    else:
        first_elem = my_list.pop(0)
        if first > 0:  
            rest_sliced = slice(my_list, first - 1, last - 1)
            return rest_sliced
        elif last > 0:
            rest_sliced = slice(my_list, 0, last - 1)
            return [first_elem] + rest_sliced
        else:
            return []
'''

def test_slice():
    """
    Some test cases for slice
    """
    print "Computed:", slice([], 0, 0), "Expected: []"
    print "Computed:", slice([1], 0, 0), "Expected: []"
    print "Computed:", slice([1], 0, 1), "Expected: [1]"
    print "Computed:", slice([1, 2, 3], 0, 3), "Expected: [1, 2, 3]"
    print "Computed:", slice([1, 2, 3], 1, 2), "Expected: [2]"
    print "Computed:", slice([1, 1, 1, 1, 1], 3, 5), "Expected: [1, 1]"
    
test_slice()
