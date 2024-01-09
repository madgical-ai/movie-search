import base64

# key = "ZKG0I3WBM9V5U1OA8TXS"
key = "JD2egWojhFxYnK8AqH3PGUrX0C7ltZ94SLmwM/vB"

# Encode the key using base64
encoded_key = base64.b64encode(key.encode("utf-8")).decode("utf-8")

print("Encoded Key:", encoded_key)
