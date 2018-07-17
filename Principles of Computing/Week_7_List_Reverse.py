def list_reverse(my_list):
	if len(my_list) <= 1:
		return my_list
	else:
		return [my_list[-1]] + list_reverse(my_list[:-1])

'''
Solution
def list_reverse(my_list):
    """
    Takes a list my_list and returns new list
    whose elements are in reverse order
    Returns a list
    """
    if my_list == []:
        return []
    else:
        first_elem = my_list[0]
        rest_reversed = list_reverse(my_list[1 :])
        return rest_reversed + [first_elem]
'''

def test_list_reverse():
    """
    Some test cases for list_reverse
    """
    print "Computed:", list_reverse([]), "Expected: []"
    print "Computed:", list_reverse([1]), "Expected: [1]"
    print "Computed:", list_reverse([1, 2, 3]), "Expected: [3, 2, 1]"
    print "Computed:", list_reverse([2, 3, 1]), "Expected: [1, 3, 2]"
    
test_list_reverse()
print list_reverse([2, 3, 1])


