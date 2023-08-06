# ject
#### functional extensions

### Features
- length: get length of function parameters
- oneself: returns the parameter itself
- pipe: pipe chain of functions

### Usage
#### get length of function parameters
```python
from ject import length

def fun(a, b, *args, **kwargs): return a, b, args, kwargs

print(length(fun)) # 4
```

#### pipe chain of functions
```python
from ject import pipe

def add_one(n): return n + 1
def times_two(n): return n * 2

add_one_then_times_two = pipe(add_one, times_two)
print(add_one_then_times_two(4))  # 10
```