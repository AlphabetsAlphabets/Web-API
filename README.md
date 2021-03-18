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


# Sugestions
- Instead of creating a new table for api keys add a new column in the tsc_office.tap table, called api key.
