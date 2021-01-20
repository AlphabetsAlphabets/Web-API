# Syncing SQLite and MySQL databases.
The purpose of this syncing is to be able to update the global catalogue of transactions done by each employee to the central database hosted in a server. To keep track of transactions that are completed, and to verify it's legitamacy, reduce costs. As it is an inherent side effect of syncing two databases.

# How it works
## Syncing databases with the API (Mono-directional)
For now as of 19/1/2021, Tuesday. A __GET__ request is made to the API (Ideally it should be a POST/PUT request), and the API will compare the difference in the two tables, find the differences and amend it.  

For example, consider the following:
1. In the local database 2 new entries has been added by salesperson 2:
```
DepartmentID = "1", "4"
DepartmentName = "Coreography", "Cinematography"
Salesperson = "2", "2"
```
And within the server database these are it's fields:
```
DepartmentID = "2", "3"
DepartmentName = "Finance", "Sales"
Salesperson = "1", "1"
```
2. When the API is called via the GET request. It will do a comparison, and see what's missing; The server side database does not have an entry for: `DepartmentID of 1, 2. DepartmentName of Coreography and Cinematography, and of Salesperson 2`  

3. What happens next is that the API will go through checks to see what new information has been entered, and do a cross check against the database running in the server. Then it will update the database with new information.

The updated database:
```
DepartmentID = "2", "3", "1", "4"
DepartmentName = "Finance", "Sales", "Coreography", "Cinematography"
Salesperson = "1", "1", "2", "2"
```
It should be noted that the order is sorted by whoever syncs first. And __not__ ordered numerically or alphabetically.

There will be a hidden element that is being tracked called `counter`. It ranges from a minimum score of 0 to 2. Where 0 represents transaction not confirmed, 1 represents synced to the database once. And 2 represents that payment has been received.
