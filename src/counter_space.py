import utils as u


def counter_space(data, k=10):
    counts = {}
    for token in data:
        if token in counts:
            counts[token] += 1
        elif len(counts) < k:
            counts[token] = 1
        else:
            min_token = min(counts, key=counts.get)
            counts[token] = counts[min_token] + 1
            counts.pop(min_token)
    return counts


if __name__ == "__main__":
    data = u.read_file("../documents/proc/othello/pg1793.txt")
    res = counter_space(data)
    print(u.sorted_dict_by_value(res))
