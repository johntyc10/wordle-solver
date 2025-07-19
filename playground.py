def thing(lst: list):
    lst_copy = lst.copy()
    lst_copy.remove(1)
    print(lst_copy)

lst = [i for i in range(10)]
thing(lst)
print(lst)