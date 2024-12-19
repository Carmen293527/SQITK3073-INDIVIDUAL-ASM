# Stock Selection Tool

This repository contains the source code for a stock selection tool developed in Python.

**Features:**

* User registration and authentication.
* Stock data retrieval using `yfinance`.
* Customizable stock screening based on fundamental and technical criteria.
* Stock analysis including key financial metrics, technical indicators, and performance analysis.
* Data visualization and reporting capabilities.

### functions.py
Create a file named functions.py

**Installation:**
   ```bash
   import yfinance as yf
   import pandas as pd
   import csv
   import hashlib
   import os
   from datetime import datetime
```
**Write function for register user**
   ```bash
def register_user(email, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, hashed_password])
```

**Write function for authenticate user**
   ```bash
def authenticate_user(email, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email and row[1] == hashed_password:
                return True
    return False
```

**Write function for get closing prices**
   ```bash
def get_closing_prices(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data['Close']
```

**Write function for analyze closing prices**
This function calculates the average price, percentage change, highest and lowert closing price
   ```bash
def analyze_closing_prices(closing_prices):
    average_price = closing_prices.mean()
    percentage_change = ((closing_prices.iloc[-1] - closing_prices.iloc[0]) / closing_prices.iloc[0]) * 100
    highest_price = closing_prices.max()
    lowest_price = closing_prices.min()
    return average_price, percentage_change, highest_price, lowest_price
```

**Write function for save data to csv file**
   ```bash
def save_to_csv(email, ticker, start_date, end_date, average_price, percentage_change, highest_price, lowest_price):
    filename = f'{email}_stock_analysis.csv'  # Use a simple filename based on email

    # Check if the file exists and is empty (new analysis for the user)
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        # Write header if file is new
        with open(filename, 'w', newline='') as file:
            file.write("Ticker, Start Date, End Date, Average Price, Percentage Change, Highest Price, Lowest Price\n")

    # Append data to the existing file
    with open(filename, 'a', newline='') as file:
        file.write(f"{ticker}, {start_date}, {end_date}, {average_price.values[0]:.2f}, {percentage_change.values[0]:.2f}%, {highest_price.values[0]:.2f}, {lowest_price.values[0]:.2f}\n")

    print("Analysis appended to your CSV file.") 
```

**Write function for read data from csv file**
This function calculates the average price, percentage change, highest and lowert closing price
   ```bash
def read_from_csv(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            # Skip the header row
            next(reader) 
            for row in reader:
                print(f"Ticker: {row[0]}")
                print(f"Start Date: {row[1]}")
                print(f"End Date: {row[2]}")
                print(f"Average Price: {row[3]}")
                print(f"Percentage Change: {row[4]}")
                print(f"Highest Price: {row[5]}")
                print(f"Lowest Price: {row[6]}")
                print("-" * 20) 
    else:
        print(f"File {filename} not found.")
```

### main.py
Create a new file named: main.py

**Write code to prompt users input, and call all the functions from main.py**
   ```bash

from functions import register_user, authenticate_user, get_closing_prices, analyze_closing_prices, save_to_csv, read_from_csv

def main():
    while True:
        print("=====Welcome to Stock Selection Tool=====")
        choice = input("Enter (r)egister, (l)ogin, (v)iew data, or (e) to exit: ").lower()

        if choice == 'r':
            email = input("Please enter your email: ")
            if "@" not in email:
                print("Invalid email. Please enter a valid email address.")

            password = input("Please enter your password: ")
            confirm_password = input("Please confirm password again: ")

            if password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue

            register_user(email, password)
            print("Congratulations! Registration successful!")
        elif choice == 'l':
            email = input("Please enter your email: ")
            if "@" not in email:
                print("Invalid email. Please enter a valid email address.")
                
            password = input("Please enter your password: ")

            if authenticate_user(email, password):
                print("Authentication successful!")

                # Fetch AAPL data for December 2023
                ticker = input("Please enter the stock ticker (e.g., 1155.KL): ")
                start_date = input("Please enter the start date (YYYY-MM-DD): ")
                end_date = input("Please enter the end date (YYYY-MM-DD): ")

                closing_prices = get_closing_prices(ticker, start_date, end_date)

                average_price, percentage_change, highest_price, lowest_price = analyze_closing_prices(closing_prices)
                save_to_csv(email, ticker, start_date, end_date, average_price, percentage_change, highest_price, lowest_price)
                print("Analysis saved to your CSV file.")
            else:
                print("Authentication failed. Please check your email and password.")
        elif choice == 'v':
            email = input("Please enter your email: ")
            filename = f'{email}_stock_analysis.csv'  # Use the simple filename
            read_from_csv(filename) 
        elif choice == 'e':
            print("Exiting the program.")
            break  # Exit the while loop
        else:
                print("No analysis files found for this user.")
        
    else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
```
