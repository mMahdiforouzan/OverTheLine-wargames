##this is a script for level 11 of the natas game
import base64

# change the cookie if it has changed
cookie = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg="

# decrypt cookie to be XORed with the default data to get the key
decryptedCookie = base64.b64decode(cookie)

# the default data from the sourcecode. In bits since we need it for XOR operation
defaultData = b'{"showpassword":"no","bgcolor":"#ffffff"}'

# We can get the key using a plaintext of the data and the encrypted ciphertext since XOR is transitive
xorOut = bytes(
    [decryptedCookie[x] ^ defaultData[x] for x in range(len(decryptedCookie))]
)

print("The key used was: ", xorOut)




# The actual key used to do the XOR operation was shorter than the plaintext so it was repeated multiple times to compensate.
def findKey():
    for x in range(len(xorOut) - 1):
        if x != 0 and x <= len(xorOut) - 1 / 2 and xorOut[:x] == xorOut[x : 2 * x]:
            return xorOut[:x]
        elif (
            x != 0
            and x > len(xorOut) - 1 / 2
            and xorOut[:x] == xorOut[x:0] + xorOut[0 : len(xorOut) - x]
        ):
            return xorOut[:x]
    return xorOut

#the key used in XOR encryption
key = findKey()

print("the actual key used (before being repeated): ",key)

#the plaintext of the cookie we need to send
PlainNewCookie=b'{"showpassword":"yes","bgcolor":"#ffffff"}'

#the encrypted version using the same method as the website
encryptedNewCookie = bytes(
    [PlainNewCookie[x] ^ key[x%len(key)] for x in range(len(PlainNewCookie))]
)

#the cookie we need to send
Base64NewCookie = base64.b64encode(encryptedNewCookie)

print("the new cookie is (copy what's inside the  ' symbols): ",Base64NewCookie)
