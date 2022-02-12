#!/usr/bin/env python3
import random
import string


def generate_uid(count=15):
    uid = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=count))
    return uid


if __name__ == "__main__":
    uid = generate_uid()
    print(f"UID: {uid}")
