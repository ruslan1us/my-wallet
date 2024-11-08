# My Wallet

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Getting Started](#getting-started)
* [Access My Wallet](#access-my-wallet)

## General info
My Wallet is a finance management tool designed to help you take control of your expenses, income, and savings with ease. With My Wallet, you can track your financial transactions, analyze your spending patterns, and make informed decisions about your money.

## Features
### Expense Tracking:
Keep track of your expenses and categorize them for better analysis.
### Income Management:
Record your income sources and monitor your cash flow.
### Savings Monitoring:
Set savings goals and track your progress over time.
### Secure Authentication:
Protect your financial information with secure user authentication.

## Technologies
* Python 3.12
* FastAPI
* PostgreSQL
* SQLAlchemy 2.0
* Alembic
* uvicorn

## Getting Started
#### To get started with My Wallet, follow these steps:
### Clone the repository:
```
git clone https://github.com/ruslan1us/my-wallet.git
```
### Install dependencies:
```
pip install -r requirements.txt
```
### Set up the database:
* Ensure PostgreSQL is installed and running on your system.
* Create a new PostgreSQL database.
* Update the database connection settings in config.py to point to your PostgreSQL instance.
### Run Migrations:
```
alembic upgrade head
```
### Start the application:
```
uvicorn app.main:app --reload
```
## Access My Wallet:
Open your web browser and navigate to http://localhost:8000 to access the My Wallet application.

# Testing
This project includes a comprehensive suite of tests to ensure reliability and performance. The tests are written using pytest and cover critical functionality, including user authentication, data handling, and endpoint accessibility. Below is a guide to setting up and running these tests.
## Running Tests
To run all tests in the project, use the following command:
```
pytest
```
## Test Structure
The tests are organized across multiple files to provide modular coverage:
* Authentication Tests: These tests verify registration, login, and access token validity to ensure only authorized users can access certain endpoints.
* Data Handling Tests: This suite checks the database's ability to correctly create, read, update, and delete data. Dependencies such as authenticated users or pre-existing data are managed within individual test functions
  for isolation.

## Running Specific Tests
To run tests for a specific functionality or to debug a particular issue, you can target specific files or test functions. For example:
```
pytest tests/test_authentication.py  # Run authentication tests only
pytest -k "test_expenses_read"       # Run a specific test by name
```

### Contributing
Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request.
