#Name: Tyler Kirchner
#Assignment: SQL Python
#Reflection
    # I enjoy the SQL!
    # Struggled with time management!
    # DDL works with the tables whereas DML works with the data in the tables
    # joins Employee and Pay by the EmployeeID column then joins the records to SocialSecurityMin by the Year column
    # Using SQLite in python and using SQL statements in python!

from TaxYearValidator import (get_connection,
                              create_tables,
                              load_data,
                              join_tax_data,
                              print_results)


def main() -> None:
    db_connection = get_connection()
    db_cursor = db_connection.cursor()

    create_tables(db_cursor)
    load_data(db_cursor)
    db_connection.commit()

    results = join_tax_data(db_cursor)
    print_results(results)

    db_connection.close()


if __name__ == "__main__":
    main()