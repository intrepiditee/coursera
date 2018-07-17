def binary_search(list, num):
    print 'input', list
    if list[0] == num:
        return True
    elif len(list) == 1 and list[0] != num:
        return False
    else:
        first_half = list[0:len(list)//2]
        print first_half
        second_half = list[len(list)//2:]
        print second_half
        if num < second_half[0]:
            binary_search(first_half, num)
        else:
            binary_search(second_half, num)


print binary_search([1,2,3,4,5,6,7,8], 10)
