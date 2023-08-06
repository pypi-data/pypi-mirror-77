# way
##### filesystem tools

### Usage
```python
from way import get_files

SRC = './'
files = get_files(SRC, 
                  predicate=lambda f: not f.startswith('_'), 
                  extension='.py')
print(SRC, ':', files)
```