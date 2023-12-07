import requests
import os

def get_exchange_rates(api_key):
    """
    Fetches real-time exchange rates using the provided API key.

    :param api_key: API key for the exchange rate service
    :return: Dictionary of currency conversion rates
    """
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)
    data = response.json()
    return data['conversion_rates']

def convert_currency(amount, from_currency, to_currency, rates):
    """
    Converts a currency amount from one currency to another.

    :param amount: The amount of currency to convert
    :param from_currency: The currency code to convert from
    :param to_currency: The currency code to convert to
    :param rates: Dictionary of exchange rates
    :return: Converted amount in target currency
    """
    # Convert amount to USD first
    usd_amount = amount / rates[from_currency]
    # Then convert from USD to the target currency
    return usd_amount * rates[to_currency]

def main():
    # Get API key from environment variable
    api_key = os.getenv('EXCHANGE_API_KEY')
    if not api_key:
        print("API key not found. Please set the EXCHANGE_API_KEY environment variable.")
        return

    exchange_rates = get_exchange_rates(api_key)

    if exchange_rates:
        # User input
        try:
            amount = float(input("Enter the amount to convert: "))
            from_currency = input("Enter the currency code you are converting from (EUR, USD, CNY, RUB, NGN): ").upper()
            to_currency = input("Enter the currency code you are converting to (EUR, USD, CNY, RUB, NGN): ").upper()

            # Perform conversion and display result
            converted_amount = convert_currency(amount, from_currency, to_currency, exchange_rates)
            print(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
        except KeyError:
            print("Unsupported currency code.")
        except ValueError:
            print("Invalid amount entered. Please enter a numeric value.")
    else:
        print("Unable to fetch exchange rates.")

if __name__ == "__main__":
    main()
