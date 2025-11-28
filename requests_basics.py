"""
Python Requests Library - Complete Tutorial
This file teaches you everything you need to know about the requests library
for HackerRank API problems.
"""

import requests
import json


# 1. BASIC GET REQUEST

def basic_get_request():
    """Simple GET request - most common in HackerRank"""
    url = "https://jsonplaceholder.typicode.com/posts/1"

    # Make the request
    response = requests.get(url)

    # Check if request was successful
    print(f"Status Code: {response.status_code}")  # 200 means success

    # Get JSON data
    data = response.json()  # Automatically parses JSON
    print(f"Data: {data}")

    return data


# 2. GET REQUEST WITH QUERY PARAMETERS

def get_with_parameters():
    """Using query parameters (like ?city=Seattle&page=1)"""
    url = "https://jsonplaceholder.typicode.com/posts"

    # Method 1: Build URL manually
    manual_url = "https://jsonplaceholder.typicode.com/posts?userId=1"
    response1 = requests.get(manual_url)

    # Method 2: Use params dictionary (RECOMMENDED)
    params = {
        'userId': 1,
        'id': 1
    }
    response2 = requests.get(url, params=params)

    # Both methods work the same
    print(f"Response: {response2.json()}")
    return response2.json()


# 3. HANDLING PAGINATION (Common in HackerRank)

def fetch_all_pages(base_url, city):
    """
    Many HackerRank problems require fetching multiple pages.
    The API usually tells you total_pages in the response.
    """
    all_data = []
    page = 1

    while True:
        # Build URL with parameters
        params = {
            'city': city,
            'page': page
        }

        response = requests.get(base_url, params=params)

        # Check for errors
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        json_data = response.json()

        # Typical HackerRank API structure
        current_page = json_data.get('page', 0)
        total_pages = json_data.get('total_pages', 0)
        data = json_data.get('data', [])

        # Add current page data to our collection
        all_data.extend(data)

        # Check if we've reached the last page
        if current_page >= total_pages:
            break

        page += 1

    return all_data


# 4. ERROR HANDLING (Important for production code)

def safe_api_call(url):
    """Always handle potential errors"""
    try:
        response = requests.get(url, timeout=10)  # 10 second timeout
        response.raise_for_status()  # Raises exception for 4xx/5xx status codes
        return response.json()

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to server")
        return None

    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return None

    except json.JSONDecodeError:
        print("Error: Response is not valid JSON")
        return None


# 5. COMMON DATA MANIPULATION PATTERNS

def data_manipulation_examples():
    """Common patterns you'll use after fetching data"""

    # Sample data structure (typical HackerRank format)
    restaurants = [
        {"name": "Pizza Place", "rating": 4.5, "price": 25, "cuisine": "Italian"},
        {"name": "Burger Joint", "rating": 3.8, "price": 15, "cuisine": "American"},
        {"name": "Sushi Bar", "rating": 4.8, "price": 45, "cuisine": "Japanese"},
        {"name": "Taco Stand", "rating": 4.2, "price": 12, "cuisine": "Mexican"},
    ]

    # Pattern 1: FILTERING (using list comprehension)
    high_rated = [r for r in restaurants if r['rating'] >= 4.0]
    print(f"High rated: {len(high_rated)} restaurants")

    # Pattern 2: FILTERING with multiple conditions
    affordable_and_good = [
        r for r in restaurants
        if r['rating'] >= 4.0 and r['price'] <= 30
    ]

    # Pattern 3: TRANSFORMING data (adding new fields)
    with_discount = [
        {**r, 'discounted_price': r['price'] * 0.8}  # 20% discount
        for r in restaurants
    ]

    # Pattern 4: SORTING
    sorted_by_price = sorted(restaurants, key=lambda x: x['price'])
    sorted_by_rating = sorted(restaurants, key=lambda x: x['rating'], reverse=True)

    # Pattern 5: SORTING by multiple criteria
    sorted_multi = sorted(
        restaurants,
        key=lambda x: (-x['rating'], x['price'])  # High rating first, then low price
    )

    # Pattern 6: FINDING min/max
    cheapest = min(restaurants, key=lambda x: x['price'])
    highest_rated = max(restaurants, key=lambda x: x['rating'])

    # Pattern 7: GROUPING (using dictionaries)
    by_cuisine = {}
    for r in restaurants:
        cuisine = r['cuisine']
        if cuisine not in by_cuisine:
            by_cuisine[cuisine] = []
        by_cuisine[cuisine].append(r)

    # Pattern 8: AGGREGATION
    total_restaurants = len(restaurants)
    average_price = sum(r['price'] for r in restaurants) / total_restaurants
    average_rating = sum(r['rating'] for r in restaurants) / total_restaurants

    return {
        'filtered': high_rated,
        'sorted': sorted_by_price,
        'cheapest': cheapest,
        'average_price': average_price
    }


# 6. WORKING WITH NESTED JSON

def handle_nested_json():
    """HackerRank APIs often return nested structures"""

    # Example nested response
    api_response = {
        "page": 1,
        "total_pages": 5,
        "data": [
            {
                "id": 1,
                "name": "Restaurant A",
                "location": {
                    "city": "Seattle",
                    "address": "123 Main St"
                },
                "menu": [
                    {"item": "Pizza", "price": 12},
                    {"item": "Pasta", "price": 15}
                ]
            }
        ]
    }

    # Accessing nested data
    first_restaurant = api_response['data'][0]
    city = first_restaurant['location']['city']
    first_menu_item = first_restaurant['menu'][0]['item']

    # Safe access with .get() to avoid KeyError
    rating = first_restaurant.get('rating', 0)  # Returns 0 if 'rating' doesn't exist

    # Flattening nested structures
    all_menu_items = []
    for restaurant in api_response['data']:
        for item in restaurant.get('menu', []):
            all_menu_items.append({
                'restaurant': restaurant['name'],
                'item': item['item'],
                'price': item['price']
            })

    return all_menu_items


# QUICK REFERENCE CHEAT SHEET

"""
COMMON REQUESTS PATTERNS:
------------------------

1. Basic GET:
   response = requests.get(url)
   data = response.json()

2. GET with parameters:
   response = requests.get(url, params={'key': 'value'})

3. Check status:
   if response.status_code == 200:
       # Success!

4. Common response methods:
   response.json()          # Parse JSON
   response.text            # Raw text
   response.status_code     # HTTP status (200, 404, etc.)
   response.headers         # Response headers

5. List comprehension filtering:
   filtered = [item for item in items if item['field'] > value]

6. Sorting:
   sorted(items, key=lambda x: x['field'])              # Ascending
   sorted(items, key=lambda x: x['field'], reverse=True) # Descending

7. Multiple sort criteria:
   sorted(items, key=lambda x: (x['field1'], -x['field2']))

8. Safe dictionary access:
   value = dict.get('key', default_value)

9. Transform and add fields:
   new_list = [{**item, 'new_field': calculation} for item in items]
"""


if __name__ == "__main__":
    print("Python Requests Tutorial")
    print("=" * 50)

    # Test basic functionality
    print("\n1. Basic GET Request:")
    basic_get_request()

    print("\n2. Request with Parameters:")
    get_with_parameters()

    print("\n3. Data Manipulation:")
    results = data_manipulation_examples()
    print(f"Cheapest restaurant: {results['cheapest']}")