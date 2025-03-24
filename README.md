# BME Scraper 🚀
Author: Fernando García Catalán ✍️

Github: [https://github.com/fergarcat](https://github.com/fergarcat) 🌐

Scrum Project: [https://github.com/users/fergarcat/projects/2](https://github.com/users/fergarcat/projects/2) 📋

## Overview 📖

BME Scraper is a tool designed to scrape data from the BME (Bolsa y Mercados Españoles Stock Exchange) website.  
It automates the process of extracting relevant financial data for analysis or reporting purposes.  
This is my second project during the AI Bootcamp at [https://github.com/Factoria-F5-dev/](https://github.com/Factoria-F5-dev/) 🎓

## Features ✨

- Scrape companies and stock data from the BME website (https://www.bolsasymercados.es/). 📊
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
   git clone https://github.com/your-username/bme-scraper.git
   ```
2. Navigate to the project directory:
   ```bash
   cd bme-scraper
   ```
3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
4. Rename file in the project directory `.env.example` to `.env` and set database path and default waiting time in the file:
   ```bash
   rename .env.example .env
   ```
5. Activate the virtual environment:
   ```bash
   .venv/Scripts/activate # For Windows
   source venv/bin/activate # For MacOS/Linux
   ```

## Usage 🚦

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

## Contributing 🤝

Contributions are welcome! Please fork the repository and submit a pull request.

## License 📜

This project is licensed under the MIT License. See the `LICENSE` file for details.