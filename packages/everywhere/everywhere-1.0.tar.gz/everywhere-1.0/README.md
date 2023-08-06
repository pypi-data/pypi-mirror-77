# Everywhere

The everywhere package is a utility package that allows importing a single thread local variable form everywhere.

The only purpose of this package is to abstract the import location from any specific project or file.

Sample usage:
```
from everywhere import box

box.data = "This will be visible wherever else the box is imported."
```

## Building

Installation: `pip install --user --upgrade setuptools wheel`

Build with: `python setup.py sdist bdist_wheel`
