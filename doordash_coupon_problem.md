# DoorDash Coupon Optimization Problem

## Problem Statement

You have a shopping cart with items and a list of coupons. Your task is to:

1. Calculate the subtotal before coupons
2. Find the **best coupon** to apply (maximum discount)
3. Calculate the final price after applying the best coupon
4. Handle invalid coupons gracefully

**Key Constraint**: Only ONE coupon can be applied to the entire cart.

---

## Input Data Structures

### Cart Item
```python
{
    'price': float,      # Price of the item
    'category': str      # Category like 'fruit', 'toy', 'clothing'
}
```

### Coupon (Single Category)
```python
{
    'category': str,                      # Target category
    'percent_discount': int or None,      # Percentage off (e.g., 15 for 15%)
    'amount_discount': float or None,     # Dollar amount off (e.g., 10.0)
    'minimum_num_items_required': int,    # Min items in category
    'minimum_amount_required': float      # Min total price in category
}
```

### Coupon (Multi-Category) - Advanced Version
```python
{
    'categories': list[str],              # Multiple categories
    'percent_discount': int or None,
    'amount_discount': float or None,
    'minimum_num_items_required': int or None,
    'minimum_amount_required': float or None
}
```

---

## Business Rules

### Coupon Validity Rules

1. **Exactly ONE discount type**: Coupon must have EITHER `percent_discount` OR `amount_discount`, not both, not neither
2. **Category must exist in cart**: Can't apply a coupon for a category not in the cart
3. **Minimum items requirement**: Must have at least N items in the category
4. **Minimum amount requirement**: Total price of items in category must be >= minimum
5. **No category overlap** (multi-coupon): Each category can only appear in ONE coupon

### Discount Calculation

**Percent Discount:**
```
discount = category_total * (percent_discount / 100)
```

**Amount Discount:**
```
discount = min(amount_discount, category_total)  # Can't discount more than the category total
```

### Best Coupon Selection

- Calculate the discount amount for each valid coupon
- Choose the coupon that gives the **maximum discount**
- If no coupon is valid, apply no discount

---

## Example Walkthrough

### Example 1: Basic Single Coupon

**Cart:**
```python
[
    {'price': 2.00, 'category': 'fruit'},
    {'price': 8.00, 'category': 'fruit'},
    {'price': 20.00, 'category': 'toy'}
]
# Total: $30.00
# Fruit total: $10.00 (2 items)
```

**Coupon:**
```python
{
    'category': 'fruit',
    'percent_discount': 15,
    'amount_discount': None,
    'minimum_num_items_required': 2,
    'minimum_amount_required': 10.00
}
```

**Calculation:**
- Fruit items: 2 ✓ (meets minimum of 2)
- Fruit total: $10.00 ✓ (meets minimum of $10.00)
- Discount: $10.00 * 0.15 = $1.50
- **Final Price: $30.00 - $1.50 = $28.50**

---

### Example 2: Invalid Coupon (Not Enough Items)

**Cart:**
```python
[
    {'price': 2.00, 'category': 'fruit'},
    {'price': 8.00, 'category': 'fruit'}
]
# Fruit total: $10.00 (2 items)
```

**Coupon:**
```python
{
    'category': 'fruit',
    'percent_discount': 15,
    'amount_discount': None,
    'minimum_num_items_required': 3,  # Need 3 items!
    'minimum_amount_required': 10.00
}
```

**Result:**
- Fruit items: 2 ✗ (needs 3)
- Coupon is **invalid**
- **Final Price: $10.00** (no discount)

---

### Example 3: Multi-Category Coupon

**Cart:**
```python
[
    {'price': 2.00, 'category': 'fruit'},
    {'price': 8.00, 'category': 'fruit'},
    {'price': 20.00, 'category': 'toy'},
    {'price': 5.00, 'category': 'clothing'}
]
# Total: $35.00
```

**Multi-Coupon:**
```python
[
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
```

**Calculation:**
- First coupon applies to clothing ($5) + toy ($20) = $25 total
  - Best discount within: min($6, $25) = $6 off toy or clothing
- Second coupon applies to fruit ($10 total)
  - Discount: $10 * 0.15 = $1.50

- Best overall discount: $6 (from first coupon)
- **Final Price: $35.00 - $6.00 = $29.00**

---

## Key Edge Cases to Handle

1. **Both discount types present**: Return None (invalid)
2. **Neither discount type present**: Return None (invalid)
3. **Category overlap in multi-coupon**: Return None (invalid)
4. **Amount discount > category total**: Discount capped at category total
5. **Category not in cart**: Coupon doesn't apply
6. **No valid coupons**: Return original total

---

## Algorithm Steps

### Step 1: Validate All Coupons
```
For each coupon:
    - Must have exactly ONE discount type (percent OR amount, not both/neither)
```

### Step 2: Group Cart Items by Category
```
category_to_price = {
    'fruit': [total_price, item_count],
    'toy': [total_price, item_count],
    ...
}
```

### Step 3: Find Best Discount
```
For each coupon:
    For each category in coupon:
        - Check if minimum requirements are met
        - Calculate discount for this category
        - Track largest discount
    Apply largest discount from this coupon
Track the best coupon overall
```

### Step 4: Return Final Price
```
final_price = original_total - best_discount
```

---

## Common Mistakes to Avoid

1. **Not capping amount discount**: `amount_discount` can't exceed category total
2. **Forgetting to validate coupons**: Check for both/neither discount types
3. **Category overlap**: In multi-coupon, same category can't appear twice
4. **Not finding BEST discount**: Need to compare all valid coupons
5. **Modifying original total**: Track discount separately

---

## Interview Tips

1. **Ask clarifying questions**:
   - Can multiple coupons be applied? (Usually NO)
   - What if amount_discount > category total?
   - What to return for invalid coupons?

2. **Think out loud**:
   - "First, I'll validate the coupons..."
   - "Then I'll group items by category..."
   - "Next, I'll calculate discount for each coupon..."

3. **Test edge cases**:
   - Empty cart
   - No valid coupons
   - All items in one category
   - Multi-category coupons

4. **Time complexity**: O(C * K) where C = number of coupons, K = average categories per coupon
