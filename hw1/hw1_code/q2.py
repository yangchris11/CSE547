import collections

SUPPORT = 100

all_item = collections.defaultdict(int) # C1
frequent_itemset = collections.defaultdict(int)# L1

with open('q2/data/browsing.txt', 'r') as file:
    for basket in file:
        items = basket.strip().split(' ')
        for item in items:
            all_item[item] += 1

    for item_id, item_count in all_item.items():
        if item_count >= SUPPORT:
            frequent_itemset[item_id] = item_count

print('Total unique item IDs(support >= 0): ', len(all_item))
print('Total unique item IDs(support >= 100): ', len(frequent_itemset))

# N = len(frequent_itemset)
all_2pair = collections.defaultdict(int) # C2
frequent_2pairset = collections.defaultdict(int)  # L2

with open('q2/data/browsing.txt', 'r') as file:
    for basket in file:
        items = basket.strip().split(' ')
        n = len(items)
        for i in range(0, n-1):
            if items[i] in frequent_itemset:
                for j in range(i+1, n):
                    if items[j] in frequent_itemset:
                        key = (items[i], items[j]) if items[i] < items[j] else (items[j], items[i])
                        all_2pair[key] += 1
    
    for pair_ids, pair_count in all_2pair.items():
        if pair_count >= SUPPORT:
            frequent_2pairset[pair_ids] = pair_count

print('Total unique item IDs(support >= 0): ', len(all_2pair))
print('Total unique item IDs(support >= 100): ', len(frequent_2pairset))


confidence_size2 = []
for pair_ids, pair_count in frequent_2pairset.items():
    item1, item2 = pair_ids
    confidence_size2.append((item1, item2, pair_count/frequent_itemset[item1]))
    confidence_size2.append((item2, item1, pair_count/frequent_itemset[item2]))

confidence_size2.sort(key = lambda x: -x[2])

for i in range(5):
    print(confidence_size2[i][0], confidence_size2[i][1], confidence_size2[i][2])



all_3pair = collections.defaultdict(int) # C3
frequent_3pairset = collections.defaultdict(int)  # L3

with open('q2/data/browsing.txt', 'r') as file:
    for basket in file:
        items = basket.strip().split(' ')
        n = len(items)
        for i in range(0, n-2):
            for j in range(i+1, n-1):
                for k in range(j+1, n):
                    sorted_pairs = sorted([items[i], items[j], items[k]])
                    key_pair1 = (sorted_pairs[0], sorted_pairs[1])
                    key_pair2 = (sorted_pairs[0], sorted_pairs[2])
                    key_pair3 = (sorted_pairs[1], sorted_pairs[2])
                    # key_pairs = ((sorted_pairs[0], sorted_pairs[1]), (sorted_pairs[0], sorted_pairs[2]), (sorted_pairs[1], sorted_pairs[2]))
                    if key_pair1 in frequent_2pairset and key_pair2 in frequent_2pairset and key_pair3 in frequent_2pairset:
                        all_3pair[tuple(sorted_pairs)] += 1
    
    
    for pair_ids, pair_count in all_3pair.items():
        if pair_count >= SUPPORT:
            frequent_3pairset[pair_ids] = pair_count

print('Total unique item IDs(support >= 0): ', len(all_3pair))
print('Total unique item IDs(support >= 100): ', len(frequent_3pairset))


confidence_size3 = []
for pair_ids, pair_count in frequent_3pairset.items():
    key_pair1 = (pair_ids[0], pair_ids[1])
    key_pair2 = (pair_ids[0], pair_ids[2])
    key_pair3 = (pair_ids[1], pair_ids[2])

    confidence_size3.append([key_pair1, pair_ids[2], pair_count/frequent_2pairset[key_pair1]])
    confidence_size3.append([key_pair2, pair_ids[1], pair_count/frequent_2pairset[key_pair2]])
    confidence_size3.append([key_pair3, pair_ids[0], pair_count/frequent_2pairset[key_pair3]])

confidence_size3.sort(key = lambda x: (-x[2], x[0][0], x[0][1], x[1]))

for i in range(5):
    print(confidence_size3[i][0], confidence_size3[i][1], confidence_size3[i][2])
