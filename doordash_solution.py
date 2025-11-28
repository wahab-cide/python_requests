"""
DoorDash Coupon Optimization Problem - Clean Solution

This solution finds the best coupon to apply to a shopping cart
to maximize the discount.
"""

from typing import List, Dict, Optional, Union


def calculate_best_coupon(coupons: List[Dict], cart: List[Dict]) -> Optional[float]:
    """
    Calculate the final price after applying the best coupon to the cart.

    Args:
        coupons: List of coupon dictionaries (can be single or multi-category)
        cart: List of item dictionaries with 'price' and 'category'

    Returns:
        Final price after applying best coupon, or None if coupons are invalid

    Example:
        cart = [
            {'price': 2.00, 'category': 'fruit'},
            {'price': 8.00, 'category': 'fruit'}
        ]
        coupon = [{
            'categories': ['fruit'],
            'percent_discount': 15,
            'amount_discount': None,
            'minimum_num_items_required': 2,
            'minimum_amount_required': 10.00
        }]
        result = calculate_best_coupon(coupon, cart)  # Returns 8.50
    """

    # Step 1: Validate all coupons
    if not _validate_coupons(coupons):
        return None

    # Step 2: Build category summary from cart
    # category_to_price[category] = [total_price, item_count]
    category_to_price = {}
    total_price = 0

    for item in cart:
        category = item['category']
        price = item['price']

        if category not in category_to_price:
            category_to_price[category] = [0, 0]

        category_to_price[category][0] += price  # total price
        category_to_price[category][1] += 1      # item count

        total_price += price

    # Step 3: Check for category overlap (each category can only appear once)
    seen_categories = set()
    for coupon in coupons:
        for category in coupon['categories']:
            if category in seen_categories:
                return None  # Category appears in multiple coupons - invalid
            seen_categories.add(category)

    # Step 4: Find best discount across all coupons
    best_discount = 0

    for coupon in coupons:
        # Find the best discount within this coupon (across its categories)
        coupon_best_discount = _calculate_coupon_discount(
            coupon,
            category_to_price
        )
        best_discount = max(best_discount, coupon_best_discount)

    # Step 5: Return final price
    return total_price - best_discount


def _validate_coupons(coupons: List[Dict]) -> bool:
    """
    Validate that all coupons have exactly ONE discount type.

    A valid coupon must have EITHER percent_discount OR amount_discount,
    not both and not neither.
    """
    for coupon in coupons:
        has_percent = coupon.get('percent_discount') is not None
        has_amount = coupon.get('amount_discount') is not None

        # Invalid if both or neither
        if has_percent == has_amount:  # Both True or both False
            return False

    return True


def _calculate_coupon_discount(
    coupon: Dict,
    category_to_price: Dict[str, List[float]]
) -> float:
    """
    Calculate the maximum discount this coupon can provide.

    For a multi-category coupon, we find the category that gives
    the largest discount (if requirements are met).

    Args:
        coupon: Single coupon dictionary
        category_to_price: Map of category -> [total_price, item_count]

    Returns:
        Maximum discount amount from this coupon
    """
    max_discount = 0

    for category in coupon['categories']:
        # Skip if category not in cart
        if category not in category_to_price:
            continue

        category_total = category_to_price[category][0]
        category_count = category_to_price[category][1]

        # Check if minimum requirements are met
        min_items = coupon.get('minimum_num_items_required')
        min_amount = coupon.get('minimum_amount_required')

        # If minimums specified, check them
        if min_items is not None and category_count < min_items:
            continue

        if min_amount is not None and category_total < min_amount:
            continue

        # Calculate discount for this category
        discount = 0

        if coupon.get('percent_discount') is not None:
            # Percent discount
            percent = coupon['percent_discount']
            discount = category_total * (percent / 100)

        elif coupon.get('amount_discount') is not None:
            # Amount discount (capped at category total)
            amount = coupon['amount_discount']
            discount = min(amount, category_total)

        # Track the best discount within this coupon
        max_discount = max(max_discount, discount)

    return max_discount


# HELPER FUNCTION FOR DETAILED RESULTS

def calculate_with_details(coupons: List[Dict], cart: List[Dict]) -> Dict:
    """
    Enhanced version that returns detailed breakdown.

    Returns:
        {
            'subtotal': float,
            'best_coupon_index': int or None,
            'discount_amount': float,
            'final_price': float,
            'valid': bool
        }
    """
    # Calculate subtotal
    subtotal = sum(item['price'] for item in cart)

    # Validate coupons
    if not _validate_coupons(coupons):
        return {
            'subtotal': subtotal,
            'best_coupon_index': None,
            'discount_amount': 0,
            'final_price': subtotal,
            'valid': False,
            'error': 'Invalid coupon configuration'
        }

    # Build category summary
    category_to_price = {}
    for item in cart:
        category = item['category']
        if category not in category_to_price:
            category_to_price[category] = [0, 0]
        category_to_price[category][0] += item['price']
        category_to_price[category][1] += 1

    # Check for category overlap
    seen_categories = set()
    for coupon in coupons:
        for category in coupon['categories']:
            if category in seen_categories:
                return {
                    'subtotal': subtotal,
                    'best_coupon_index': None,
                    'discount_amount': 0,
                    'final_price': subtotal,
                    'valid': False,
                    'error': 'Category overlap in coupons'
                }
            seen_categories.add(category)

    # Find best coupon
    best_discount = 0
    best_coupon_index = None

    for idx, coupon in enumerate(coupons):
        discount = _calculate_coupon_discount(coupon, category_to_price)
        if discount > best_discount:
            best_discount = discount
            best_coupon_index = idx

    return {
        'subtotal': subtotal,
        'best_coupon_index': best_coupon_index,
        'discount_amount': best_discount,
        'final_price': subtotal - best_discount,
        'valid': True
    }


# TEST CASES

def test_basic_percent_discount():
    """Test basic percent discount coupon"""
    cart = [
        {'price': 2.00, 'category': 'fruit'},
        {'price': 8.00, 'category': 'fruit'}
    ]

    coupons = [{
        'categories': ['fruit'],
        'percent_discount': 15,
        'amount_discount': None,
        'minimum_num_items_required': 2,
        'minimum_amount_required': 10.00
    }]

    result = calculate_best_coupon(coupons, cart)
    expected = 8.50  # 10 - (10 * 0.15) = 8.50

    assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
    print(f"✓ Test basic percent discount: ${result:.2f}")


def test_amount_discount():
    """Test fixed amount discount"""
    cart = [
        {'price': 2.00, 'category': 'fruit'},
        {'price': 8.00, 'category': 'fruit'}
    ]

    coupons = [{
        'categories': ['fruit'],
        'percent_discount': None,
        'amount_discount': 3.00,
        'minimum_num_items_required': 2,
        'minimum_amount_required': 10.00
    }]

    result = calculate_best_coupon(coupons, cart)
    expected = 7.00  # 10 - 3 = 7

    assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
    print(f"✓ Test amount discount: ${result:.2f}")


def test_amount_discount_capped():
    """Test amount discount capped at category total"""
    cart = [
        {'price': 5.00, 'category': 'fruit'}
    ]

    coupons = [{
        'categories': ['fruit'],
        'percent_discount': None,
        'amount_discount': 20.00,  # More than cart total!
        'minimum_num_items_required': None,
        'minimum_amount_required': None
    }]

    result = calculate_best_coupon(coupons, cart)
    expected = 0.00  # 5 - min(20, 5) = 0

    assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
    print(f"✓ Test amount discount capped: ${result:.2f}")


def test_invalid_not_enough_items():
    """Test coupon that doesn't meet minimum items requirement"""
    cart = [
        {'price': 2.00, 'category': 'fruit'},
        {'price': 8.00, 'category': 'fruit'}
    ]

    coupons = [{
        'categories': ['fruit'],
        'percent_discount': 15,
        'amount_discount': None,
        'minimum_num_items_required': 3,  # Need 3, only have 2
        'minimum_amount_required': 10.00
    }]

    result = calculate_best_coupon(coupons, cart)
    expected = 10.00  # No discount applied

    assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
    print(f"✓ Test insufficient items: ${result:.2f}")


def test_multi_category_coupon():
    """Test multi-category coupon finding best discount"""
    cart = [
        {'price': 2.00, 'category': 'fruit'},
        {'price': 8.00, 'category': 'fruit'},
        {'price': 20.00, 'category': 'toy'},
        {'price': 5.00, 'category': 'clothing'}
    ]

    coupons = [
        {
            'categories': ['clothing', 'toy'],
            'percent_discount': None,
            'amount_discount': 6,
            'minimum_num_items_required': None,
            'minimum_amount_required': None
        },
        {
            'categories': ['fruit'],
            'percent_discount': 15,
            'amount_discount': None,
            'minimum_num_items_required': 2,
            'minimum_amount_required': 10.00
        }
    ]

    result = calculate_best_coupon(coupons, cart)
    # Coupon 1: Can discount $6 from toy or clothing (best is $6)
    # Coupon 2: 15% of $10 = $1.50
    # Best: $6 discount
    expected = 29.00  # 35 - 6 = 29

    assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
    print(f"✓ Test multi-category coupon: ${result:.2f}")


def test_invalid_both_discounts():
    """Test invalid coupon with both discount types"""
    cart = [{'price': 10.00, 'category': 'fruit'}]

    coupons = [{
        'categories': ['fruit'],
        'percent_discount': 15,
        'amount_discount': 10,  # Can't have both!
        'minimum_num_items_required': None,
        'minimum_amount_required': None
    }]

    result = calculate_best_coupon(coupons, cart)
    assert result is None, "Should return None for invalid coupon"
    print(f"✓ Test invalid coupon (both discounts): None")


def test_category_overlap():
    """Test invalid multi-coupon with category overlap"""
    cart = [
        {'price': 10.00, 'category': 'fruit'},
        {'price': 5.00, 'category': 'clothing'}
    ]

    coupons = [
        {
            'categories': ['fruit', 'clothing'],
            'percent_discount': None,
            'amount_discount': 5,
            'minimum_num_items_required': None,
            'minimum_amount_required': None
        },
        {
            'categories': ['fruit'],  # Duplicate!
            'percent_discount': 10,
            'amount_discount': None,
            'minimum_num_items_required': None,
            'minimum_amount_required': None
        }
    ]

    result = calculate_best_coupon(coupons, cart)
    assert result is None, "Should return None for category overlap"
    print(f"✓ Test category overlap: None")


def run_all_tests():
    """Run all test cases"""
    print("\nRunning DoorDash Coupon Tests...")
    print("=" * 50)

    test_basic_percent_discount()
    test_amount_discount()
    test_amount_discount_capped()
    test_invalid_not_enough_items()
    test_multi_category_coupon()
    test_invalid_both_discounts()
    test_category_overlap()

    print("=" * 50)
    print("All tests passed! ✓\n")


if __name__ == "__main__":
    run_all_tests()

    # Example usage with detailed results
    print("\nDetailed Example:")
    print("=" * 50)

    cart = [
        {'price': 2.00, 'category': 'fruit'},
        {'price': 8.00, 'category': 'fruit'},
        {'price': 20.00, 'category': 'toy'}
    ]

    coupons = [{
        'categories': ['fruit'],
        'percent_discount': 15,
        'amount_discount': None,
        'minimum_num_items_required': 2,
        'minimum_amount_required': 10.00
    }]

    details = calculate_with_details(coupons, cart)
    print(f"Subtotal: ${details['subtotal']:.2f}")
    print(f"Best coupon: #{details['best_coupon_index']}")
    print(f"Discount: ${details['discount_amount']:.2f}")
    print(f"Final price: ${details['final_price']:.2f}")
