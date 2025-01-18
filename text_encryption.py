from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA, DSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Signature import DSS
from Cryptodome.Hash import SHA256
import base64

banner="""                                                                              
 @@@@@@@  @@@@@@@   @@@ @@@  @@@@@@@   @@@@@@@  @@@@@@@    @@@@@@   @@@  @@@  
@@@@@@@@  @@@@@@@@  @@@ @@@  @@@@@@@@  @@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@  
!@@       @@!  @@@  @@! !@@  @@!  @@@    @@!    @@!  @@@  @@!  @@@  @@!  !@@  
!@!       !@!  @!@  !@! @!!  !@!  @!@    !@!    !@   @!@  !@!  @!@  !@!  @!!  
!@!       @!@!!@!    !@!@!   @!@@!@!     @!!    @!@!@!@   @!@  !@!   !@@!@!   
!!!       !!@!@!      @!!!   !!@!!!      !!!    !!!@!!!!  !@!  !!!    @!!!    
:!!       !!: :!!     !!:    !!:         !!:    !!:  !!!  !!:  !!!   !: :!!   
:!:       :!:  !:!    :!:    :!:         :!:    :!:  !:!  :!:  !:!  :!:  !:!  
 ::: :::  ::   :::     ::     ::          ::     :: ::::  ::::: ::   ::  :::  
 :: :: :   :   : :     :      :           :     :: : ::    : :  :    :   ::   
 
"""

# AES Encryption and Decryption
def aes_encrypt_decrypt(text):
    print("\n--- AES Encryption/Decryption ---")
    key = get_random_bytes(16)  # AES key (128-bit)
    cipher = AES.new(key, AES.MODE_EAX)  # AES in EAX mode
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))

    print(f"Original Text: {text}")
    print(f"Ciphertext (AES): {base64.b64encode(ciphertext).decode()}")
    print(f"AES Key (Keep Safe): {base64.b64encode(key).decode()}")

    # Decrypt
    decipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_text = decipher.decrypt(ciphertext).decode('utf-8')
    print(f"Decrypted Text: {decrypted_text}")


# RSA Encryption and Decryption
def rsa_encrypt_decrypt(text):
    print("\n--- RSA Encryption/Decryption ---")
    key = RSA.generate(2048)
    public_key = key.publickey()

    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(text.encode('utf-8'))
    print(f"Original Text: {text}")
    print(f"Ciphertext (RSA): {base64.b64encode(ciphertext).decode()}")

    # Decrypt
    decipher = PKCS1_OAEP.new(key)
    decrypted_text = decipher.decrypt(ciphertext).decode('utf-8')
    print(f"Decrypted Text: {decrypted_text}")


# DSA Signing and Verification
def dsa_sign_verify(message):
    print("\n--- DSA Signing/Verification ---")
    # Generate a new DSA key pair
    key = DSA.generate(2048)

    # Create a hash of the message
    h = SHA256.new(message)

    # Create a DSS signer using the DSA key
    signer = DSS.new(key, 'fips-186-3')

    # Sign the hash
    signature = signer.sign(h)
    print(f"Signature: {base64.b64encode(signature).decode()}")  # Encode signature for readability

    # Create a DSS verifier using the public key
    verifier = DSS.new(key.public_key(), 'fips-186-3')

    try:
        # Verify the signature
        verifier.verify(h, signature)
        print("Signature is valid.")
    except ValueError:
        print("Signature is invalid.")

#print banner
print(banner)
# Input Text
text_to_encrypt = input("Enter text to perform encryption and signing: ")

# Perform encryption and signing
aes_encrypt_decrypt(text_to_encrypt)
rsa_encrypt_decrypt(text_to_encrypt)
dsa_sign_verify(text_to_encrypt.encode('utf-8'))  # Pass message in bytes format
