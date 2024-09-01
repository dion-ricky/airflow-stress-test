import random
from uuid import UUID


def rand_id(seed):
    rd = random.Random()
    rd.seed(seed)
    return UUID(int=rd.getrandbits(128), version=4).hex

def rand_num(seed, min, max):
    rd = random.Random()
    rd.seed(seed)
    return rd.randrange(min, max)