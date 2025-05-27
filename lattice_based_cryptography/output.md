```text
 LWE Parameters: n=10, q=257, m=20
Max possible noise in r.e could be around m*error_mag = 20*2 = 40
Decryption requires noise < q/4 = 64.25
----------------------------------------
Secret key s (first 5 elements):
[[252 123  64  55 216]]
Public matrix A (first 5x5 block):
[[252 226  19 194 251]
 [229 104 193 106  49]
 [ 27 125 108  63 203]
 [208 117  61 197  90]
 [ 97 236 160 235  70]]
Public vector b (first 5 elements):
[[255 163 128 245 232]]
----------------------------------------
Encrypting message bit: 0
Ciphertext (u0, v0):
  u0 (first 5 elements): [ 83 243  42 217 135]
  v0: 252
--------------------
Encrypting message bit: 1
Ciphertext (u1, v1):
  u1 (first 5 elements): [127 240 209  70  82]
  v1: 190
----------------------------------------
Decrypting (u0, v0)... Result: 0
Original bit: 0, Decrypted bit: 0 -> Correct: True
--------------------
Decrypting (u1, v1)... Result: 1
Original bit: 1, Decrypted bit: 1 -> Correct: True
----------------------------------------
Running multiple encryption/decryption tests...
Success rate: 50/50 = 100.00%
```
