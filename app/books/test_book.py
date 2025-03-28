import requests

url = "http://127.0.0.1:8080/book/add_book"
data = {
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "year": 1937
}



response = requests.post(url, json=data)
print(response.json())
