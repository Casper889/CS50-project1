import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "RHUix4sDcDH9V9PfN3jqg", "isbns": "9781632168146"})
print(res.json())
