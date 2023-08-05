# htmlcomparator

## Usage

To start using the comparator, first import the package, and make an object.

```python
from htmlcomparator import HTMLComparator
comparator = HTMLComparator()
```
The method that is used to compare html code is 
```python
HTMLComparator.compare(html1, html2, quick_compare = True, compare_type = "all")
```

```html1, html2``` are the two html to be compared. If they are both strings, it will treat them as two html strings. If they are both ```io.IOBase``` objects, then the program will treat them as two opened files. Otherwise the program will raise a ```TypeError```.

```quick_compare``` argument is used to specify whether the user want the method to simply return boolean or to return a detailed information of the differences. If it is set to True, then the method will return False as soon as it encountered the first difference, and return True otherwise. If it is set to False, then the two html are compared thoroughly, and the method will return a ```string``` to describe the differences. If there are no differences, it will return an empty string.
