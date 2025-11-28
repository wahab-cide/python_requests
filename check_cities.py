import requests

url = "https://jsonmock.hackerrank.com/api/food_outlets"

# Fetch all data to see what cities exist and if any have cuisine data
params = {'page': 1}
response = requests.get(url, params=params)
data = response.json()

all_restaurants = []
for page in range(1, min(data.get('total_pages', 0) + 1, 5)):  # Check first 5 pages
    params = {'page': page}
    response = requests.get(url, params=params)
    all_restaurants.extend(response.json().get('data', []))

# Check cities
cities = set(r.get('city') for r in all_restaurants)
print(f"Cities found: {cities}")

# Check if any restaurant has cuisine data
with_cuisine = [r for r in all_restaurants if r.get('cuisine') is not None]
print(f"\nRestaurants with cuisine data: {len(with_cuisine)} out of {len(all_restaurants)}")

if with_cuisine:
    print("\nExample restaurant with cuisine:")
    r = with_cuisine[0]
    print(f"  Name: {r.get('name')}")
    print(f"  City: {r.get('city')}")
    print(f"  Cuisine: {r.get('cuisine')}")
