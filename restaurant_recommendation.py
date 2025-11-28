"""
HackerRank Restaurant Recommendation System
This solution demonstrates:
- Making API calls with pagination
- Data filtering and transformation
- Business logic implementation
- Sorting by multiple criteria
"""

import requests
from typing import List, Dict, Optional


# STEP 1: FETCH DATA FROM API (with pagination)

def fetch_restaurants_by_city(city: str) -> List[Dict]:
    """
    Fetch all restaurant data for a given city from the HackerRank API.

    The API returns paginated results, so we need to:
    1. Make the first request to get total_pages
    2. Loop through all pages
    3. Collect all restaurant data

    Args:
        city: City name to search for restaurants

    Returns:
        List of all restaurant dictionaries
    """
    base_url = "https://jsonmock.hackerrank.com/api/food_outlets"
    all_restaurants = []
    page = 1

    # Keep fetching until we've got all pages
    while True:
        # Build URL with query parameters
        params = {
            'city': city,
            'page': page
        }

        try:
            # Make the API call
            response = requests.get(base_url, params=params, timeout=10)

            # Check for HTTP errors
            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            # Extract pagination info
            current_page = data.get('page', 0)
            total_pages = data.get('total_pages', 0)
            restaurants = data.get('data', [])

            # Add restaurants from this page
            all_restaurants.extend(restaurants)

            print(f"Fetched page {current_page}/{total_pages} - {len(restaurants)} restaurants")

            # Check if we're done
            if current_page >= total_pages:
                break

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break

    return all_restaurants


# STEP 2: FETCH USER PREFERENCES (mock implementation)

def fetch_user_preferences(user_id: str) -> Dict:
    """
    In a real scenario, this would call an API.
    For this example, we'll return mock data.

    Args:
        user_id: User identifier

    Returns:
        Dictionary with user tier and preferences
    """
    # Mock user data - in real HackerRank problem this would be an API call
    mock_users = {
        'user1': {'tier': 'gold', 'name': 'John Doe'},
        'user2': {'tier': 'silver', 'name': 'Jane Smith'},
        'user3': {'tier': 'bronze', 'name': 'Bob Johnson'},
    }

    return mock_users.get(user_id, {'tier': 'bronze', 'name': 'Guest'})


# STEP 3: APPLY BUSINESS RULES (discounts, delivery fees, filtering)

def calculate_discount_rate(tier: str) -> float:
    """
    Calculate discount rate based on user tier.

    Business Rules:
    - Gold: 20% discount
    - Silver: 10% discount
    - Bronze: No discount

    Args:
        tier: User tier (gold, silver, bronze)

    Returns:
        Discount rate as decimal (0.20 for 20%)
    """
    discount_rates = {
        'gold': 0.20,
        'silver': 0.10,
        'bronze': 0.0
    }
    return discount_rates.get(tier.lower(), 0.0)


def calculate_delivery_fee(tier: str, subtotal: float) -> float:
    """
    Calculate delivery fee based on user tier and order subtotal.

    Business Rules:
    - Gold: Free delivery over $30
    - Silver: Free delivery over $50
    - Bronze: $5 delivery fee (always)

    Args:
        tier: User tier
        subtotal: Order subtotal after discount

    Returns:
        Delivery fee amount
    """
    tier_lower = tier.lower()

    if tier_lower == 'gold':
        return 0.0 if subtotal >= 30 else 5.0
    elif tier_lower == 'silver':
        return 0.0 if subtotal >= 50 else 5.0
    elif tier_lower == 'bronze':
        return 5.0
    else:
        return 5.0


def process_restaurant_data(restaurants: List[Dict], user_tier: str) -> List[Dict]:
    """
    Process restaurant data by:
    1. Filtering restaurants with rating >= 4.0
    2. Applying discount based on user tier
    3. Calculating delivery fees
    4. Computing final price

    Args:
        restaurants: List of restaurant dictionaries
        user_tier: User's membership tier

    Returns:
        List of processed restaurant dictionaries with pricing info
    """
    processed = []
    discount_rate = calculate_discount_rate(user_tier)

    for restaurant in restaurants:
        # Extract data (using .get() for safe access)
        name = restaurant.get('name', 'Unknown')
        rating = restaurant.get('user_rating', {}).get('average_rating', 0.0)
        estimated_cost = restaurant.get('estimated_cost', 0)

        # FILTER: Only include restaurants with rating >= 4.0
        if rating < 4.0:
            continue

        # CALCULATE: Apply discount
        discount_amount = estimated_cost * discount_rate
        subtotal = estimated_cost - discount_amount

        # CALCULATE: Delivery fee
        delivery_fee = calculate_delivery_fee(user_tier, subtotal)

        # CALCULATE: Final price
        final_price = subtotal + delivery_fee

        # Build result dictionary with all calculated fields
        processed.append({
            'name': name,
            'rating': rating,
            'original_price': estimated_cost,
            'discount_rate': discount_rate,
            'discount_amount': discount_amount,
            'subtotal': subtotal,
            'delivery_fee': delivery_fee,
            'final_price': final_price,
            'city': restaurant.get('city', ''),
            'cuisine': restaurant.get('cuisine', []),
            'address': restaurant.get('address', '')
        })

    return processed


# STEP 4: SORT AND RETURN TOP RECOMMENDATIONS

def get_top_recommendations(
    city: str,
    user_tier: str,
    top_n: int = 5
) -> List[Dict]:
    """
    Main function that orchestrates the entire recommendation process.

    Process:
    1. Fetch all restaurants for the city
    2. Filter by rating >= 4.0
    3. Apply discounts based on user tier
    4. Calculate delivery fees
    5. Sort by final price (ascending)
    6. Return top N recommendations

    Args:
        city: City to search for restaurants
        user_tier: User's membership tier (gold, silver, bronze)
        top_n: Number of recommendations to return

    Returns:
        List of top N restaurant recommendations sorted by final price
    """
    print(f"\nFetching restaurants in {city} for {user_tier} tier user...")

    # Step 1: Fetch restaurant data from API
    restaurants = fetch_restaurants_by_city(city)
    print(f"Total restaurants found: {len(restaurants)}")

    # Step 2-4: Process data (filter, calculate prices)
    processed = process_restaurant_data(restaurants, user_tier)
    print(f"Restaurants with rating >= 4.0: {len(processed)}")

    # Step 5: Sort by final price (lowest first)
    sorted_restaurants = sorted(processed, key=lambda x: x['final_price'])

    # Step 6: Return top N
    top_recommendations = sorted_restaurants[:top_n]

    return top_recommendations


# STEP 5: DISPLAY RESULTS

def display_recommendations(recommendations: List[Dict], user_tier: str):
    """
    Display recommendations in a user-friendly format.

    Args:
        recommendations: List of restaurant dictionaries
        user_tier: User's tier for context
    """
    if not recommendations:
        print("No recommendations found.")
        return

    print(f"\n{'='*80}")
    print(f"TOP RESTAURANT RECOMMENDATIONS ({user_tier.upper()} TIER)")
    print(f"{'='*80}\n")

    for idx, restaurant in enumerate(recommendations, 1):
        print(f"{idx}. {restaurant['name']}")
        print(f"   Rating: {restaurant['rating']:.1f} stars")
        print(f"   Original Price: ${restaurant['original_price']:.2f}")

        if restaurant['discount_amount'] > 0:
            print(f"   Discount ({restaurant['discount_rate']*100:.0f}%): -${restaurant['discount_amount']:.2f}")

        print(f"   Subtotal: ${restaurant['subtotal']:.2f}")

        if restaurant['delivery_fee'] > 0:
            print(f"   Delivery Fee: ${restaurant['delivery_fee']:.2f}")
        else:
            print(f"   Delivery Fee: FREE")

        print(f"   FINAL PRICE: ${restaurant['final_price']:.2f}")
        print(f"   Cuisine: {', '.join(restaurant['cuisine']) if restaurant['cuisine'] else 'N/A'}")
        print(f"   Address: {restaurant['address']}")
        print()


# EXAMPLE USAGE

def main():
    """
    Example usage of the restaurant recommendation system.
    """
    # Test different user tiers
    test_cases = [
        {'city': 'Seattle', 'user_id': 'user1', 'tier': 'gold'},
        {'city': 'Seattle', 'user_id': 'user2', 'tier': 'silver'},
        {'city': 'Seattle', 'user_id': 'user3', 'tier': 'bronze'},
    ]

    for test in test_cases:
        city = test['city']
        tier = test['tier']

        # Get recommendations
        recommendations = get_top_recommendations(city, tier, top_n=3)

        # Display results
        display_recommendations(recommendations, tier)

        print("\n" + "="*80 + "\n")


# KEY TAKEAWAYS FOR HACKERRANK PROBLEMS

"""
PATTERN SUMMARY:
----------------

1. PAGINATION:
   - Always check for 'page' and 'total_pages' in response
   - Use while loop to fetch all pages
   - Accumulate data in a list

2. FILTERING:
   - Use list comprehension: [item for item in items if condition]
   - Or filter during processing with if statements

3. TRANSFORMATION:
   - Add calculated fields to each item
   - Use dictionary comprehension or loops
   - Pattern: {**original_dict, 'new_field': value}

4. SORTING:
   - sorted(items, key=lambda x: x['field'])
   - Use negative for descending: key=lambda x: -x['field']
   - Multiple criteria: key=lambda x: (x['field1'], x['field2'])

5. BUSINESS LOGIC:
   - Break complex logic into small functions
   - Each function handles one concern
   - Easy to test and debug

6. ERROR HANDLING:
   - Always use try/except for API calls
   - Set timeouts
   - Use .get() for safe dictionary access

COMMON HACKERRANK API RESPONSE FORMAT:
---------------------------------------
{
    "page": 1,
    "per_page": 10,
    "total": 100,
    "total_pages": 10,
    "data": [
        {...},
        {...}
    ]
}
"""


if __name__ == "__main__":
    main()