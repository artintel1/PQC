# Playfair Cipher

The Playfair cipher is a manual symmetric encryption technique and was the first literal digraph substitution cipher. It encrypts pairs of letters (digraphs), instead of single letters as in simpler substitution ciphers.

## Algorithm Steps

The Playfair cipher involves several stages: key generation, plaintext preparation, encryption, and decryption.

### 1. Key Matrix Generation

A 5x5 matrix of letters is generated based on a keyword.

1.  **Prepare the Key**:
    *   Convert the keyword to uppercase.
    *   Remove any duplicate letters from the keyword.
    *   The letter 'J' is typically combined with 'I' (or 'Q' with 'Z', but 'I'/'J' is more common) to fit the 26 letters of the alphabet into 25 spaces (5x5). In our implementation, 'J' is replaced by 'I'.

2.  **Populate the Matrix**:
    *   Fill the unique letters of the prepared keyword into the matrix from left to right, top to bottom.
    *   Then, fill the remaining spaces in the matrix with the rest of the letters of the alphabet in order (excluding 'J' if it's merged with 'I', and any letters already used from the key).

**Example Key Matrix (Key: "PLAYFAIR EXAMPLE")**
P L A Y F
I R E X M
B C D G H
K N O Q S
T U V W Z

(Note: 'J' is treated as 'I'. The alphabet used is A-Z excluding J)

### 2. Plaintext Preparation

The plaintext must be processed before encryption:

1.  **Convert to Uppercase**: Make the entire plaintext uppercase.
2.  **Replace 'J' with 'I'**: Consistent with the key matrix.
3.  **Remove Non-Alphabetic Characters**: Spaces, numbers, punctuation, etc., are removed.
4.  **Form Digraphs (Pairs of Letters)**:
    *   Group the letters into pairs.
    *   **Rule for Identical Letters**: If a pair consists of two identical letters (e.g., "LL"), insert a filler letter (commonly 'X') between them. So, "HELLO" becomes "HE LX LO".
    *   **Rule for Odd Length**: If the plaintext has an odd number of letters after the previous steps, append a filler letter (e.g., 'X') to the end to make it even. So "HELXLO" becomes "HE LX LO XZ" if Z is chosen (our code uses 'X' by default).

**Example Plaintext Preparation (Plaintext: "Hide the gold in the tree stump", Filler: 'X')**
Original: `HIDE THE GOLD IN THE TREE STUMP`
Processed: `HIDETHEGOLDINTHETREESTUMP`
Replace J with I: (No 'J' in this example)
Digraphs:
HI DE TH EG OL DI NT HE TR EX ES TU MP (Note: "EE" in "TREE" becomes "EX E")
If the text was "BALLOON", it would become "BA LX LO ON". (LL -> LX L, then append X if still odd, so BA LX LO OX NX)
Our `prepare_plaintext` function handles this to output a list of digraph strings: `['HI', 'DE', 'TH', 'EG', 'OL', 'DI', 'NT', 'HE', 'TR', 'EX', 'ES', 'TU', 'MP']`

### 3. Encryption Rules

Encryption is performed on the prepared digraphs using the key matrix:

1.  **Locate Letters in Matrix**: For each digraph, find the positions (row and column) of its two letters in the key matrix.
2.  **Apply Rules based on Positions**:
    *   **Rule 1: Letters in the Same Row**:
        *   Replace each letter with the letter to its immediate right in the matrix.
        *   If a letter is in the rightmost column, wrap around to the leftmost column of the same row.
        *   Example: If matrix has `P L A Y F` and digraph is `PL`, it becomes `LA`. If digraph is `FP`, it becomes `PL`.
    *   **Rule 2: Letters in the Same Column**:
        *   Replace each letter with the letter immediately below it in the matrix.
        *   If a letter is in the bottommost row, wrap around to the topmost row of the same column.
        *   Example: If matrix has `P`, `I`, `B`, `K`, `T` in the first column and digraph is `PI`, it becomes `IB`. If digraph is `TP`, it becomes `PI`.
    *   **Rule 3: Letters form a Rectangle**:
        *   If the two letters are in different rows and different columns, they form a rectangle.
        *   Replace each letter with the letter that is in its same row but in the column of the other letter.
        *   Example: Digraph `HI`. If `H` is at (row2, col4) and `I` is at (row1, col0). The encrypted letters would be at (row2, col0) and (row1, col4).

**Example Encryption (Digraph: "HI", Key Matrix from "PLAYFAIR EXAMPLE")**
H is at (2,4), I is at (1,0)
P L A Y F
I R E X M  <- I is here (1,0)
B C D G H  <- H is here (2,4)
K N O Q S
T U V W Z

They form a rectangle.
Letter 1 (`H`): Same row (2), column of `I` (0) -> `B`
Letter 2 (`I`): Same row (1), column of `H` (4) -> `M`
So, "HI" encrypts to "BM".

### 4. Decryption Rules

Decryption is the reverse of encryption, using the same key matrix:

1.  **Locate Letters in Matrix**: For each ciphertext digraph, find the positions of its two letters.
2.  **Apply Inverse Rules**:
    *   **Rule 1: Letters in the Same Row**:
        *   Replace each letter with the letter to its immediate **left**.
        *   If a letter is in the leftmost column, wrap around to the rightmost column.
    *   **Rule 2: Letters in the Same Column**:
        *   Replace each letter with the letter immediately **above** it.
        *   If a letter is in the topmost row, wrap around to the bottommost row.
    *   **Rule 3: Letters form a Rectangle**:
        *   This rule is the same as for encryption: Replace each letter with the letter that is in its same row but in the column of the other letter. (This rule is symmetric).

After decryption, the resulting plaintext may contain filler letters (e.g., 'X') and will have 'I' for any original 'J's. These usually need to be manually or heuristically processed to get the final readable message.

## Python Implementation (`playfair_cipher.py`)

The provided Python code implements the Playfair cipher with the following key functions:

### `generate_key_matrix(key)`
*   Takes a `key` string as input.
*   Converts the key to uppercase.
*   Replaces all occurrences of 'J' with 'I'.
*   Builds a list of unique characters from the key, followed by the remaining letters of the alphabet (A-Z, excluding J).
*   Constructs and returns a 5x5 list of lists (the key matrix).
    ```python
    # Simplified snippet
    key_letters = [] # Unique letters from key + rest of alphabet (no J)
    # ... logic to populate key_letters ...
    matrix = []
    for i in range(5):
        row = []
        for j in range(5):
            row.append(key_letters[i * 5 + j])
        matrix.append(row)
    return matrix
    ```

### `prepare_plaintext(text, filler='X')`
*   Takes the `text` string and an optional `filler` character (default 'X').
*   Converts text to uppercase, replaces 'J' with 'I', and removes non-alphabetic characters.
*   Iterates through the text to form digraphs:
    *   If `text[i] == text[i+1]`, it appends `text[i]` and `filler`.
    *   Otherwise, it appends `text[i]` and `text[i+1]`.
    *   If there's a single character left at the end, it appends that character and `filler`.
*   Returns a list of 2-character strings (digraphs).
    ```python
    # Simplified snippet
    # ... text cleaning ...
    prepared_text_chars = []
    i = 0
    while i < len(text):
        char1 = text[i]
        if i + 1 < len(text): # There is a next character
            char2 = text[i+1]
            if char1 == char2: # Same characters
                prepared_text_chars.extend([char1, filler])
                i += 1
            else: # Different characters
                prepared_text_chars.extend([char1, char2])
                i += 2
        else: # Last character, needs padding
            prepared_text_chars.extend([char1, filler])
            i += 1
    # Convert list of chars to list of digraph strings
    digraphs = [ "".join(prepared_text_chars[k:k+2]) for k in range(0, len(prepared_text_chars), 2)]
    return digraphs
    ```

### `find_char_coords(matrix, char)`
*   A helper function that takes the `matrix` and a `char`.
*   Returns the `(row, column)` tuple for the character in the matrix.

### `playfair_transform(matrix, digraph, encrypt=True)`
*   This function encapsulates the core Playfair rules for a single `digraph`.
*   It takes the `matrix`, `digraph` string, and a boolean `encrypt` (True for encryption, False for decryption).
*   It calls `find_char_coords` for both characters in the digraph.
*   Implements the three rules:
    *   **Same Row**: `col_shift = 1` for encrypt, `-1` for decrypt. New columns are `(col + col_shift) % 5`.
    *   **Same Column**: `row_shift = 1` for encrypt, `-1` for decrypt. New rows are `(row + row_shift) % 5`.
    *   **Rectangle**: Swaps the column indices: `matrix[r1][c2]` and `matrix[r2][c1]`.
*   Returns the transformed 2-character string.

### `encrypt(plaintext, key)`
*   Generates the `key_matrix` using `generate_key_matrix(key)`.
*   Prepares the `plaintext` into digraphs using `prepare_plaintext(plaintext)`.
*   Iterates through each `digraph` and calls `playfair_transform` with `encrypt=True`.
*   Concatenates the results to form the final ciphertext string.

### `decrypt(ciphertext, key)`
*   Generates the `key_matrix`.
*   Splits the `ciphertext` string into a list of 2-character digraphs.
*   Iterates through each `digraph` and calls `playfair_transform` with `encrypt=False`.
*   Concatenates the results to form the plaintext string (which may include fillers).

### Example Usage (`if __name__ == '__main__':`)
The script includes examples demonstrating:
*   Key matrix generation.
*   Plaintext preparation.
*   Encryption of a sample text.
*   Decryption of the resulting ciphertext.
*   Tests for edge cases like repeating letters, odd length plaintext, and use of 'J'.
*   Verification against a known example (e.g., "INSTRUMENTS" with key "MONARCHY").

This structure allows for clear separation of concerns and implements the Playfair cipher as described.
The README.md file has been created with a detailed explanation of the Playfair cipher, including key generation, plaintext preparation, encryption/decryption rules, and how the Python code implements these aspects. The Python code itself was created and verified in the previous step.

All parts of the subtask are now complete. I can submit the report.
