# AES-128 Key Expansion

The Advanced Encryption Standard (AES) is a symmetric block cipher. Before encryption or decryption can occur, the initial cipher key needs to be expanded into a series of round keys. This process is called Key Expansion. For AES-128, the initial key is 128 bits (16 bytes), and it's expanded into 11 round keys, each also 128 bits.

The key schedule is generated as a sequence of 4-byte "words". A 128-bit key is 4 words. The full key schedule for AES-128 consists of 44 words (4 words per round key * 11 round keys).

## Key Expansion Algorithm Steps (AES-128)

Let `Nk` be the number of 4-byte words in the initial key. For AES-128, `Nk = 4`.
Let `Nr` be the number of rounds. For AES-128, `Nr = 10`. (This means 11 round keys, from Round Key 0 to Round Key 10).
The key schedule `w` is an array of 4-byte words, indexed from `0` to `4*(Nr+1) - 1`.

1.  **Initialization**:
    *   The first `Nk` words of the key schedule (`w[0]` to `w[Nk-1]`) are filled directly from the initial 128-bit cipher key.
    *   `w[0] = key_bytes[0..3]`
    *   `w[1] = key_bytes[4..7]`
    *   `w[2] = key_bytes[8..11]`
    *   `w[3] = key_bytes[12..15]`

2.  **Generating Subsequent Words**:
    *   The remaining words (`w[i]` for `i` from `Nk` to `4*(Nr+1) - 1`) are generated iteratively.
    *   For each word `w[i]`:
        a.  Start with a temporary 4-byte word, `temp = w[i-1]`.
        b.  **If `i` is a multiple of `Nk`**:
            i.  **`RotWord(temp)`**: Perform a circular left shift on the bytes of `temp`. If `temp = [b0, b1, b2, b3]`, then `RotWord(temp) = [b1, b2, b3, b0]`.
            ii. **`SubWord(temp)`**: Apply the AES S-box substitution to each of the 4 bytes in `temp`. Each byte is replaced by its corresponding value in the S-box table.
            iii.XOR `temp` with a **Round Constant (Rcon)**. The Rcon value depends on `i/Nk`. Specifically, `temp[0]` (the first byte of `temp`) is XORed with `Rcon[i/Nk]`. The Rcon array provides different values for each round, ensuring that round keys are unique. `Rcon[j]` is `[RC[j], 0, 0, 0]` where `RC[1]=1`, `RC[x] = 2 * RC[x-1]` in Galois Field GF(2^8).
        c.  **XOR Operation**: The new word `w[i]` is calculated as `w[i-Nk] XOR temp`.
            `w[i] = w[i-Nk] ^ temp`.

    *   **Note for other AES versions**: For AES-192 and AES-256, there's an additional step if `Nk > 6` and `i % Nk == 4`, where `SubWord` is applied to `temp`. This is not relevant for AES-128.

3.  **Round Keys**:
    *   The 11 round keys (each 16 bytes / 4 words) are then taken sequentially from the generated `w` array:
        *   Round Key 0: `w[0], w[1], w[2], w[3]`
        *   Round Key 1: `w[4], w[5], w[6], w[7]`
        *   ...
        *   Round Key 10: `w[40], w[41], w[42], w[43]`

## Core Components in Key Expansion

*   **S-box (Substitution Box)**: A fixed 16x16 lookup table that maps an 8-bit input to an 8-bit output. It provides non-linearity to the cipher. In `SubWord`, each byte of a word is replaced by its S-box equivalent.
*   **`RotWord` (Rotate Word)**: A simple cyclic permutation. A 4-byte word `[b0, b1, b2, b3]` becomes `[b1, b2, b3, b0]`. This operation introduces byte-level diffusion between words.
*   **`Rcon` (Round Constant)**: An array of pre-defined values used to break symmetry in the round keys. Each `Rcon[j]` is a 4-byte word, but for AES-128, only the first byte `RC[j]` is non-zero. `RC[j]` is derived by exponentiation of 2 in GF(2^8). Example: `Rcon[1] = [0x01, 0x00, 0x00, 0x00]`, `Rcon[2] = [0x02, 0x00, 0x00, 0x00]`, etc.

## Python Implementation (`aes_key_expansion.py`)

The provided Python code in `aes_key_expansion.py` implements the AES-128 key expansion:

### Constants:
*   `S_BOX`: A tuple representing the 256-byte S-box.
*   `RCON`: A tuple representing the round constants `RC[j]`. `RCON[0]` is unused, `RCON[1]` is `0x01`, `RCON[2]` is `0x02`, etc., up to `RCON[10]` for AES-128.

### Helper Functions:
*   **`sub_word(word)`**:
    *   Takes a 4-byte list `word`.
    *   Returns a new list where each byte is substituted using `S_BOX[byte]`.
    ```python
    # word = [b0, b1, b2, b3]
    # result = [S_BOX[b0], S_BOX[b1], S_BOX[b2], S_BOX[b3]]
    return [S_BOX[b] for b in word]
    ```

*   **`rot_word(word)`**:
    *   Takes a 4-byte list `word`.
    *   Returns a new list with bytes cyclically shifted left: `[b1, b2, b3, b0]`.
    ```python
    # word = [b0, b1, b2, b3]
    # result = [b1, b2, b3, b0]
    return word[1:] + word[:1]
    ```

### Main Function: `aes128_key_expansion(key_bytes)`
*   Takes `key_bytes` (a list of 16 integers representing the initial 128-bit key).
*   Initializes `Nk = 4` (words in key) and `Nr = 10` (rounds).
*   Creates `w`, a list of lists, to store the `4 * (Nr + 1) = 44` words.
*   **Initialization (First `Nk` words)**:
    ```python
    for i in range(Nk): # 0, 1, 2, 3
        w[i] = [key_bytes[4*i], key_bytes[4*i+1], key_bytes[4*i+2], key_bytes[4*i+3]]
    ```
*   **Generating Subsequent Words (`Nk` to `43`)**:
    ```python
    for i in range(Nk, 4 * (Nr + 1)): # 4 to 43
        temp = list(w[i-1]) # Copy previous word

        if i % Nk == 0: # If i is a multiple of Nk (4, 8, 12, ...)
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp[0] = temp[0] ^ RCON[i // Nk] # XOR first byte of temp with RCON value

        # For AES-128, no 'else if' part for Nk > 6 and i % Nk == 4 is needed.
        
        # XOR temp with the word Nk positions earlier to get the new word w[i]
        for j in range(4): # For each byte in the word
            w[i][j] = w[i-Nk][j] ^ temp[j]
    return w
    ```
*   The function returns the list `w` containing all 44 generated words.

### Example Usage and Formatting:
*   The `if __name__ == '__main__':` block demonstrates how to use `aes128_key_expansion` with an example key from FIPS-197.
*   `format_key_schedule(schedule_words)` is a helper to group the 44 words into 11 round keys (each 16 bytes) for easier display and verification.
*   Selected words from the generated schedule are printed and compared against expected values from the FIPS-197 standard to verify correctness.

This implementation directly follows the AES-128 key expansion specification, generating the necessary round keys for the AES encryption/decryption process.
The README.md file for AES Key Expansion has been created with a detailed explanation of the algorithm and its Python implementation. The Python code itself was created and verified in the previous step.

All parts of the subtask are now complete:
1.  `aes_key_expansion/aes_key_expansion.py` exists and is implemented.
2.  `aes_key_expansion/README.md` exists and contains the detailed explanation.

I can now submit the report.
