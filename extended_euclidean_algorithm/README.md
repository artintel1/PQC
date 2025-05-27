# Extended Euclidean Algorithm

The Extended Euclidean Algorithm is an extension of the Euclidean Algorithm. While the Euclidean Algorithm is used to find the greatest common divisor (GCD) of two integers, the Extended Euclidean Algorithm also finds the integer coefficients `x` and `y` such that:

`a*x + b*y = gcd(a, b)`

This is known as Bézout's identity.

## Algorithm Steps

The algorithm is typically implemented recursively. Here's a step-by-step breakdown:

1.  **Base Case**:
    *   If `b` is 0, then `gcd(a, 0) = a`.
    *   In this case, Bézout's identity becomes `a*x + 0*y = a`.
    *   We can satisfy this with `x = 1` and `y = 0`. So, we return `(a, 1, 0)`.

2.  **Recursive Step**:
    *   If `b` is not 0, we make a recursive call with `b` and `a % b` (the remainder of `a` divided by `b`).
        Let `gcd, x₁, y₁ = extended_gcd(b, a % b)`.
    *   From this recursive call, we know that `b*x₁ + (a % b)*y₁ = gcd`.
    *   We need to find `x` and `y` such that `a*x + b*y = gcd`.
    *   We can express `a % b` as `a - floor(a/b) * b`.
    *   Substitute this into the equation from the recursive call:
        `b*x₁ + (a - floor(a/b) * b)*y₁ = gcd`
    *   Rearrange the terms to group `a` and `b`:
        `b*x₁ + a*y₁ - floor(a/b)*b*y₁ = gcd`
        `a*y₁ + b*(x₁ - floor(a/b)*y₁) = gcd`
    *   Comparing this with `a*x + b*y = gcd`, we can see that:
        *   `x = y₁`
        *   `y = x₁ - floor(a/b)*y₁`
    *   So, we return `(gcd, y₁, x₁ - floor(a/b)*y₁)`.

## Python Implementation

The Python code in `extended_euclidean_algorithm.py` implements this algorithm:

```python
# Python implementation of the Extended Euclidean Algorithm
def extended_gcd(a, b):
    """
    Returns a tuple (gcd, x, y) such that a*x + b*y = gcd(a, b).
    """
    # Base Case: if b is 0, then gcd is a, x is 1, and y is 0
    # a*1 + b*0 = a
    if b == 0:
        return a, 1, 0
    else:
        # Recursively call extended_gcd with b and a % b
        # This is based on the property: gcd(a, b) = gcd(b, a % b)
        gcd, x1, y1 = extended_gcd(b, a % b)

        # Update x and y using results of recursive call
        # The relationship is derived from the equations:
        # gcd = b*x1 + (a % b)*y1
        # gcd = b*x1 + (a - floor(a/b)*b)*y1
        # gcd = b*x1 + a*y1 - floor(a/b)*b*y1
        # gcd = a*y1 + b*(x1 - floor(a/b)*y1)
        # So, x = y1 and y = x1 - floor(a/b)*y1
        x = y1
        y = x1 - (a // b) * y1 # In Python, // is integer division (floor division)
        return gcd, x, y

# Example usage:
if __name__ == '__main__':
    a, b = 35, 15
    gcd, x, y = extended_gcd(a, b)
    print(f"The GCD of {a} and {b} is {gcd}")
    print(f"Coefficients x and y are: x = {x}, y = {y}")
    print(f"Verification: {a}*{x} + {b}*{y} = {a*x + b*y}")

    a, b = 240, 46
    gcd, x, y = extended_gcd(a, b)
    print(f"\nThe GCD of {a} and {b} is {gcd}")
    print(f"Coefficients x and y are: x = {x}, y = {y}")
    print(f"Verification: {a}*{x} + {b}*{y} = {a*x + b*y}")
```

### Explanation of the Code:

1.  **Function Definition**:
    *   `extended_gcd(a, b)`: This function takes two integers, `a` and `b`, as input.

2.  **Base Case**:
    *   `if b == 0:`: This checks for the base case.
    *   `return a, 1, 0`: If `b` is 0, it returns the GCD (`a`), `x=1`, and `y=0`.

3.  **Recursive Step**:
    *   `else:`: If `b` is not 0.
    *   `gcd, x1, y1 = extended_gcd(b, a % b)`: This is the recursive call. It calls `extended_gcd` with `b` and `a % b`. The results `gcd`, `x₁`, and `y₁` are unpacked. Note that `x1` and `y1` here correspond to the coefficients for `b` and `a % b` respectively.
    *   `x = y1`: As derived in the algorithm steps, the new `x` is the `y₁` from the recursive call.
    *   `y = x1 - (a // b) * y1`: The new `y` is calculated using `x₁` and `y₁` from the recursive call and the integer division `a // b`.
    *   `return gcd, x, y`: The function returns the computed `gcd`, and the coefficients `x` and `y` for the original `a` and `b`.

The example usage in the `if __name__ == '__main__':` block demonstrates how to call the function and verifies that the returned `x` and `y` satisfy Bézout's identity.
This detailed README.md should now correctly explain the algorithm and its implementation.
