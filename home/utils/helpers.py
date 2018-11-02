import random
import string


def random_password():
    chars = string.letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for i in range(random.randint(12, 16)))
