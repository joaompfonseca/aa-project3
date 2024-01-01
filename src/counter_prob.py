import math as m
import random as r
import utils as u


def counter_prob(data, prob=1 / 16, seed=r.random()):
    r.seed(seed)
    counts = {}
    for token in data:
        if r.random() > prob:
            continue  # Skip this token
        if token not in counts:
            counts[token] = 1
        counts[token] += 1
    for token in counts:
        counts[token] = m.floor(counts[token] / prob)
    return counts


if __name__ == "__main__":
    data = u.read_file("../documents/proc/othello/pg1793.txt")
    res = counter_prob(data, seed=103154)
    print(u.sorted_dict_by_value(res))
