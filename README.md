# sharearray
Have you worried about creating large identical numpy arrays across processes due to RAM wastage, e.g. datasets that are big enough to fit in RAM but large enough to cause concern when running multiple jobs using the same data?
`sharearray` efficiently caches numpy arrays in RAM (using shared memory in `/dev/shm`, no root needed) locally on a machine.

Usage is simple, using the `cache` function or `decorator` decorator.
A first call saves the result of the call into the built-in RAM disk, and
returns a read-only memory-mapped view into it.
Since it's in RAM, there's no performance penalty.
Any subsequent calls with the same ID will return an identical read-only memory mapped view,
even across processes. The IDs are **global**.

Installation:
```
pip install git+https://github.com/bshillingford/python-sharearray
```
or
```
git clone https://github.com/bshillingford/python-sharearray
python setup.py install
```

## Usage
### Using `decorator`:
```python
@sharearray.decorator('some_unique_id', verbose=False)
def get_training_data():
    # create largeish / expensive-to-generate data
    return my_array # some instance of np.ndarray

# first call, across all processes, creates the array
arr_view = get_training_data()

# all further calls are cached/memoized: we return a view into memory
arr_view_2 = get_training_data()
```

### Using the `cache` function:
```python
import sharearray
import numpy as np
arr = sharearray.cache('my_global_id', lambda: create_large_array())
# or:
arr = sharearray.cache('my_global_id', lambda: create_large_array())
```
where, for instance, `create_large_array` returns a large training set, potentially performing expensive feature transformations or data augmentations first.

By default, the file is at `/dev/shm/sharearray_my_global_id.npy`, and to avoid concurrency
issues when first generating the array, and to avoid duplicated computation, 

For futher details, read the docstrings. You may be interested in the `timeout`, `verbose`, and `log_func` arguments (to either `cache` or `decorator`).

### PyTorch
Since PyTorch does not yet support memmapped files (at time of writing), we can instead just create torch Tensors that point to the memory mapped by numpy:
```python
data_numpy = get_training_data()          # numpy.ndarray
data_torch = torch.from_numpy(data_numpy) # torch.Tensor
```

## Notes
TODO: support returning multiple arrays (e.g. as a tuple or dict) from the callback / decorated function

There exist similar libraries in Python already, but this just makes it easier to do as a memoization-style API. Also, this module is a single file, and does not write anything in C.
