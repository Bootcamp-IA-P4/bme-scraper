import argparse
def argument_parser():
    # Crear un grupo de argumentos mutuamente excluyentes
    parser = argparse.ArgumentParser(description='Scrape data from the spanish stock market website')
    parser.add_argument('-V', '--verbose', help="Show detail output", action='store_true',default=False)
    #Scrape group
    scrape_group = parser.add_mutually_exclusive_group(required=True)
    scrape_group.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    scrape_group.add_argument('-a','--all', action='store_true', help='Scrape all data')
    scrape_group.add_argument('-c','--companies', action='store_true', help='Scrape companies')
    scrape_group.add_argument('-s','--stock_values', action='store_true', help='Scrape stock values')
    return(parser.parse_args())