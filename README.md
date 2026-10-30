# Tax Year Validator

A small Python program that uses SQLite to check, for each employee and year, whether their earnings reach the Social Security minimum for that year.

## What it does

- Creates three tables (`Employee`, `Pay`, `SocialSecurityMin`) in a SQLite database.
- Loads them from `Employee.txt`, `Pay.txt` and `SocialSecurityMinimum.txt`.
- Joins Employee to Pay on the employee ID, then joins the result to the minimums on the year.
- Prints each employee's name, year, earnings, the minimum and whether the earnings qualify (`Yes` or `No`).

## Run it

Needs Python 3.10 or newer, with no other packages (`sqlite3` is built in).

```
python main.py
```

The database file (`retirement.db`) is created when the program runs.

## Notes

This was a coursework project (SQL in Python). The data files are sample data.
