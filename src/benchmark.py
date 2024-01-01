import math as m
import time
import counter_exact as ce
import counter_prob as cp
import counter_space as cs
import utils as u

DOCS = {
    "othello": {
        "source": "../documents/proc/othello",
        "files": {
            "de": "pg7185.txt",
            "en": "pg1793.txt",
            "fi": "pg17529.txt",
            "fr": "pg18179.txt",
            "pt": "pg28526.txt",
        },
    }
}

CP_P = 1 / 16  # Probabilistic Counter probability
CP_N = 10  # Probabilistic Counter number of runs
CS_K = [3, 5, 10]  # Space Saving Counter k values


def benchmark(algorithm, data, **kwargs):
    """
    Benchmark the given algorithm on the given data.
    """
    ts = time.time()
    res = algorithm(data, **kwargs)
    te = time.time()
    return res, te - ts


if __name__ == "__main__":
    stats_header = ["lang", "time_taken"]
    counts_header = ["token"] # Languages are appended later
    
    exact_stats = {} # Language: time_taken
    exact_counts = {} # Language: {token: count}
    
    prob_stats = {} # Language: time_taken
    prob_counts = {} # Language: {token: count}
    
    space_stats = {} # Language: time_taken
    space_counts = {} # Language: {token: count}

    for doc in DOCS:
        for lang, file_name in DOCS[doc]["files"].items():
            data = u.read_file(f"{DOCS[doc]['source']}/{file_name}")
            counts_header += [lang]

            # Exact Counter
            ce_counts, ce_time_taken = benchmark(ce.counter_exact, data)
            exact_stats[lang] = ce_time_taken
            exact_counts[lang] = ce_counts
            
            # Probabilistic Counter
            cp_avg_counts = {}
            cp_time_taken = 0
            for _ in range(CP_N):
                cp_counts, cp_time_taken = benchmark(cp.counter_prob, data, prob=CP_P)
                for cp_token, cp_count in cp_counts.items():
                    if cp_token not in cp_avg_counts:
                        cp_avg_counts[cp_token] = 0
                    cp_avg_counts[cp_token] += cp_count
            for cp_token in cp_avg_counts:
                cp_avg_counts[cp_token] = m.floor(cp_avg_counts[cp_token] / CP_N)
                
            prob_stats[lang] = cp_time_taken
            prob_counts[lang] = cp_avg_counts
            
            # Space Saving Counter
            for k in CS_K:
                cs_counts, cs_time_taken = benchmark(cs.counter_space, data, k=k)
                if k not in space_stats:
                    space_stats[k] = {}
                    space_counts[k] = {}
                space_stats[k][lang] = cs_time_taken
                space_counts[k][lang] = cs_counts
            
    # Exact Counter
    stats_data = [[lang, time_taken] for lang, time_taken in u.sorted_dict_by_key(exact_stats)]
    counts_data = []
    all_tokens = set([token for lang in exact_counts for token in exact_counts[lang]]) 
    for token in sorted(all_tokens):
        counts_data_entry = [token]
        for lang in exact_counts:
            if token in exact_counts[lang]:
                counts_data_entry += [exact_counts[lang][token]]
            else:
                counts_data_entry += [0]
        counts_data += [counts_data_entry]
    u.write_benchmark(
        data=[
            stats_header,
            *stats_data,
            counts_header,
            *counts_data,
        ],
        folder_path="../benchmarks",
        algorithm_name="ce",
        document_name=doc,
    )
    

    # Probabilistic Counter
    stats_data = [[lang, time_taken] for lang, time_taken in u.sorted_dict_by_key(prob_stats)]
    counts_data = []
    all_tokens = set([token for lang in prob_counts for token in prob_counts[lang]]) 
    for token in sorted(all_tokens):
        counts_data_entry = [token]
        for lang in prob_counts:
            if token in prob_counts[lang]:
                counts_data_entry += [prob_counts[lang][token]]
            else:
                counts_data_entry += [0]
        counts_data += [counts_data_entry]
    u.write_benchmark(
        data=[
            stats_header,
            *stats_data,
            counts_header,
            *counts_data,
        ],
        folder_path="../benchmarks",
        algorithm_name="cp",
        document_name=doc,
    )

    # Space Saving Counter
    for k in CS_K:
        stats_data = [[lang, time_taken] for lang, time_taken in u.sorted_dict_by_key(space_stats[k])]
        counts_data = []
        all_tokens = set([token for lang in space_counts[k] for token in space_counts[k][lang]]) 
        for token in sorted(all_tokens):
            counts_data_entry = [token]
            for lang in space_counts[k]:
                if token in space_counts[k][lang]:
                    counts_data_entry += [space_counts[k][lang][token]]
                else:
                    counts_data_entry += [0]
            counts_data += [counts_data_entry]
        u.write_benchmark(
            data=[
                stats_header,
                *stats_data,
                counts_header,
                *counts_data,
            ],
            folder_path="../benchmarks",
            algorithm_name=f"cs-k{k}",
            document_name=doc,
        )
