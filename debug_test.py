import requests

url = "https://jsonmock.hackerrank.com/api/food_outlets"

# Test what cities are available
params = {'page': 1}
response = requests.get(url, params=params)
data = response.json()

print(f"Total restaurants in API: {data.get('total')}")
print(f"Total pages: {data.get('total_pages')}")

# Check first few restaurants
print("\nFirst 5 restaurants:")
for r in data.get('data', [])[:5]:
    print(f"  - {r.get('name')} | City: {r.get('city')} | Rating: {r.get('user_rating', {}).get('average_rating')} | Cuisine: {r.get('cuisine')}")

# Test with Seattle specifically
print("\n\nTesting Seattle:")
params = {'city': 'Seattle', 'page': 1}
response = requests.get(url, params=params)
data = response.json()

print(f"Total Seattle restaurants: {data.get('total')}")
print(f"Restaurants on page 1: {len(data.get('data', []))}")

if data.get('data'):
    print("\nFirst Seattle restaurant:")
    r = data['data'][0]
    print(f"  Name: {r.get('name')}")
    print(f"  City: {r.get('city')}")
    print(f"  Rating: {r.get('user_rating', {}).get('average_rating')}")
    print(f"  Cuisine: {r.get('cuisine')}")
    print(f"  Cost: {r.get('estimated_cost')}")
