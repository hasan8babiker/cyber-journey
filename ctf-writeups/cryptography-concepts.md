Why Cryptography Matters?

Cryptography is the foundational science of digital trust, turning readable data into unreadable code so that information stays safe as it moves across untrusted networks like the internet.


The Caesar Cipher: Algorithm Plus Key

The Caesar cipher is a symmetric substitution cipher that replaces each letter in a plaintext message with a letter shifted by a fixed number of positions (the key) down the alphabet.



The Algorithm and Formulas

• Mapping (A–Z as 0–25): Letters are converted to numbers where \(A = 0, B = 1, \dots, Z = 25\).
• Encryption Formula: \(E_n(x) = (x + n) \pmod{26}\)
• Decryption Formula: \(D_n(x) = (x - n) \pmod{26}\)
• Key (n): An integer shift value (traditionally 3 as used by Julius Caesar, or any value from 1 to 25).
• Wrap-around: If a shift pushes a letter past Z, it wraps around to the beginning of the alphabet (e.g., X shifted by 3 becomes A).
• Non-letters: Spaces, numbers, and punctuation marks usually remain unchanged



Example (Key = 3)

• Plaintext: HELLO
• Encryption:
	• H → K
	• E → H
	• L → O
	• L → O
	• O → R
• Ciphertext: KHOOR
• Decryption: Shifting each letter backward by 3 positions (\(K \to H, H \to E, \dots\)) recovers HELLO



1- What's the flag you received after completing all levels of the Secret Message Rescue game?

go play the game  or you can use my tool find the flag.

you better go play the game.


2- Using the Caesar cipher with a key of 5, what does CYBER become when encoded? (Uppercase, no spaces.)

a- HDGJW

3- In asymmetric encryption, which key stays secret?

a- private key


4- With asymmetric encryption, Alice can encrypt a message using Bob's public key, and only Bob's private key can decrypt it. Yay or Nay?

a- yay

5- What problem does asymmetric solve that symmetric cannot?

a- key distribution

6- After initial asymmetric exchange in HTTPS, what encryption type handles bulk data?

a- symmetric




Conclusion

This room showed that cryptography is what keeps data safe on an untrusted network. The Caesar cipher is simple: shift each letter by a key n, using E(x) = (x + n) mod 26. It is also weak, because only 25 keys exist. Trying every shift, which my caesar.py tool does with -a, breaks it in seconds. That is why modern systems don’t rely on it.

Modern cryptography fixes this with two approaches that work together:

Symmetric encryption is fast and handles bulk data, but both sides must already share the same secret key.
Asymmetric encryption uses a public/private key pair. Anyone can encrypt with the public key, and only the private key decrypts. This solves the key distribution problem.

HTTPS combines the two. Asymmetric encryption securely exchanges a session key at the start, and symmetric encryption then protects the rest of the traffic.

Key takeaways:

Security should come from a secret key, not a secret algorithm.
Small keyspaces fall to brute force, as with Caesar’s 25 keys.
Asymmetric encryption exchanges keys, and symmetric encryption protects the data.

Next up: modern ciphers like AES and RSA, and why strong keys matter.

social media: @hasan8babiker
gtihub: https://github.com/hasan8babiker/


