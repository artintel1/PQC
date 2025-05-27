# Python implementation of a simplified Learning With Errors (LWE) encryption scheme
import numpy as np

def lwe_keygen(n, q, m=None):
    """
    Generates keys for the LWE encryption scheme.
    n: security parameter (dimension of the secret key vector s)
    q: modulus for all operations
    m: number of equations in the public key (A is m x n). Typically m > n log q.
       If None, defaults to 2*n.
    Returns a tuple (s, A, b):
        s: secret key vector (n x 1) of random integers mod q.
        A: public matrix (m x n) of random integers mod q.
        b: public vector (m x 1) computed as (A.s + e) mod q, where e is a small error vector.
    """
    if m is None:
        m = 2 * n  # A common choice for m

    # 1. Generate secret key vector s (n x 1) with elements in [0, q-1]
    s = np.random.randint(0, q, size=(n, 1))

    # 2. Generate public matrix A (m x n) with elements in [0, q-1]
    A = np.random.randint(0, q, size=(m, n))

    # 3. Generate error vector e (m x 1) with small random integers.
    #    The "smallness" is crucial for LWE security and correctness.
    #    Here, we'll choose errors from a small range, e.g., {-1, 0, 1} or a small Gaussian.
    #    For simplicity, let's use errors in a small range like [0, 1, 2] or [-1, 0, 1].
    #    A standard deviation for Gaussian noise is often sigma approx sqrt(alpha*q) where alpha is small.
    #    Let's use a simple discrete uniform distribution for errors, e.g., 0, 1, 2. Max error = 2.
    #    The error magnitude should be much smaller than q/4 for decryption to work.
    error_magnitude = 2 
    e = np.random.randint(0, error_magnitude + 1, size=(m, 1))
    # Alternative: Gaussian noise
    # e = np.round(np.random.normal(0, 1.0, size=(m,1))).astype(int) % q # Small Gaussian errors

    # 4. Compute public vector b = (A.s + e) mod q
    #    A (m x n), s (n x 1) => A.s (m x 1)
    #    e (m x 1)
    b = (np.dot(A, s) + e) % q

    return s, A, b

def lwe_encrypt(msg_bit, A, b, q, n, m=None):
    """
    Encrypts a single message bit using the LWE scheme.
    msg_bit: the message to encrypt (0 or 1).
    A: public matrix (m x n).
    b: public vector (m x 1).
    q: modulus.
    n: original security parameter (dimension of s).
    m: number of rows in A and b. If None, defaults to 2*n.

    Returns a tuple (u, v):
        u: ciphertext vector (1 x n) computed as (r.A) mod q.
        v: ciphertext scalar computed as (r.b + msg_bit * floor(q/2)) mod q.
        where r is a random binary vector (1 x m).
    """
    if m is None:
        m = A.shape[0]

    # 1. Generate a random "blinding" vector r (1 x m)
    #    Often, r is chosen to be a binary vector (elements are 0 or 1).
    #    This helps keep the error growth manageable.
    r = np.random.randint(0, 2, size=(1, m)) # Elements are 0 or 1

    # 2. Compute ciphertext component u = (r.A) mod q
    #    r (1 x m), A (m x n) => r.A (1 x n)
    u = np.dot(r, A) % q

    # 3. Compute ciphertext component v = (r.b + msg_bit * floor(q/2)) mod q
    #    r (1 x m), b (m x 1) => r.b (1 x 1, a scalar)
    #    Encoding the message bit: multiply by floor(q/2) to shift it away from 0 if msg_bit is 1.
    msg_encoded = msg_bit * (q // 2)
    v_scalar = (np.dot(r, b)[0,0] + msg_encoded) % q # Ensure scalar result from r.b

    return u, v_scalar # u is a row vector, v is a scalar

def lwe_decrypt(u, v, s, q):
    """
    Decrypts a ciphertext (u, v) using the secret key s.
    u: ciphertext vector (1 x n).
    v: ciphertext scalar.
    s: secret key vector (n x 1).
    q: modulus.

    Returns the decrypted message bit (0 or 1).
    """
    # 1. Compute dec_val = (v - u.s) mod q
    #    u (1 x n), s (n x 1) => u.s (1 x 1, a scalar)
    us_product = np.dot(u, s)[0,0] # Ensure scalar result
    dec_val = (v - us_product) % q

    # 2. Recover the message bit.
    #    If dec_val is closer to 0 (mod q) than to floor(q/2) (mod q), msg_bit was 0.
    #    Otherwise, msg_bit was 1.
    #    The condition is roughly: |dec_val| < q/4 implies 0, |dec_val - q/2| < q/4 implies 1.
    #    This works because the noise term r.e is small.
    #    v - u.s = (r.b + msg_bit*q/2) - (r.A).s
    #            = (r.(A.s + e) + msg_bit*q/2) - r.A.s
    #            = r.A.s + r.e + msg_bit*q/2 - r.A.s
    #            = r.e + msg_bit*q/2  (mod q)
    #    If msg_bit = 0, dec_val = r.e (small).
    #    If msg_bit = 1, dec_val = r.e + q/2 (close to q/2, if r.e is small).
    
    # Check if dec_val is in the interval [0, q/4) or (3q/4, q-1] (closer to 0)
    # or in the interval [q/4, 3q/4] (closer to q/2)
    # A simpler check:
    if dec_val < (q / 4) or dec_val > (3 * q / 4): # Closer to 0 (or q)
        return 0
    else: # Closer to q/2
        return 1

# Example Usage:
if __name__ == '__main__':
    # LWE Parameters
    n_param = 10      # Security parameter (dimension of s)
    # q_param needs to be a prime and large enough to handle noise, typically.
    # For simplicity, choose q such that q/2 is distinct and noise is < q/4.
    # If max error in e is E_e (e.g., 2) and r is binary (max 1),
    # then max r.e is roughly m * 1 * E_e. For m=2n=20, max r.e ~ 20*2 = 40.
    # We need 4 * max(r.e) < q. So, 4 * 40 = 160 < q.
    # Let's choose q = 257 (a prime number)
    q_param = 257    
    m_param = 2 * n_param # Number of LWE samples in public key A

    print(f"LWE Parameters: n={n_param}, q={q_param}, m={m_param}")
    print(f"Max possible noise in r.e could be around m*error_mag = {m_param}*{2} = {m_param*2}")
    print(f"Decryption requires noise < q/4 = {q_param/4:.2f}")
    if m_param * 2 >= q_param / 4:
        print("Warning: Parameters might be too small for reliable decryption due to noise.")
        print("Consider increasing q or reducing m or error magnitude for e.")
    print("-" * 40)

    # 1. Key Generation
    secret_key, public_A, public_b = lwe_keygen(n=n_param, q=q_param, m=m_param)
    print("Secret key s (first 5 elements):")
    print(secret_key[:5].T) # Transpose for row display
    print("Public matrix A (first 5x5 block):")
    print(public_A[:5, :5])
    print("Public vector b (first 5 elements):")
    print(public_b[:5].T) # Transpose for row display
    print("-" * 40)

    # 2. Message to encrypt (a single bit)
    message_bit_0 = 0
    message_bit_1 = 1

    # 3. Encryption
    print(f"Encrypting message bit: {message_bit_0}")
    u0, v0 = lwe_encrypt(message_bit_0, public_A, public_b, q_param, n_param, m_param)
    print("Ciphertext (u0, v0):")
    print(f"  u0 (first 5 elements): {u0[0, :5]}") # u0 is 1xn
    print(f"  v0: {v0}")
    print("-" * 20)

    print(f"Encrypting message bit: {message_bit_1}")
    u1, v1 = lwe_encrypt(message_bit_1, public_A, public_b, q_param, n_param, m_param)
    print("Ciphertext (u1, v1):")
    print(f"  u1 (first 5 elements): {u1[0, :5]}")
    print(f"  v1: {v1}")
    print("-" * 40)

    # 4. Decryption
    decrypted_bit_0 = lwe_decrypt(u0, v0, secret_key, q_param)
    print(f"Decrypting (u0, v0)... Result: {decrypted_bit_0}")
    print(f"Original bit: {message_bit_0}, Decrypted bit: {decrypted_bit_0} -> Correct: {message_bit_0 == decrypted_bit_0}")
    print("-" * 20)

    decrypted_bit_1 = lwe_decrypt(u1, v1, secret_key, q_param)
    print(f"Decrypting (u1, v1)... Result: {decrypted_bit_1}")
    print(f"Original bit: {message_bit_1}, Decrypted bit: {decrypted_bit_1} -> Correct: {message_bit_1 == decrypted_bit_1}")
    print("-" * 40)

    # Test with multiple encryptions/decryptions
    print("Running multiple encryption/decryption tests...")
    correct_count = 0
    test_iterations = 50
    for i in range(test_iterations):
        msg = np.random.randint(0,2)
        u_test, v_test = lwe_encrypt(msg, public_A, public_b, q_param, n_param, m_param)
        dec_msg = lwe_decrypt(u_test, v_test, secret_key, q_param)
        if msg == dec_msg:
            correct_count +=1
        # print(f"Msg: {msg}, Dec: {dec_msg}, Correct: {msg == dec_msg}")
    print(f"Success rate: {correct_count}/{test_iterations} = {(correct_count/test_iterations)*100:.2f}%")
    if correct_count < test_iterations:
        print("Some decryptions failed. This can happen if noise term r.e is too large.")
        print("The condition for correct decryption is that |(r.e) mod q| < q/4.")
        print("If r is binary {0,1}, then r.e is sum of subset of e_i values.")
        print("Max value of r.e is sum of all positive e_i which can be up to m * max(e_i).")
        print(f"Max r.e could be {m_param * 2} vs q/4 = {q_param/4}")
