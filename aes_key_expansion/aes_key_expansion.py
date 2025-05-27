# Python implementation of AES-128 Key Expansion

# S-box: A fixed substitution table used in SubWord
S_BOX = (
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
)

# Rcon: Round Constant array for key schedule
# Rcon[i] = [RC[i], 0, 0, 0] where RC[1]=1, RC[i]=2*RC[i-1] (in GF(2^8))
RCON = (
    0x00, # Rcon[0] - not used, placeholder for 1-based indexing in spec
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36 # Rcon[1] to Rcon[10]
    # For AES-128, we only need up to Rcon[10]
)

def sub_word(word):
    """Applies S-box substitution to each byte of a 4-byte word."""
    return [S_BOX[b] for b in word]

def rot_word(word):
    """Performs a circular left shift on a 4-byte word."""
    return word[1:] + word[:1]

def aes128_key_expansion(key_bytes):
    """
    Generates the AES-128 key schedule (11 round keys, each 16 bytes).
    The input key_bytes must be a list or tuple of 16 integers (bytes).
    Returns a list of 44 words (176 bytes). Each word is a list of 4 bytes.
    """
    if len(key_bytes) != 16:
        raise ValueError("AES-128 key must be 16 bytes (128 bits).")

    # Nk: Number of 32-bit words in the key. For AES-128, Nk = 4.
    Nk = 4
    # Nr: Number of rounds. For AES-128, Nr = 10. (So 11 round keys)
    Nr = 10

    # The key schedule words. Total words = Nk * (Nr + 1) = 4 * (10 + 1) = 44 words.
    # Each word is 4 bytes.
    w = [[0] * 4 for _ in range(4 * (Nr + 1))]

    # The first Nk words are filled directly from the cipher key.
    for i in range(Nk):
        w[i] = [key_bytes[4*i], key_bytes[4*i+1], key_bytes[4*i+2], key_bytes[4*i+3]]

    # Generate the remaining words
    for i in range(Nk, 4 * (Nr + 1)):
        temp = list(w[i-1]) # Make a copy for modification

        if i % Nk == 0:
            # Apply RotWord, SubWord, and XOR with Rcon
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp[0] = temp[0] ^ RCON[i // Nk]
        # For AES-256 (Nk=8), there's an additional SubWord if i % Nk == 4.
        # Not needed for AES-128.

        # XOR with the word Nk positions earlier
        if i == 29: # Specific debug for w[29]
            w_i_minus_nk = w[i-Nk]
            # temp is w[i-1] because 29 % Nk != 0
            # w[i-1] is w[28]
            print(f"DEBUG i=29: w[i-Nk] (w[25]) = {[f'{b:02x}' for b in w_i_minus_nk]}")
            print(f"DEBUG i=29: temp (w[28])      = {[f'{b:02x}' for b in temp]}")
            
            result_xor_word = [0,0,0,0]
            for byte_idx in range(4):
                result_xor_word[byte_idx] = w_i_minus_nk[byte_idx] ^ temp[byte_idx]
            print(f"DEBUG i=29: w[25]^w[28] result = {[f'{b:02x}' for b in result_xor_word]}")

        for j in range(4): # Iterate over bytes in the word
            w[i][j] = w[i-Nk][j] ^ temp[j]
            
    return w

def format_key_schedule(schedule_words):
    """Formats the key schedule for display."""
    formatted_schedule = []
    for i in range(0, len(schedule_words), 4):
        round_key_words = schedule_words[i:i+4]
        round_key_bytes = []
        for word in round_key_words:
            round_key_bytes.extend(word)
        formatted_schedule.append(round_key_bytes)
    return formatted_schedule


# Example Usage:
if __name__ == '__main__':
    # Example Key (16 bytes / 128 bits)
    # From NIST FIPS-197 Appendix A.1 (AES-128)
    # Key: 2b7e151628aed2a6abf7158809cf4f3c
    key_hex = "2b7e151628aed2a6abf7158809cf4f3c"
    key_bytes_example = [int(key_hex[i:i+2], 16) for i in range(0, len(key_hex), 2)]

    print(f"Original Key (hex): {key_hex}")
    print(f"Original Key (bytes): {[f'{b:02x}' for b in key_bytes_example]}")
    print("-" * 40)

    # Generate the key schedule
    key_schedule_words = aes128_key_expansion(key_bytes_example)
    
    # Print the key schedule words (44 words for AES-128)
    print("Generated Key Schedule (words w[0] to w[43]):")
    for idx, word_val in enumerate(key_schedule_words):
        print(f"w[{idx:02d}]: {[f'{b:02x}' for b in word_val]}")
    print("-" * 40)

    # For actual AES encryption, round keys are typically used as 16-byte blocks.
    # The key schedule `w` contains 11 such round keys for AES-128.
    # Round Key 0: w[0]w[1]w[2]w[3]
    # Round Key 1: w[4]w[5]w[6]w[7]
    # ...
    # Round Key 10: w[40]w[41]w[42]w[43]
    
    round_keys_bytes = format_key_schedule(key_schedule_words)
    print("Round Keys (11 keys, each 16 bytes):")
    for r_idx, r_key in enumerate(round_keys_bytes):
        print(f"Round Key {r_idx:02d}: {[f'{b:02x}' for b in r_key]}")
    
    # Verification against FIPS-197 Appendix A.1 (Selected words)
    # w[0-3] should be the original key
    print("-" * 40)
    print("Verification (selected words from FIPS-197 A.1):")
    print(f"w[00]: {[f'{b:02x}' for b in key_schedule_words[0]]}  (Expected: 2b 7e 15 16)")
    print(f"w[03]: {[f'{b:02x}' for b in key_schedule_words[3]]}  (Expected: 09 cf 4f 3c)")
    
    # After first full application of core (for w[4])
    # temp = RotWord(w[3]) = [cf, 4f, 3c, 09]
    # temp = SubWord(temp) = [8a, 84, eb, 01] (Using S-Box values for cf, 4f, 3c, 09)
    # Rcon[1] = [01, 00, 00, 00]
    # temp[0] = temp[0] ^ Rcon[1][0] = 8a ^ 01 = 8b
    # So, temp becomes [8b, 84, eb, 01]
    # w[4] = w[0] ^ temp = [2b,7e,15,16] ^ [8b,84,eb,01] = [a0,fa,fe,17]
    print(f"w[04]: {[f'{b:02x}' for b in key_schedule_words[4]]}  (Expected: a0 fa fe 17)")
    print(f"w[07]: {[f'{b:02x}' for b in key_schedule_words[7]]}  (Expected: 56 50 e3 d8)")
    print(f"w[36]: {[f'{b:02x}' for b in key_schedule_words[36]]} (Expected: d0 14 f9 a8)") # Start of Round Key 9
    print(f"w[39]: {[f'{b:02x}' for b in key_schedule_words[39]]} (Expected: c6 7c 37 96)") # End of Round Key 9
    print(f"w[40]: {[f'{b:02x}' for b in key_schedule_words[40]]} (Expected: 4d 3c 69 5a)") # Start of Round Key 10
    print(f"w[43]: {[f'{b:02x}' for b in key_schedule_words[43]]} (Expected: 80 fb eb 23)") # End of Round Key 10
