import utils as u

def counter_exact(data):
    counts = {}
    for token in data:
        if token not in counts:
            counts[token] = 1
        counts[token] += 1
    return counts


if __name__ == "__main__":
    data = u.read_file("../documents/proc/othello/pg1793.txt")
    res = counter_exact(data)
    print(u.sorted_dict_by_value(res))
