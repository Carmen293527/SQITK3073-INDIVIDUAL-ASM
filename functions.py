import yfinance as yf
import pandas as pd
import csv
import hashlib
import os
from datetime import datetime

def register_user(email, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, hashed_password])

def authenticate_user(email, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email and row[1] == hashed_password:
                return True
    return False

def get_closing_prices(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data['Close']

def analyze_closing_prices(closing_prices):
    average_price = closing_prices.mean()
    percentage_change = ((closing_prices.iloc[-1] - closing_prices.iloc[0]) / closing_prices.iloc[0]) * 100
    highest_price = closing_prices.max()
    lowest_price = closing_prices.min()
    return average_price, percentage_change, highest_price, lowest_price

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