import random

def generate_secret_santa(participantsName):
    names = [p["name"] for p in participantsName]
    receivers = names[:]

    # Intentar hasta que nadie se regale a sí mismo
    while True:
        random.shuffle(receivers)
        if all(giver != receiver for giver, receiver in zip(names, receivers)):
            break

    return {giver: receiver for giver, receiver in zip(names, receivers)}
