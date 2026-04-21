import os
import requests
from dotenv import load_dotenv

# Load variables from .env into the system environment
load_dotenv()


def search_books(book_name):
    # Retrieve the API key from the environment
    api_key = os.getenv("GBOOKS_API_KEY")

    if not api_key:
        print("Error: API Key not found. Check your .env file.")
        return

    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': book_name,
        'key': api_key,
        'maxResults': 5
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "items" in data:
            for item in data["items"]:
                v_info = item.get("volumeInfo", {})
                title = v_info.get("title", "No Title")

                # Accessing the cover image
                image_links = v_info.get("imageLinks", {})
                # We use .get() to avoid KeyErrors if the thumbnail is missing
                cover_url = image_links.get("thumbnail", "No cover image available")

                print(f"Title: {title}")
                print(f"Cover URL: {cover_url}")
                print("-" * 20)
        else:
            print("No books found.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


# Run the search
if __name__ == "__main__":
    search_query = "The Great Gatsby"
    search_books(search_query)