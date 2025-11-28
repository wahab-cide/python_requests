

import requests


def test_api_structure():
    """
    First, let's understand the API response structure.
    This is ALWAYS your first step with any HackerRank API problem.
    """
    url = "https://jsonmock.hackerrank.com/api/food_outlets"

    # Test 1: Call with just city parameter
    print("Test 1: Understanding the API response structure")
    print("=" * 60)

    params = {
        'city': 'Seattle',
        'page': 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        # Print the structure
        print(f"Keys in response: {data.keys()}")
        print(f"\nPage: {data.get('page')}")
        print(f"Per Page: {data.get('per_page')}")
        print(f"Total: {data.get('total')}")
        print(f"Total Pages: {data.get('total_pages')}")
        print(f"Number of restaurants in this page: {len(data.get('data', []))}")

        # Look at the first restaurant to understand the data structure
        if data.get('data'):
            first_restaurant = data['data'][0]
            print(f"\nFirst restaurant structure:")
            print(f"Keys: {first_restaurant.keys()}")
            print(f"\nExample restaurant:")
            import json
            print(json.dumps(first_restaurant, indent=2))
    else:
        print(f"Error: {response.status_code}")


def test_filtering_and_sorting():
    """
    Practice filtering and sorting - core skills for HackerRank.
    """
    print("\n\nTest 2: Filtering and Sorting Practice")
    print("=" * 60)

    # Fetch data
    url = "https://jsonmock.hackerrank.com/api/food_outlets"
    params = {'city': 'Seattle', 'page': 1}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching data")
        return

    restaurants = response.json().get('data', [])

    # Filter: Only restaurants with rating >= 4.0
    high_rated = [
        r for r in restaurants
        if r.get('user_rating', {}).get('average_rating', 0) >= 4.0
    ]

    print(f"Total restaurants: {len(restaurants)}")
    print(f"High rated (>=4.0): {len(high_rated)}")

    # Sort by rating (descending)
    sorted_by_rating = sorted(
        high_rated,
        key=lambda x: x.get('user_rating', {}).get('average_rating', 0),
        reverse=True
    )

    # Display top 3
    print(f"\nTop 3 highest rated:")
    for idx, r in enumerate(sorted_by_rating[:3], 1):
        name = r.get('name', 'Unknown')
        rating = r.get('user_rating', {}).get('average_rating', 0)
        cost = r.get('estimated_cost', 0)
        print(f"{idx}. {name} - Rating: {rating}, Cost: ${cost}")


def test_pagination():
    """
    Practice fetching all pages - VERY common in HackerRank.
    """
    print("\n\nTest 3: Pagination Practice")
    print("=" * 60)

    url = "https://jsonmock.hackerrank.com/api/food_outlets"
    all_restaurants = []
    city = "Seattle"
    page = 1

    while True:
        params = {'city': city, 'page': page}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        current_page = data.get('page', 0)
        total_pages = data.get('total_pages', 0)
        restaurants = data.get('data', [])

        all_restaurants.extend(restaurants)
        print(f"Page {current_page}/{total_pages}: {len(restaurants)} restaurants")

        if current_page >= total_pages:
            break

        page += 1

    print(f"\nTotal restaurants fetched across all pages: {len(all_restaurants)}")


def practice_problem():
    """
    PRACTICE PROBLEM: Try this yourself!

    Problem: Find the cheapest restaurant in Seattle with:
    - Rating >= 4.5
    - Serves "Italian" cuisine
    - Sort by price (lowest first)

    Print the top 3 results.
    """
    print("\n\nPractice Problem - Try to implement this!")

    # YOUR CODE HERE
    # Hints:
    # 1. Fetch all pages for Seattle
    # 2. Filter by rating >= 4.5
    # 3. Filter by cuisine (check if 'Italian' in cuisine list)
    # 4. Sort by estimated_cost
    # 5. Print top 3

    url = "https://jsonmock.hackerrank.com/api/food_outlets"

    params = {'city': 'Seattle', 'page': 1}
    page = 1
    total_pages = 1
    all_restaurants = []
    response = None

    try:
        while page <= total_pages:
            params['page'] = page
            response = requests.get(url, params=params)

            data = response.json()
            all_restaurants.extend(data.get('data', []))

            page = data.get('page', 0)
            total_pages = data.get('total_pages', 0)

            if page >= total_pages:
                break
            page += 1


    except requests.exceptions.Timeout:
        print(response.status_code)

    print(response.status_code)
    higher_rated = [r for r in all_restaurants if r.get('user_rating', {}).get('average_rating', 0) >= 4.5]

    has_italian_cuisine = higher_rated

    sorted_by_estcost = sorted(has_italian_cuisine, key = lambda x:x.get('estimated_cost', 0))

    for idx, r in enumerate(sorted_by_estcost[:3], 1):
        name = r.get('name', 'Unknown')
        average_rating = r.get('user_rating', {}).get('average_rating', 0)
        estimated_cost = r.get('estimated_cost', 0)
        print(f"Name: {name} --- Average Rating: {average_rating} --- Estimated Cost: {estimated_cost}")



if __name__ == "__main__":
    # Run all tests
    #test_api_structure()
    #test_filtering_and_sorting()
    #test_pagination()
    practice_problem()

    print("\n\n" + "=" * 60)
    print("Experiment with your own queries above!")
    print("=" * 60)