import os


def sorted_dict_by_key(d, decreasing=False):
    return sorted(d.items(), key=lambda x: x[0], reverse=decreasing)


def sorted_dict_by_value(d, decreasing=True):
    return sorted(d.items(), key=lambda x: x[1], reverse=decreasing)


def write_file(file_path, data):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, "w") as file:
        file.write(data)


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def write_benchmark(data, folder_path, algorithm_name, document_name):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(f"{folder_path}/b_{algorithm_name}_{document_name}.csv", "w") as f:
        for d in data:
            f.write(";".join(map(str, d)) + "\n")


def read_benchmark(folder_path, algorithm_name, document_name):
    counts_data = []
    with open(f"{folder_path}/b_{algorithm_name}_{document_name}.csv", "r") as f:
        found_counts = False
        for line in f:
            # Skip to counts
            if not line.startswith("token") and not found_counts:
                continue
            elif line.startswith("token"):
                found_counts = True
            # Read counts
            counts_data.append(line.strip().split(";"))
    # Transform counts to dictionary
    counts_by_lang = {}
    languages = [lang for lang in counts_data[0][1:]]
    for i, lang in enumerate(languages):
        counts_by_lang[lang] = {}
        for row in counts_data[1:]:
            if int(row[i + 1]) > 0:  # Skip zero counts
                counts_by_lang[lang][row[0]] = int(row[i + 1])
        counts_by_lang[lang] = sorted_dict_by_value(counts_by_lang[lang])
    return counts_by_lang
