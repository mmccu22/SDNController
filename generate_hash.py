import hashlib

student_id = "897263492"
secret = "NeoDDaBRgX5a9"

data = student_id + secret
hash_object = hashlib.sha256(data.encode())
hash_hex = hash_object.hexdigest()

print("SHA-256 Hash:", hash_hex)
