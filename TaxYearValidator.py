import sqlite3

# consts
DB_NAME: str = "retirement.db"
EMPLOYEE_TXT: str = "Employee.txt"
PAY_TXT: str = "Pay.txt"
SOCIAL_SECURITY_MIN: str = "SocialSecurityMinimum.txt"

def get_connection() -> sqlite3.Connection:
    """Returns the connection to SQLite db"""
    return sqlite3.connect(DB_NAME)


def create_tables(db_cursor: sqlite3.Cursor) -> None:
    """ Creates tables if they don't exist."""
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employee (
            EmployeeID INTEGER PRIMARY KEY,
            Name TEXT
        )
    """)
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pay (
            EmployeeID INTEGER,
            Year INTEGER,
            Earnings REAL
        )
    """)
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS SocialSecurityMin (
            Year INTEGER PRIMARY KEY,
            Minimum REAL
        )
    """)


def read_file(file: str):
    """Yields rows from a file, skipping the header."""
    with open(file, "r") as f:
        next(f)
        for line in f:
            stripped: str = line.strip()
            if stripped:
                yield stripped.split(",")


def load_table(db_cursor: sqlite3.Cursor, table: str, file: str, insert_query: str, parse_row) -> None:
    """Insert rows into a table only if it's empty."""
    db_cursor.execute(f"SELECT COUNT(*) FROM {table}")
    if db_cursor.fetchone()[0] == 0:
        rows: list = []
        for row in read_file(file):
            rows.append(parse_row(row))
        db_cursor.executemany(insert_query, rows)
        print(f"{table} table data inserted")
    else:
        print(f"{table} table is already filled")


# helpers
def parse_employee(row: list) -> tuple:
    return int(row[0]), row[1]
def parse_pay(row: list) -> tuple:
    return int(row[0]), int(row[1]), float(row[2])
def parse_social_security_min(row: list) -> tuple:
    return int(row[0]), float(row[1])

def qualifies(earnings: float, minimum: float) -> str:
    if earnings >= minimum:
        return "Yes"
    else:
        return "No"


def load_data(db_cursor: sqlite3.Cursor) -> None:
    """loads all data from the three text files into their tables"""
    load_table(
        db_cursor, "Employee", EMPLOYEE_TXT,
        "INSERT INTO Employee (EmployeeID, Name) VALUES (?, ?)",
        parse_employee
    )
    load_table(
        db_cursor, "Pay", PAY_TXT,
        "INSERT INTO Pay (EmployeeID, Year, Earnings) VALUES (?, ?, ?)",
        parse_pay
    )
    load_table(
        db_cursor, "SocialSecurityMin", SOCIAL_SECURITY_MIN,
        "INSERT INTO SocialSecurityMin (Year, Minimum) VALUES (?, ?)",
        parse_social_security_min
    )


def join_tax_data(db_cursor: sqlite3.Cursor) -> list:
    """Joins Employee Pay and socialSecurityMin """
    db_cursor.execute("""
        SELECT e.Name, p.Year, p.Earnings, s.Minimum
        FROM Employee AS e
        JOIN Pay AS p ON e.EmployeeID = p.EmployeeID
        JOIN SocialSecurityMin AS s ON p.Year = s.Year
        ORDER BY e.Name, p.Year
    """)
    return db_cursor.fetchall()


def print_results(results: list) -> None:
    """Print each employees yearly earnings, minimum and whether they qualify """
    print(f"\n{'Employee Name':<20} {'Year':<8} {'Earnings':>12} {'Minimum':>12}  {'Include'}")
    for name, year, earnings, minimum in results:
        print(f"{name:<20} {year:<8} {earnings:>12,.2f} {minimum:>12,.2f}  {qualifies(earnings, minimum)}")

