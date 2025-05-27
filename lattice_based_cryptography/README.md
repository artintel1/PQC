# Learning With Errors (LWE) Based Cryptography - Simplified Scheme

This directory contains a Python implementation of a simplified public-key encryption scheme based on the Learning With Errors (LWE) problem. LWE is a hard computational problem that serves as a foundation for many modern post-quantum cryptographic systems.

## Learning With Errors Problem

The LWE problem, in its decision form, is to distinguish between two types of distributions:
1.  Pairs `(A, b)` where `A` is a matrix of random integers modulo `q`, and `b` is a vector of truly random integers modulo `q`.
2.  Pairs `(A, b)` where `A` is a matrix of random integers modulo `q`, `s` is a fixed secret vector modulo `q`, `e` is a "small" error vector, and `b = (A.s + e) mod q`.

Solving LWE (i.e., finding `s` given `A` and `b` when `e` is small) is believed to be computationally hard, especially for specific choices of parameters.

## LWE Encryption Scheme Overview

The implemented scheme is a basic public-key encryption system capable of encrypting single bits.

### 1. Key Generation (`lwe_keygen`)

The key generation process creates a public key `(A, b)` and a secret key `s`.

**Parameters:**
*   `n`: Security parameter. This is the dimension of the secret key vector `s`.
*   `q`: A prime modulus for all arithmetic operations. It should be large enough to accommodate the noise introduced by the error term `e` and the encryption process.
*   `m`: The number of LWE samples (rows) in the public matrix `A`. Typically, `m` is chosen to be somewhat larger than `n` (e.g., `m > n log q`, often `m = 2n` is used for simplicity in basic schemes).

**Steps:**
1.  **Secret Key `s`**: A vector of `n` random integers is generated, where each element is chosen from `[0, q-1]`. This is `s` (size `n x 1`).
2.  **Public Matrix `A`**: A matrix of size `m x n` is generated, where each element is a random integer chosen from `[0, q-1]`.
3.  **Error Vector `e`**: An error vector `e` of size `m x 1` is generated. The crucial property of `e` is that its elements are "small" compared to `q`. For instance, they can be chosen from a discrete uniform distribution like `{-1, 0, 1}` or ` {0, 1, 2}`, or sampled from a discrete Gaussian distribution centered at 0.
4.  **Public Vector `b`**: The second part of the public key, vector `b` (size `m x 1`), is computed as `b = (A.s + e) mod q`.

**Output**: The function returns the secret key `s` and the public key `(A, b)`.

### 2. Encryption (`lwe_encrypt`)

Encrypts a single message bit `msg_bit` (0 or 1).

**Parameters:**
*   `msg_bit`: The message bit to encrypt (0 or 1).
*   `A`, `b`: The public key components.
*   `q`: The modulus.
*   `n`: The original security parameter (dimension of `s`).
*   `m`: The number of rows in `A` and `b`.

**Steps:**
1.  **Random Blinding Vector `r`**: A random binary vector `r` of size `1 x m` (row vector) is generated. Its elements are typically 0 or 1. This vector helps in selecting a random subset of the equations in `A` and `b`, effectively adding more noise to mask the message.
2.  **Ciphertext Component `u`**: Compute `u = (r.A) mod q`. This results in a vector of size `1 x n`.
3.  **Ciphertext Component `v`**: Compute `v = (r.b + msg_bit * floor(q/2)) mod q`. This results in a scalar value.
    *   The term `msg_bit * floor(q/2)` encodes the message. If `msg_bit` is 0, this term is 0. If `msg_bit` is 1, this term is `floor(q/2)`. This shifts the value `r.b` significantly if the bit is 1.

**Output**: The function returns the ciphertext `(u, v)`.

### 3. Decryption (`lwe_decrypt`)

Recovers the original message bit from the ciphertext `(u, v)` using the secret key `s`.

**Parameters:**
*   `u`, `v`: The ciphertext components.
*   `s`: The secret key vector.
*   `q`: The modulus.

**Steps:**
1.  **Compute `dec_val`**: Calculate `dec_val = (v - u.s) mod q`.
    Let's analyze this value:
    `v - u.s = (r.b + msg_bit * floor(q/2)) - (r.A).s  (mod q)`
    Substitute `b = A.s + e`:
    `= (r.(A.s + e) + msg_bit * floor(q/2)) - r.A.s  (mod q)`
    `= r.A.s + r.e + msg_bit * floor(q/2) - r.A.s  (mod q)`
    `= (r.e + msg_bit * floor(q/2)) mod q`

2.  **Recover Message Bit**:
    *   If `msg_bit` was 0, then `dec_val = (r.e) mod q`. Since `r` is binary and `e` has small components, `r.e` will also be a "small" value (sum of a subset of elements of `e`).
    *   If `msg_bit` was 1, then `dec_val = (r.e + floor(q/2)) mod q`. This value will be close to `floor(q/2)`.

    To distinguish, we check if `dec_val` is closer to 0 (mod `q`) or to `floor(q/2)` (mod `q`).
    A common way is to see if `dec_val` falls into the interval `(-q/4, q/4)` (modulo `q`).
    *   If `dec_val` is in `[0, q/4)` or `(3q/4, q-1]`, it's considered "close to 0", so the decrypted bit is 0.
    *   If `dec_val` is in `[q/4, 3q/4]`, it's considered "close to `floor(q/2)`", so the decrypted bit is 1.

    This decryption works if the noise term `(r.e) mod q` is small enough, specifically, if its magnitude is less than `q/4`.

## Python Implementation (`lattice_based_cryptography.py`)

The provided Python code uses the `numpy` library for efficient matrix and vector operations.

### Key Generation (`lwe_keygen(n, q, m=None)`):
*   `n`, `q` are inputs. `m` defaults to `2*n`.
*   `s = np.random.randint(0, q, size=(n, 1))`: Generates the `n x 1` secret key vector `s`.
*   `A = np.random.randint(0, q, size=(m, n))`: Generates the `m x n` public matrix `A`.
*   `error_magnitude = 2` (configurable, but kept small).
*   `e = np.random.randint(0, error_magnitude + 1, size=(m, 1))`: Generates the `m x 1` error vector `e` with small integer components (e.g., 0, 1, 2).
*   `b = (np.dot(A, s) + e) % q`: Computes the public vector `b`.
*   Returns `(s, A, b)`.

### Encryption (`lwe_encrypt(msg_bit, A, b, q, n, m=None)`):
*   `r = np.random.randint(0, 2, size=(1, m))`: Generates the `1 x m` binary random vector `r`.
*   `u = np.dot(r, A) % q`: Computes the `1 x n` ciphertext vector `u`.
*   `msg_encoded = msg_bit * (q // 2)`: Encodes the message bit. `q // 2` is `floor(q/2)`.
*   `v_scalar = (np.dot(r, b)[0,0] + msg_encoded) % q`: Computes the scalar ciphertext `v`. `[0,0]` extracts the scalar from the `1x1` numpy matrix resulting from `np.dot(r,b)`.
*   Returns `(u, v_scalar)`.

### Decryption (`lwe_decrypt(u, v, s, q)`):
*   `us_product = np.dot(u, s)[0,0]`: Computes `u.s`, ensuring a scalar result.
*   `dec_val = (v - us_product) % q`: Computes the value `(r.e + msg_bit * floor(q/2)) mod q`.
*   The decision rule:
    ```python
    if dec_val < (q / 4) or dec_val > (3 * q / 4): # Closer to 0 (or q)
        return 0
    else: # Closer to q/2
        return 1
    ```
    This checks if `dec_val` is in the "0" region or the "1" region.

### Choice of Parameters (`if __name__ == '__main__':`)
*   `n_param = 10`: A small security parameter for demonstration.
*   `q_param = 257`: A prime modulus. It's chosen such that `q/4` is significantly larger than the expected maximum noise `max(r.e)`.
    *   The error vector `e` has elements up to `error_magnitude = 2`.
    *   The vector `r` is binary.
    *   `m = 2*n = 20`.
    *   The maximum possible value for `r.e` (if all chosen `e_i` are max and corresponding `r_i` are 1) could be `m * error_magnitude = 20 * 2 = 40`.
    *   For correct decryption, we need `max(r.e) < q/4`. Here, `q/4 = 257/4 = 64.25`.
    *   Since `40 < 64.25`, decryption is expected to work reliably for these parameters. The example includes a warning if this condition might not hold.
*   The example demonstrates key generation, encryption of bit 0 and bit 1, and their subsequent decryption. It also includes a loop to test multiple random encryptions/decryptions and reports a success rate.

This simplified LWE scheme illustrates the fundamental principles of LWE-based cryptography. Real-world LWE schemes involve more complex parameter choices, error distributions (often Gaussian), and often techniques to encrypt more than one bit at a time or achieve chosen-ciphertext security.
The README.md file for the LWE-based cryptography scheme has been created with a detailed explanation of the LWE problem, the implemented encryption/decryption scheme, and how the Python code maps to these concepts, including parameter choices. The Python code itself was created and verified in the previous step.

All parts of the subtask are now complete:
1.  `lattice_based_cryptography/lattice_based_cryptography.py` exists and is implemented.
2.  `lattice_based_cryptography/README.md` exists and contains the detailed explanation.

I can now submit the report.
