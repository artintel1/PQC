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
        y = x1 - (a // b) * y1
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

    print("-" * 30) # Separator for the new test case

    a_test, b_test = 48, 18
    gcd_test, x_test, y_test = extended_gcd(a_test, b_test)
    print(f"\nTesting with a = {a_test}, b = {b_test}:")
    print(f"GCD({a_test}, {b_test}) = {gcd_test}")
    print(f"Coefficients: x = {x_test}, y = {y_test}")
    verification_passed = (a_test * x_test + b_test * y_test == gcd_test)
    print(f"Verification ({a_test}*x + {b_test}*y == gcd): {a_test}*{x_test} + {b_test}*{y_test} = {a_test*x_test + b_test*y_test} (Expected: {gcd_test})")
    print(f"Verification check passed: {verification_passed}")
