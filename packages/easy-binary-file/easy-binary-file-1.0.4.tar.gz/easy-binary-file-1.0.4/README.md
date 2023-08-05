# Easy Binary File Package

Easy way to use binary files with built in class and functions.

## Installation from PYPI
You can find last version of project in: https://pypi.org/project/easy-binary-file/

Command to install:
```
pip install easy-binary-file
```

## Quick use
Simply import and use functions or class

Example of function to dump a single value:
```python
from easy_binary_file import dump_single_value

dump_single_value("test_file_single.tmp", "test_value")
```

Example of function to load a single value:
```python
from easy_binary_file import load_single_value

value = load_single_value("test_file_single.tmp")
print(value)
```

Example of instance of class to dump several values:
```python
from easy_binary_file import EasyBinaryFile

with EasyBinaryFile("test_ebf_object.tmp") as ebf:
    ebf.dump("First value")
    ebf.dump("Second value")
```

Example of instance of class to read all items:
```python
from easy_binary_file import EasyBinaryFile

with EasyBinaryFile("test_ebf_object.tmp", "rb") as ebf:
    for item in ebf:
        print(item)
```


## Import
Import functions, class or all.
```python
from easy_binary_file import *
```

## Content
This is a review of class and functions content inside.

The difference between use functions vs class: 
 * Functions open and close file in each use (For use a lot, functions are slower than class)
 * Instance of class maintain open the file until end of use (or call to `close`)

**You have complete docstring documentation in code and more examples/tests in doctest format.**

### Functions:

 * `dump_ensure_space`: Only dump value if space enough in disk.
 * `dump_single_value`: Open a file in the binary mode, dump a single value and close file
 * `load_single_value`: Open a file in the binary mode, load a single value, return it and close file
 * `dump_items`: Serialize one iterable in a single file
 * `load_items`: Deserialize item by item in one stream generator
 * `quick_dump_items`: Quick open a file in ab or wb mode and dump items one by one from iterator, when generator is exhausted then close the file.
 * `quick_load_items`: Quick open a file in rb mode and load items in one generator, when generator is exhausted then close the file.

### Class:
 * `EasyBinaryFile`: Open (or create if not exist) a new binary file.
    * `close`: Close the binary file.
    * `dump`: Dump one single value in file.
    * `dump_ensure_space`: Dump one single value in file only if space enough in disk.
    * `load`: Load from file one single value.
    * `get_cursor_position`: Get last position of cursor in file.
    * `seek`: Seek file in position.
    * `get_by_cursor_position`: Get value by cursor position in file.
    * `dump_items`: Serialize one iterable in a file.
    * `load_items`: Deserialize item by item in one stream generator.
    * `__iter__`: wrap of `load_items` result to use directly in a `for` loop.


## Is useful for you?
Maybe you would be so kind to consider the amount of hours puts in, the great effort and the resources expended in 
doing this project. Thank you.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PWRRXZ2HETVG8&source=url)
