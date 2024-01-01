import utils as u

TOP = 10

if __name__ == "__main__":
    exact_counts = u.read_benchmark("../benchmarks", "ce", "othello")
    prob_counts = u.read_benchmark("../benchmarks", "cp", "othello")
    space_counts = u.read_benchmark(
        "../benchmarks", "cs-k10", "othello"
    )  # Consider k=10

    for lang in exact_counts:
        print()

        print(f"### Language: {lang}")

        print()
        
        # Sort by count / value
        
        exact_counts[lang].sort(key=lambda x: x[1], reverse=True)
        prob_counts[lang].sort(key=lambda x: x[1], reverse=True)
        space_counts[lang].sort(key=lambda x: x[1], reverse=True)
        
        print(f"--- Top {TOP} results")
        print("Exact:")
        print(exact_counts[lang][:TOP])
        print("Prob:")
        print(prob_counts[lang][:TOP])
        print("Space:")
        print(space_counts[lang][:TOP])

        print()

        print("--- Counter Values")
        print("Exact:")
        print("Max:", max([x[1] for x in exact_counts[lang]]))
        print("Min:", min([x[1] for x in exact_counts[lang]]))
        print("Avg:", sum([x[1] for x in exact_counts[lang]]) / len(exact_counts[lang]))
        print("Prob:")
        print("Max:", max([x[1] for x in prob_counts[lang]]))
        print("Min:", min([x[1] for x in prob_counts[lang]]))
        print("Avg:", sum([x[1] for x in prob_counts[lang]]) / len(prob_counts[lang]))
        print("Space:")
        print("Max:", max([x[1] for x in space_counts[lang]]))
        print("Min:", min([x[1] for x in space_counts[lang]]))
        print("Avg:", sum([x[1] for x in space_counts[lang]]) / len(space_counts[lang]))

        print()
        
        # Sort by token / key        
        
        exact_counts[lang].sort(key=lambda x: x[0])
        prob_counts[lang].sort(key=lambda x: x[0])
        space_counts[lang].sort(key=lambda x: x[0])

        print("--- Absolute Errors")
        exact_vs_prob = [
            [
                exact_counts[lang][i][0],
                exact_counts[lang][i][1] - prob_counts[lang][i][1],
            ]
            for i in range(TOP)
        ]
        exact_vs_space = [
            [
                exact_counts[lang][i][0],
                exact_counts[lang][i][1] - space_counts[lang][i][1],
            ]
            for i in range(TOP)
        ]
        print("Exact vs Prob:")
        print("Max:", max([abs(x[1]) for x in exact_vs_prob]))
        print("Min:", min([abs(x[1]) for x in exact_vs_prob]))
        print("Avg:", sum([abs(x[1]) for x in exact_vs_prob]) / len(exact_vs_prob))
        print("Exact vs Space:")
        print("Max:", max([abs(x[1]) for x in exact_vs_space]))
        print("Min:", min([abs(x[1]) for x in exact_vs_space]))
        print("Avg:", sum([abs(x[1]) for x in exact_vs_space]) / len(exact_vs_space))

        print()

        print("--- Relative Errors")
        exact_vs_prob = [
            [
                exact_counts[lang][i][0],
                (exact_counts[lang][i][1] - prob_counts[lang][i][1])
                / exact_counts[lang][i][1],
            ]
            for i in range(TOP)
        ]
        exact_vs_space = [
            [
                exact_counts[lang][i][0],
                (exact_counts[lang][i][1] - space_counts[lang][i][1])
                / exact_counts[lang][i][1],
            ]
            for i in range(TOP)
        ]
        print("Exact vs Prob:")
        print("Max:", max([abs(x[1]) for x in exact_vs_prob]))
        print("Min:", min([abs(x[1]) for x in exact_vs_prob]))
        print("Avg:", sum([abs(x[1]) for x in exact_vs_prob]) / len(exact_vs_prob))
        print("Exact vs Space:")
        print("Max:", max([abs(x[1]) for x in exact_vs_space]))
        print("Min:", min([abs(x[1]) for x in exact_vs_space]))
        print("Avg:", sum([abs(x[1]) for x in exact_vs_space]) / len(exact_vs_space))

        print()
