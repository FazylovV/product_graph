import csv
import itertools

pairs = set()

with open('./data/similar.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    count = 0
    for pair in reader:
        count += 1
        pairs.add(frozenset({pair['asin'], pair['similar_asin']}))

# uniquepairs = {frozenset(pair) for pair in pairs}
# uniquepairslist = [tuple(sorted(pair)) for pair in uniquepairs]

with open('similar_unique_pairs.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
    writer.writeheader()
    for pair in pairs:
        pair = list(pair)
        writer.writerow({'asin': pair[0], 'similar_asin': pair[1]})

print(len(pairs))