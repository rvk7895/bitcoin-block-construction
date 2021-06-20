import csv
import json
import queue
from pprint import pprint
from operator import itemgetter

data = {}
priority_queue = queue.PriorityQueue()
blocks_fee = 0
blocks_weight = 0
blocks = {}
processed_transactions = []
transactions_rejected = {}
MAX_WEIGHT = 4000000
final_transactions = []

with open("./mempool.csv") as f:
    line_count = 0
    for line in csv.reader(f):
        if line_count != 0:
            data[line[0]] = {
                "fee": int(line[1]),
                "weight": int(line[2]),
                "parents": line[3].split(";"),
            }
            if "" in data[line[0]]["parents"]:
                data[line[0]]["parents"] = []
        line_count += 1

# score of a transaction = fee/weight + scores of parents


def calculate_score(tx_id):
    score = float(data[tx_id]["fee"]) / data[tx_id]["weight"]
    weight = data[tx_id]["weight"]
    fee = data[tx_id]["fee"]
    for parent in data[tx_id]["parents"]:
        parent_score, parent_weight, parent_fee = calculate_score(parent)
        data[parent]["score"] = parent_score
        data[parent]["total_weight"] = parent_weight
        data[parent]["total_fee"] = parent_fee
        score += parent_score
        weight += parent_weight
        fee += parent_fee

    return score, weight, fee


for tx_id in data.keys():
    if "score" not in data[tx_id]:
        score, total_weight, total_fee = calculate_score(tx_id)
        data[tx_id]["score"] = score
        data[tx_id]["total_weight"] = total_weight
        data[tx_id]["total_fee"] = total_fee
    
    data[tx_id]["included"] = False
    processed_transaction = {
        "tx_id": tx_id,
        "score": data[tx_id]["score"],
    }

    processed_transactions.append(processed_transaction.copy())

sorted_processed_transactions = sorted(
    processed_transactions, key=lambda i: i["score"])


def include_parent_transaction(tx_id):
    for parent_tx_id in data[tx_id]["parents"]:
        if not data[parent_tx_id]["included"]:
            data[parent_tx_id]["included"] = True
            final_transactions.append(parent_tx_id)
            include_parent_transaction(parent_tx_id)
    return


for transaction in sorted_processed_transactions:
    tx_id, score = itemgetter('tx_id', 'score')(transaction)
    if (blocks_weight + data[tx_id]["total_weight"]) < MAX_WEIGHT and not data[tx_id]["included"]:
        blocks_weight += data[tx_id]["total_weight"]
        final_transactions.append(tx_id)
        data[tx_id]["included"] = True
        include_parent_transaction(tx_id)

file = open('block.txt', 'w')
for transaction in final_transactions:
    file.write(transaction+"\n")
file.close()

# with open('./processed_transactions.json','w') as f:
#     json.dump(data, f)
