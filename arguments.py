import argparse
import os
from dotenv import load_dotenv
load_dotenv()
wait_time = os.getenv("WAIT_TIME")
browser_display = os.getenv("BROWSER_DISPLAY")

def argument_parser():
    parser = argparse.ArgumentParser(description='Scrape proyect for BME stock market website.\n\nYou may get all data from scratch or select the scope of the scrape.')
    parser.add_argument('-V', '--verbose', help="Show detailed output for each scrape.", action='store_true',default=False)
    parser.add_argument('-w', '--wait_time', help="Time to wait between requests.", type=int, default=wait_time)
    parser.add_argument('-b', '--browser', help="Show driver browser.", type=bool, default=browser_display)
    #Main group exclusive 
    main_option = parser.add_mutually_exclusive_group(required=True)
    main_option.add_argument('-scr','--scrape', help="Scrape data from the website.", action='store_true',default=False)
    main_option.add_argument('-db','--database', help="Manage db options.", action='store_true',default=False)
    #DB group exclusive
    database = parser.add_mutually_exclusive_group(required=False)
    database.add_argument('-du', '--dump', help="Dump database to file.", action='store_true',default=False)
    database.add_argument('-delf', '--delete_file', help="DELETE database file.", action='store_true',default=False)
    database.add_argument('-delbd', '--delete_db', help="Delete all rows from all tables.", action='store_true',default=False)
    #Scrape group exclusive
    scrape_group = parser.add_mutually_exclusive_group(required=False)
    scrape_group.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    scrape_group.add_argument('-a','--all', action='store_true', help='Scrape all data')
    scrape_group.add_argument('-c','--companies', action='store_true', help='Scrape companies')
    scrape_group.add_argument('-s','--stock_values', action='store_true', help='Scrape stock values')
    return(parser.parse_args())

def validate_arguments(arguments):
    if not arguments.scrape and arguments.browser:
        print("Browser option only available in scrape mode. Use -h for help")
        exit()
    if arguments.scrape and not arguments.all and not arguments.companies and not arguments.stock_values:
        print("No scope selected for scrape. Use -h for help")
        exit()
    if arguments.database and not arguments.dump and not arguments.delete_db and not arguments.delete_file:
        print("No action selected for database. Use -h for help")
        exit()
    return