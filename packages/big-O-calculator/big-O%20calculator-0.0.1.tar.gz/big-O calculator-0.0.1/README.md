# Big-O Caculator

A big-O calculator to estimate time complexity of sorting arrays.

inspired by : https://github.com/ismaelJimenez/cpp.leastsq

# Usage

You can call which array to test

```py
Big-O calculator

Args:
    functionName ([string]): function name to call
    array ([string]): "random", "sorted", "reversed", "partial"
  
```

```py
from bigO import bigO

def bubbleSort(array):  # in-place | stable
    """
    Best : O(n) | O(n) Space
    Average : O(n^2) | O(n) Space
    Worst : O(n^2) | O(n) Space
    """
    isSorted = False
    i = 0
    while not isSorted:
        isSorted = True
        for j in range(len(array) - 1 - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                isSorted = False

    return array
    
tester = bigO.bigO()
complexity, _ = tester.test(bubbleSort, "random")

print(complexity)  # O(N^2)

```