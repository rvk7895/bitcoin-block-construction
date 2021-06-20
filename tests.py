import json


file = open('./block.txt','r')
data = file.readlines()

for i in range(len(data)):
    for j in range(len(data)):
        if data[i] == data[j] and i!=j:
            print("found")

'''
check if parents are above children
'''
transactions = json.load(open('./processed_transactions.json','r'))
idx = 0
for id in data:
    id = id.strip()
    for parent_id in transactions[id]["parents"]:
        p_idx = 0
        for pid in data:
            if parent_id == pid:
                if p_idx > idx:
                    print("parent after child")
                    break
            p_idx += 1
