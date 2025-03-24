import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
from arguments import argument_parser
arguments = argument_parser()
import logging
import os
logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",)
DB_NAME = os.getenv("DB_NAME")

def db_connect():
    # Connect to database
    try:
        connection = sqlite3.connect(DB_NAME)
        try:
            logger.info('Database connected')
            create_tables(connection)
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            print(f"Error creating tables: {e}")
            exit()
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def db_dump(connection):
    # Dump database to file
    try:
        with open("dump.sql", "w") as file:
            for line in connection.iterdump():
                file.write(f"{line}\n")
        print("Database dumped to file dump.sql")
        logger.info('Database dumped to file dump.sql')
    except Exception as e:
        logger.error(f"Error dumping database: {e}")
        print(f"Error dumping database: {e}")
        exit()

def create_tables(connection):
        cursor = connection.cursor()
        try:
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
                print("Table checked/created")
            connection.commit()
            logger.info('Table company checked/created')
        except Exception as e:
            logger.error(f"Error creating table company: {e}")
            print(f"Error creating table company: {e}")
            exit()
        try:
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
                print("Table stock_value checked/created")
                logger.info('Table stock_value checked/created')
        except Exception as e:
            logger.error(f"Error creating table stock_value: {e}")
            print(f"Error creating table stock_value: {e}")
            exit()

def save_company(company,connection):
    try:
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
    except Exception as e:
        logger.error(f"Error saving company: {e}")
        print(f"Error saving company: {e}")
        exit()
           
def save_stock_value(stock_value,connection):
    try:
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
    except Exception as e:
        logger.error(f"Error saving stock value: {e}")
        print(f"Error saving stock value: {e}")
        exit()

def db_delete(connection):
    try:
        while True:
            if input(f"Type 'yes' to delete all rows from all tables at {DB_NAME}. CTRL+C to abort: ") == "yes":
                cursor = connection.cursor()
                cursor.execute("DELETE FROM company")
                cursor.execute("DELETE FROM stock_value")
                connection.commit()
                print("Database deleted")
                logger.info('Database deleted')
                logger.warning('Database deleted')
                exit()
            else:
                print("Wrong input!!!")
    except Exception as e:
        logger.error(f"Error deleting database: {e}")
        print(f"Error deleting database: {e}")
        exit()

def db_file_delete(db_file):
    try:
        while True:
            if input(f"Type 'yes' to delete file {db_file}. CTRL+C to abort: ") == "yes":
                os.remove(db_file)
                print(f"File {db_file} deleted")
                logger.warning(f'File {db_file} deleted')
                exit()
            else:
                print("Wrong input!!!")
    except Exception as e:
        logger.error(f"Error deleting file {db_file}: {e}")
        print(f"Error deleting file dump.sql: {e}")
        exit()