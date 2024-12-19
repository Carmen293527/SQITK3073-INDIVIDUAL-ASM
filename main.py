
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