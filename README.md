# Python Requests Library - HackerRank Practice

Learn the `requests` library for API-based HackerRank problems with practical examples.

## Files

1. **requests_basics.py** - Complete tutorial covering:
   - Basic GET requests
   - Query parameters
   - Pagination
   - Error handling
   - Data manipulation patterns (filtering, sorting, transforming)
   - Working with nested JSON

2. **restaurant_recommendation.py** - Full solution to the HackerRank restaurant problem:
   - Fetch restaurant data with pagination
   - Apply business rules (discounts, delivery fees)
   - Filter by rating
   - Sort by final price
   - Demonstrates real-world problem structure

3. **quick_test.py** - Interactive testing script:
   - Explore API structure
   - Practice filtering and sorting
   - Test pagination
   - Includes a practice problem for you to solve

4. **requirements.txt** - Python dependencies

## Getting Started

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Examples

```bash
# 1. Start with the basics tutorial
python requests_basics.py

# 2. See the complete restaurant solution
python restaurant_recommendation.py

# 3. Experiment with the API yourself
python quick_test.py
```

## Key Concepts

### Making API Calls
```python
import requests

# Simple GET request
response = requests.get(url)
data = response.json()

# With parameters
params = {'city': 'Seattle', 'page': 1}
response = requests.get(url, params=params)
```

### Handling Pagination
```python
all_data = []
page = 1

while True:
    response = requests.get(url, params={'page': page})
    data = response.json()

    all_data.extend(data['data'])

    if data['page'] >= data['total_pages']:
        break

    page += 1
```

### Filtering Data
```python
# Filter with list comprehension
high_rated = [r for r in restaurants if r['rating'] >= 4.0]

# Multiple conditions
filtered = [
    r for r in restaurants
    if r['rating'] >= 4.0 and r['price'] < 30
]
```

### Sorting Data
```python
# Sort ascending
sorted_asc = sorted(items, key=lambda x: x['price'])

# Sort descending
sorted_desc = sorted(items, key=lambda x: x['price'], reverse=True)

# Multiple criteria
sorted_multi = sorted(
    items,
    key=lambda x: (-x['rating'], x['price'])  # High rating, then low price
)
```

### Transforming Data
```python
# Add calculated fields
with_discount = [
    {**item, 'final_price': item['price'] * 0.8}
    for item in items
]
```