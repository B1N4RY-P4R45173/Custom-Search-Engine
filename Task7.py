import os
import sys
from googleapiclient.discovery import build
from getpass import getpass
from cryptography.fernet import Fernet

def get_api_key(key_file="secret.key", api_key_file="api_key.encrypted"):
    
    def write_key(file_path="secret.key"):
        key = Fernet.generate_key()
        with open(file_path, "wb") as key_file:
            key_file.write(key)

    def load_key(file_path="secret.key"):
        return open(file_path, "rb").read()

    def encrypt_message(message, key):
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(encrypted_message, key):
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode()
        return decrypted_message

    if not os.path.exists(key_file):
        write_key(key_file)
    
    key = load_key(key_file)

    if os.path.exists(api_key_file):
        with open(api_key_file, "rb") as file:
            encrypted_api_key = file.read().strip()
            try:
                api_key = decrypt_message(encrypted_api_key, key)
                if api_key:
                    return api_key
            except Exception as e:
                print(f"An error occurred while decrypting the API key: {e}")

    api_key = getpass("Please enter your API key: ")
    encrypted_api_key = encrypt_message(api_key, key)
    with open(api_key_file, "wb") as file:
        file.write(encrypted_api_key)
    
    return api_key

def search_cse(api_key, search_engine_id, search_term):
    try:
        service = build("customsearch", "v1", developerKey=api_key)

        request = service.cse().list(
            q=search_term, cx=search_engine_id
        )

        response = request.execute()

        if 'items' in response:
            return response['items']
        else:
            print("No results found.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    API_KEY = get_api_key()
    SEARCH_ENGINE_ID = "762ebd0d12e5c4364"
    SEARCH_TERM = input("Please enter the word you want to search for: ")

    results = search_cse(API_KEY, SEARCH_ENGINE_ID, SEARCH_TERM)

    if results:
        print(f"Search results for '{SEARCH_TERM}':")
        for item in results:
            print(f"- Title: {item['title']}")
            print(f"  Snippet: {item['snippet']}")
            print(f"  Link: {item['link']}")
            print("---")

if __name__ == "__main__":
    main()
