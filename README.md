# HTTPAccessLogParser

This solution defines the following entities:
* `IHTTPAccessLogParser`: an interface for the LogParser
* `HTTPAccessLogParserWithHeap`: a concrete implementation of the LogParser using MinHeap

Even though the problem asks for top 3, the solution supports retrieving the top K ip addresses and urls. This allows for extensions in case users want to retrieve more than 3. Also, an interface `IHTTPAccessLogParser` is declared to support dependency injection, in case we want to implement the LogParser in a different way instead of MinHeap. This solution allows getting top K elements across multiple log files.

## Usage
The `parse()` takes in a `Path` object from `pathlib` module which is OS agnostic. Thus, this code should be working on both Windows and Unix

Example usage of the library
```
from pathlib import Path
from parser import HTTPAccessLogParserWithHeap


parser = HTTPAccessLogParserWithHeap()
logDir = "/var/log/apache"
files = Path(logDir).glob("**/*.log")
for f in files:
  parser.parse(f)
```

## Implementation Discussion
There are a few different ways to implement top K elements problem
* Sorting
* Heap
* Self-balanced binary search tree like AVL or Red-black tree

The worst case time and space complexities for getting top K elements are summarized in the table below (with N = number of log lines)
|               | Sorting       | Heap          | Balanced BST
| ------------- | ------------- | ------------- | ------------- |
| Time          | O(NlogN + K)  | O(NlogK)      | O(logN)       |
| Space         | O(N)          | O(K)          | O(N)          |

With balanced BST, it offers the best performance for get. However, heap offers the best memory usage.

## Get Started
Note: This project was written with Python 3.11

You can install Python version manager `pyenv` following this [installation guide](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) and then install Python 3.11
```
pyenv install 3.11
pyenv global 3.11
```

Create and access a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
# Create git commit hooks
pre-commit install
```

Run unit tests
```
python3 -m unittest -v
```

Run the script
```
python3 main.py
```
