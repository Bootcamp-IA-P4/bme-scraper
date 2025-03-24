# BME Scraper 📊
Author: Fernando García Catalán ✍️

Github: [https://github.com/fergarcat](https://github.com/fergarcat) 🌐

Scrum Project: [https://github.com/users/fergarcat/projects/2](https://github.com/users/fergarcat/projects/2) 📋

## Overview 📖

BME Scraper is a tool designed to scrape data from the BME (Bolsa y Mercados Españoles Stock Exchange) website.  
It automates the process of extracting relevant financial data for analysis or reporting purposes.  
This is my second project during the AI Bootcamp at [https://github.com/Factoria-F5-dev/](https://github.com/Factoria-F5-dev/) 🎓

## Features ✨

- Scrape companies and stock data from the BME website (https://www.bolsasymercados.es/). 💻
- Save data to local sqlite database. 💾
- Configurable scraping options. ⚙️
- Dump and deletion options for the database. 🗑️
- Logging information to `myapp.log`. 📝
- Verbose output option. 🔍

## Requirements 📦

As described in `requirements.txt` file.

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/fergarcat/bme-scraper
   ```
2. Navigate to the project directory:
   ```bash
   cd bme-scraper
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv # For Windows
   python3 -m venv .venv # For MacOS/Linux
   ```
4. Activate the virtual environment:
   ```bash
   .venv/Scripts/activate # For Windows
   source venv/bin/activate # For MacOS/Linux
   ```
5. Install dependencies:
   ```bash
   uv pip install -r requirements.txt # For Windows
   pip3 install -r requirements.txt # For MacOS/Linux
   ```
6. Rename file in the project directory `.env.example` to `.env` and set database path and default waiting time in the file:
   ```bash
   rename .env.example .env
   ```
7. Run the scraper:
   ```bash
   python main.py --help
   ```

## Usage 🚦

### Argument Groups
Arguments are divided into two groups: `--scrape` and `--database`, as well as general options.

### General Options (Optional and non exclusive)
--help      Show options
--version   Shows program version
--verbose   Shows detailed information in time of execution
--wait      Set random wait time, in secods, from 1 to input value. Default 5

### Scrape arguments (Not available if database argument used)
--scrape       Starts the execution of the scrape
--all          Set all scrapes available
--companies    Set company info as scope of the scrape
--stock_values Set current stock values as scope of the scrape

### Database arguments (Not available if scrape arguments used)
--delete_file  Delete sqlite db file
--delete_db    Delete all rows from all tables. Keeps file and table structure.
--dump         Dumps db structure and data to dump.sql file

1. Check the available options:
   ```bash
   python main.py --help
   ```
2. Run the scraper with desired options:
   ```bash
   python main.py --scrape --all --wait 5 --verbose # Scrape all companies and current stock values with a 5-second delay between requests. Shows verbose output.
   ```
3. Dump the database to a SQL file:
   ```bash
   python main.py --database --dump # Dump the database to dump.sql file.
   ```
4. Delete the database:
   ```bash
   python main.py --database --delete_file # Delete the database file.
   python main.py --database --delete_db # Delete all the data, but keep the database file and table structure.
   ```
## Docker 🐳
Dockerfile and docker-compose.yml files are included in the project for containerization.
Cronjob is set to run the scraper every day from Monday to Friday between 8:00-20:00.

1. Build the Docker image:
   ```bash
   docker-compose up --build
   ```
2. Run the Docker container:
   ```bash
      docker ps # Check the container ID
   docker exec -it <container_id> bash # Access the container
   ```
3. Check the logs:
   ```bash
   cat myapp.log
   ```
4. Connect to database:
   ```bash
   sqlite3 bme.db
   ```
5. Select data:
   ```bash
   SELECT * FROM companies;
   SELECT * FROM stock_values;
   ```
## Contributing 🤝

Contributions are welcome! Please fork the repository and submit a pull request.

## License 📜

This project is licensed under the MIT License. See the `LICENSE` file for details.