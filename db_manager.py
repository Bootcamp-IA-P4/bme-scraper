import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
from arguments import argument_parser
arguments = argument_parser()

def db_connect():
    # Connect to database
    try:
        connection = sqlite3.connect(os.getenv("DB_NAME"))
        try:
            create_tables(connection)
        except Exception as e:
            print(f"Error creating tables: {e}")
            return None
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
def create_tables(connection):
        cursor = connection.cursor()
        # Create table company if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name varchar(50),
                isin char(12),
                ticker varchar(4),
                nominal float,
                market varchar(50),
                listed_capital float,
                address varchar(50)
            )
        """)
        if arguments.verbose:
            print("Table company created")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_value (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isin char(12),
                last float,
                diff float,
                max float,
                min float,
                volume float,
                turnover float,
                updated datetime
            )
        """)
        connection.commit()
        if arguments.verbose:
            print("Table stock_value created")
def save_company(company,connection):
    cursor = connection.cursor()
    # Check if company already exists, by ISIN
    cursor.execute("SELECT COUNT(*) FROM company WHERE isin = ?", (company.isin,))
    result = cursor.fetchone()[0]
    if result > 0 and arguments.verbose:
        print(f"Company {company.name} already exists in database")
        return
    else: # Insert data
        cursor.execute("""
            INSERT INTO company (name, isin, ticker, nominal, market, listed_capital, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (company.name, company.isin, company.ticker, company.nominal, company.market, company.listed_capital, company.address))
        connection.commit()
        if arguments.verbose:
            print(f"Company {company.name} saved in database")

def save_stock_value(stock_value,connection):
    cursor = connection.cursor()
    # Check if stock value already exists, by ISIN and updated date
    cursor.execute("SELECT COUNT(*) FROM stock_value WHERE isin = ? AND updated = ?", (stock_value.isin, stock_value.updated))
    result = cursor.fetchone()[0]
    if result > 0 and arguments.verbose:
        print(f"Stock value {stock_value.isin} already exists in database")
        return
    else: # Insert data
        cursor.execute("""
            INSERT INTO stock_value (isin, last, diff, max, min, volume, turnover, updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (stock_value.isin, stock_value.last, stock_value.diff, stock_value.max, stock_value.min, stock_value.volume, stock_value.turnover, stock_value.updated))
        connection.commit()
        if arguments.verbose:
            print(f"Stock value {stock_value.isin} saved in database")
