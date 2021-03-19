# Important! Read this before using or modifying 
Make sure to update the variables `self.schema` and `self.table` in **all** endpoints it appears in (all endpoints are located in env-api/endpoints/). It will usually appear in the `__init__` function of all endpoints. This is what it will look like int the `__init__` function.

```python3
class endpoint:
    def __init__(self):
        # code ...
        try: 
            self.conn, self.cursor = Database.connect(.., ..)
            self.schema = "schema"
            self.table = "table"
        except Exception:
            self.conn, self.cursor = Database.connect(.., ..)
            self.schema = "schema"
            self.table = "table"
```

change the `__init__` function to:
```python3
def __init__(self):
    # code ...
    self.conn, self.cursor = Database.connect(.., ..)
    self.schema = "schema"
    self.table = "table"
```

Of course set `self.schema` and `self.table` to valid names. **Do not** alter/modify any other code within the `__init__` method unless it's within a try/except block

---

# General information 

#### Table of contents
Topic | description |
--- | ---- |
|[Finding where anything is defined](https://github.com/YJH16120/Web-API#finding-where-anything-is-defined) | Useful for when you want to know the inner workings of a function |
| [Creating a new endpoint](https://github.com/YJH16120/Web-API#creating-a-new-endpoint) | A guide on how to create a new endpoint |
| [Verifying a user's api key](https://github.com/YJH16120/Web-API#verifying-a-users-api-key) | How to verify a user's api key |
| [Writing documentaiton](https://github.com/YJH16120/Web-API#writing-documentation) | How to write documentation that complies to PEP8 standards |
| [Type hinting](https://github.com/YJH16120/Web-API#type-hinting) | How to write type hints and return types |



### Finding where anything is defined.
- All endpoints are located in the env-api/endpoints/ directory. 
- Functions related to connecting to a database, encryption, and api key verification is located in the env-api/QA/ directory.

If your IDE or text editor supports go-to definition, I suggest you go-to defininition instead of manually locating where each file is. Especially if you're
new to the project

### Creating a new endpoint
Create a new endpoint in the env-api/endpoints/ directory. And lay it out in the following structure
```python3
from flask_restfull import Resource

class Example(Resource):
    def __init__(self):
        """Handle initilization"""
        self.conn, self.cursor = Database.connect("host", "username", "password", "schema")

    def <request>(self, arg1, arg2):
        """process the request."""
        pass
```
- `self.conn` is the connection to the MySql database
- `self.cursor` is the cursor to the MySql database
- `<request>` is the type of request. Change `<request>` to GET if the endpoint is going to process a GET request. For a template refer to example.py (docs/example.py)

### Verifying a user's api key
Validating a user's api key. In order for a user to get their api key, they must first go through the login endpoint (env-api/endpoints/login.py) and then the key must be passed
into the `verifyKey()` method provided in QA/key.py.
```python3
Key.verifyKey("username", "abc123") 
```

### Writing documentation
Documentation is important. Make sure to include it in the following format. When creating classes it's methods.
```python3
from typing import Union

class Example:
    """This class provides functions to add, and divide

    # Functions
    - add (private)
    - subtract 
    """

    def __add(self, number1: Union[int, float], number2: Union[int, float]) -> Union[int, float]:
        """Adds two numbers together

        ---

        # Parameters
        
        ### number1
        the first number

        ### number2
        the second number
        """

        return number1 + number2

    def divide(self, number1: int, number 2: int) -> Union[int, str]:
        """Performs division

        ---

        # Parameters
        
        ### number1
        the first number

        ### number2
        the second number

        ---

        # Exceptions
        - ZeroDivisionError: This occurs when you divide by 0
        """
        try:
            return number1 / number2
        except ZeroDivisionError:
            return "cannot divide by zero"
```
Make sure to include a brief summary about what the class does, and list down all their class functions. And always make sure to include a brief summary about the class and function first.

Then in each function, give a brief description, followed by a brief explanation for each parameter, and if the function has a chance to throw an exception include an exception section as well. And if the function is private make sure to include it in parenthesis.

Separate each section with three `-`'s 

And make sure to include type hinting. Refer to the python documentation about the [typing](https://docs.python.org/3/library/typing.html) module

### Type hinting
Type hinting is important because it tells the user what types the function parameters expect, and what the return type is.
```python3
def foo(a: str, b: int) -> str
    return str + str(int)
```
This tells the user that `foo` has two parameters `a`, and `b`. And that `a` accepts a string, `b` accepts an interger and the function returns a string.

for advanced type hinting, such as a parameter accepting either a boolean or an interger the [typing](https://docs.python.org/3/library/typing.html) module is required.
```python
from typing import Union
def bar(a: Union[int, bool]) -> bool:
    return bool(a)
```


# Sugestions
- Instead of creating a new table for api keys add a new column in the tsc_office.tap table, called api key. More details in (QA/key.py)
- Scrap the generic insert endpoint (env-api/endpoints/insertGeneric.py)
