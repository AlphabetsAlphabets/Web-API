# Table of contents
Topic | description |
--- | ---- |
| [Setup and foreword](https://github.com/YJH16120/Web-API#read-this-first) | Important information |
| [File structure](https://github.com/YJH16120/Web-API#familiarize-yourself-with-the-directory-structure) | Directory structure, and explanation on which file goes where. |
| [How to setup development environment](https://github.com/YJH16120/Web-API#configuring-the-development-environment) | Tells you how to setup your development environment. |
| [Foreword](https://github.com/YJH16120/Web-API#foreword) | Information on how to proceed.
| [What library this project is dependant on.](https://github.com/YJH16120/Web-API#Based-on) | Explains which libray the project is depedant on.
| [Finding where anything is defined](https://github.com/YJH16120/Web-API#finding-where-anything-is-defined) | Useful for when you want to know the inner workings of a function |
| [Creating a new endpoint](https://github.com/YJH16120/Web-API#creating-a-new-endpoint) | A guide on how to create a new endpoint |
| [Verifying a user's api key](https://github.com/YJH16120/Web-API#verifying-a-users-api-key) | How to verify a user's api key |
| [Writing documentaiton](https://github.com/YJH16120/Web-API#writing-documentation) | How to write documentation that complies to PEP8 standards |
| [Type hinting](https://github.com/YJH16120/Web-API#type-hinting) | How to write type hints and return types |

---
## Familiarize yourself with the directory structure
```
Web API
|   .gitignore
|   README.md
|   requirements.txt
|   
+---docs
|       example.py
|       
+---env-api
|   |   pyvenv.cfg
|   |   
|   +---endpoints
|   |   |   insertGeneric.py
|   |   |   location.py
|   |   |   login.py
|   |   |   spec.py
|   |   |   sync.py
|   |   |   tap.py
|   |   |   tinvoicehistory.py
|   |   |   update.py
|   |   |   upload.py
|   |   |   __init__.py
|   |   |   
|   |   \---databases
|   |           insertDb.db
|   |           syncDb.db
|   |           
|   \---QA
|           database.py
|           encrypt.py
|           key.py
|           __init__.py
|           
\---src
        main.py
```        
## Root of the project
Web API is the root of the project, and from this point onwards whenever I say "at the root of the project" or something similar.
Always assume that you have to go to Web API, unless specified otherwise.

## docs
Docs contain documentation. Code examples can be found there.

## env-api
This is where the `endpoints` directory is, and where *all* endpoints reside. It's also where `QA` is found, quality of life files/modules are
kept there.

## env-api/databases
This is where the sqlite3 databases are kept. These are used to simulate, a client's activity.

## src
This folder contains the main source file. Where `main.py` is the main source file.

---
## Configuring the development environment
1. Have python 3.9 and above installed.
2. make sure pip is working, to test run `pip --version` in a terminal. If it shows you the version number proceed, if not then fix it.
3. Have the [git](https://git-scm.com/downloads) CLI installed.
4. Run the following command:  `git clone 'https://github.com/YJH16120/Web-API'`  

From this point onwards make sure you perform all commands in the root of the project. Unless specified otherwise  

5. Cut the contents from the env-api directory.
6. Run the following commands to create a virtual environment (make sure you're in the root of Web-API when running these commands):
    - run `pip install venv`
    - `py -m venv env-api`
    - For powershell: `env-api\Scripts\active`, for CMD: `activate`
    - `pip install -r requirements.txt`, this will install the appropriate dependancies.

It is worth noting that if you run this python code through visual studio code (VSC) by clicking the [play button](https://i.postimg.cc/D0ykRP8k/image.png)
provided by the downloadable python extension, **most** endpoints that require the use of paths will fail. So you **must** always run the main source file
from a terminal instead. That is because each source file sees itself as the centre of the project, and everything else as relative to it, whereas if you
run it in VSC the root will be the centre of the project instead of each source file being the centre. Which is why it will most likely fail.

7. Check if you've setup everything correctly. Go to the root of Web-API, then run `py src/main.py`
If there are no errors and everything is fine, it means that you've successfully configured your environment to develop the API.

---
## Foreword
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

## Based on
This project is based on [flask restful](https://flask-restful.readthedocs.io/en/latest/index.html). Without this package it would not be possible to develop the api the way it is.

---

## Finding where anything is defined.
- All endpoints are located in the env-api/endpoints/ directory. 
- Functions related to connecting to a database, encryption, and api key verification is located in the env-api/QA/ directory.

If your IDE or text editor supports go-to definition, I suggest you go-to defininition instead of manually locating where each file is. Especially if you're
new to the project

## Creating a new endpoint
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

---
## Setting up a url resource
If for example, we want to make a resource that uses logic from the `Example` class, we need to create a url resource. Assume the file that the `Example` class is from is called `example.py`

I'm going to assume you are some what familiar with [Flask](https://flask.palletsprojects.com/en/1.1.x/), as least up to creating a Flask app.

From a main source file do the following:
```python3
from flask_restful import Api
from example import Example

app = Flask(__name__)
api = Api(app)

api.add_resource(Example, "/example/<string:arg1>/<string:arg2>")
```
When you run main source file with `py main.py` you can go to the link printed onto the terminal and append it with "example/1/2". In order to access the endpoint.

Keep in mind that in `/example/<string:arg1>/<string:arg2>` (I will call this string resource from this point onwards), the number of arguments in resource must match the number of arguments as specified in the class.

In `Example` the method `<request>` has two parameters `arg1`, and `arg2`. As you can see resource reflects that. If `<request>` instead has `a`, and `b`. Resource would be changed to `/example/<string:b>/<string:a>`.

The parameters in resource and the method **must** match. Or an exception will be thrown.

---
## Accepting data from multiple locations
When making a HTTP request information can be sent in through the headers or various other locations.

To do so we must modify the `Example` class' `__init__` method. And import another class.
```python3
from flask_restful import reqparse

def __init__(self):
    """Handle initilization"""
    self.conn, self.cursor = Database.connect("host", "username", "password", "schema")
    parser = reqparse.RequestParser()
    parser.add_argument("header1", type=str, location="headers")
```
This modification will make it so that you can get information from the header named "header1"

For a full list of locations, refer to the [flask restful](https://flask-restful.readthedocs.io/en/latest/reqparse.html?highlight=headers) documentation

---
## Verifying a user's api key
Validating a user's api key. In order for a user to get their api key, they must first go through the login endpoint (env-api/endpoints/login.py) and then the key must be passed
into the `verifyKey()` method provided in QA/key.py.
```python3
Key.verifyKey("username", "abc123") 
```

## Writing documentation
Documentation is important. Make sure to include it in the following format. When creating classes, and it's methods.
```python3
from typing import Union

class Example:
    """This class provides functions to add, and divide

    # Functions
    ### public
    - subtract 

    ### private
    - add 
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

        ---

        # Example(s)
        ```python3
        num1 = 2
        num2 = 2
        result = Example().divide(num1, num2)
        print(result) # 1
        """
        try:
            return number1 / number2
        except ZeroDivisionError:
            return "cannot divide by zero"
```
Make sure to include a brief summary about what the class does, and list down all their class functions. And always make sure to include a brief summary about the class and function first.

Then in each function, give a brief description, followed by a brief explanation for each parameter, and if the function has a chance to throw an exception include an exception section as well. Optionally an examples section, to illustrate what the function does in greater detail. Or to act as supporting evidence.

Separate each section with three `-`'s 

And make sure to include type hinting. Refer to the python documentation about the [typing](https://docs.python.org/3/library/typing.html) module

## Type hinting
Type hinting is important because it tells the user what types the function parameters expect, and what the return type is.
```python3
def foo(a: str, b: int) -> str
    return str + str(int)
```
This tells the user that `foo` has two parameters `a`, and `b`. And that `a` accepts a string, `b` accepts an interger and the function returns a string.
And if no return type is specified it is assumed that the function does not return anything.

for advanced type hinting, such as a parameter accepting either a boolean or an interger the [typing](https://docs.python.org/3/library/typing.html) module is required.
```python
from typing import Union
def bar(a: Union[int, bool]) -> bool:
    return bool(a)
```


# Sugestions
- Instead of creating a new table for api keys add a new column in the tsc_office.tap table, called api key. More details in (QA/key.py)
- Scrap the generic insert endpoint (env-api/endpoints/insertGeneric.py)
