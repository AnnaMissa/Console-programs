'''
Некоторые алгоритмы сортировки,
реализованные на Python.
'''


from random import shuffle, choice


def list_to_sort():
    # создаёт список для сортировки
    a = [el for el in range(1, 1000)]
    shuffle(a)
    return a


def bubble_sort(array):
    count = 1
    while count < len(array):
        array_sort = True
        for i in range(len(array)-count):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
                array_sort = False  # проверяет была ли перестановка за последний проход
                ind = i + 1  # сохраняет индекс+1 последнего обмена
        if array_sort:
            break
        if len(array)-count > ind:
            count = len(array) - ind
        count += 1
    return array


def cocktail_sort(array):
    left = 0
    right = len(array) - 1
    while left != right:
        for i in range(left, right):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
                ind = i  # сохраняет индекс последнего обмена
        right = ind
        for i in range(right, left, -1):
            if array[i] < array[i-1]:
                array[i], array[i-1] = array[i-1], array[i]
                ind = i
        left = ind
    return array


def insertion_sort(array):
    for i in range(1, len(array)):
        while i > 0 and array[i] < array[i-1]:
            array[i], array[i-1] = array[i-1], array[i]
            i -= 1
    return array


def gnome_sort(array):
    i = 1
    while i < len(array):
        if array[i] < array[i-1]:
            array[i], array[i-1] = array[i-1], array[i]
            i -= 1 if i != 1 else 0
        else:
            i += 1
    return array


def merge_sort(array):
    if len(array) > 1:
        left = array[:len(array)//2]
        right = array[len(array)//2:]
        merge_sort(left)
        merge_sort(right)
        i, j, z = 0, 0, 0
        while i < len(left) and j < len(right):  # слияние двух масиивов
            if left[i] < right[j]:
                array[z] = left[i]
                i += 1
            else:
                array[z] = right[j]
                j += 1
            z += 1
        while i < len(left):  # добавление элементов массива после слияния
            array[z] = left[i]
            i += 1
            z += 1
        while j < len(right):  # добавление элементов массива после слияния
            array[z] = right[j]
            j += 1
            z += 1
    return array


def selection_sort(array):  # неустойчивая
    min_ind, j = 0, 0
    while j < len(array):
        for i in range(j+1, len(array)):
            if array[i] < array[min_ind]:
                min_ind = i
        array[j], array[min_ind] = array[min_ind], array[j]
        j += 1
        min_ind = j
    return array


def selection_sort_stable(array):
    for i in range(len(array)):
        min_ind = i
        for j in range(i+1, len(array)):
            if array[j] < array[min_ind]:
                min_ind = j
        if i != min_ind:
            temp = array[min_ind]
            for k in range(min_ind, i-1, -1):
                array[k] = array[k-1]
            array[i] = temp
    return array


def comb_sort(array):  # неустойчивая
    step = len(array)
    while step > 1:
        step = round(step / 1.247) if step != 2 else 1
        i = 0
        while i+step < len(array):
            if array[i] > array[step+i]:
                array[i], array[step+i] = array[step+i], array[i]
            i += 1
    return array


def quick_sort(array):  #неустойчивая, с использованием дополнительной памяти
    if len(array) <= 1:
        return array
    else:
        a = choice(array)
        left = [el for el in array if el < a]
        right = [el for el in array if el >= a]
        return quick_sort(left) + quick_sort(right)
    return array


print(quick_sort(list_to_sort()))
