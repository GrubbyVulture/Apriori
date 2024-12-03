from itertools import combinations
from collections import defaultdict

# 数据集
transactions = [
    {'面包', '牛奶'},
    {'面包', '尿布', '啤酒', '鸡蛋'},
    {'牛奶', '尿布', '啤酒', '可乐'},
    {'面包', '牛奶', '尿布', '啤酒'},
    {'面包', '牛奶', '尿布', '可乐'},
]


# Apriori算法实现
def apriori(transactions, min_support=0.5):
    num_transactions = len(transactions)
    min_count = min_support * num_transactions

    # 生成频繁1项集
    C1 = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            C1[frozenset([item])] += 1

    L1 = {k: v for k, v in C1.items() if v >= min_count}
    result = [L1]

    # 迭代生成频繁k项集
    k = 2
    while True:
        prev_Lk = result[-1]
        items = list(prev_Lk.keys())
        Ck = defaultdict(int)

        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                union_set = items[i] | items[j]
                if len(union_set) == k:
                    for transaction in transactions:
                        if union_set.issubset(transaction):
                            Ck[union_set] += 1

        Lk = {k: v for k, v in Ck.items() if v >= min_count}
        if not Lk:
            break
        result.append(Lk)
        k += 1

    return result


# 计算提升度
def calculate_lift(frequent_itemsets, transactions):
    num_transactions = len(transactions)
    support = {itemset: count / num_transactions for level in frequent_itemsets for itemset, count in level.items()}
    lift_results = []

    for level in frequent_itemsets:
        for itemset in level:
            if len(itemset) > 1:
                for A_len in range(1, len(itemset)):
                    for A in combinations(itemset, A_len):
                        A = frozenset(A)
                        B = itemset - A
                        lift = support[itemset] / (support[A] * support[B])
                        lift_results.append((A, B, lift))

    return lift_results


# 运行Apriori算法
frequent_itemsets = apriori(transactions, min_support=0.5)

# 计算提升度
lift_results = calculate_lift(frequent_itemsets, transactions)

# 输出结果
print("频繁项集:")
for i, level in enumerate(frequent_itemsets):
    print(f"L{i + 1}: {level}")

print("\n提升度计算结果:")
for A, B, lift in lift_results:
    print(f"规则: {A} -> {B}, 提升度: {lift:.2f}")
