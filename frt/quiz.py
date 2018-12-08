# Solution to quiz 1
message = [104, 116, 116, 112, 115, 58, 47, 47, 101, 110, 103, 105, 110, 101, 101, 114, 105, 110, 103, 45, 97, 112, 112, 108, 105, 99, 97, 116, 105, 111, 110, 46, 98, 114, 105, 116, 101, 99, 111, 114, 101, 46, 99, 111, 109, 47, 113, 117, 105, 122, 47, 105, 112, 108, 115, 106, 102, 107, 102, 107, 114, 111, 100, 115, 101, 101, 103, 103]
deciphered_message = "".join(chr(i) for i in message)
print(deciphered_message)

# Solution to quiz 2
try:
    # This module needs to be installed
    from cryptography.fernet import Fernet
    key = "TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM="

    # Oh no! The code is going over the edge! What are you going to do?
    message = b"gAAAAABb4PJ70ZmPtrXx0Sam51h_buFiYWa51HEPel2YOrZQnIZv6UACyQBb6IS6l4YPOSLFs06XR3iwBAuTJUGR3VicZP33gkl0E7IKcElT0k94LGvjH8BqyVhpYTLZgAUg_FW4ayjMF9iBJAOp00T6MDtHRAaIW7dTYzYWvghkyzitzD7QMYn3nZCanWVhMh1L14hdtckQ"


    def main():
        f = Fernet(key)
        decrypted_message = f.decrypt(message).decode('UTF-8')
        print(decrypted_message)


    if __name__ == "__main__":
        main()
except ImportError as error:
    print('Error: Install cryptography module')
    print('Run pip install cryptography')
