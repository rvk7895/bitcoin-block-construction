# Bitcoin Mining

## Objective 
Constructing a block by selecting a set of transactions from the mempool.\
The miner selects an ordered list of transactions which have a combined weight below the maximum block weight. Transactions with parent transactions in the mempool may be included in the list, but only if all of their parents appear before them in the list.Naturally, the miner would like to include the transactions that maximize the total fee.

## Solution
The solution involves giving a score to each transaction. We see that a transaction is good if it has a high fee and low weight. Thus the score of the transaction would directly proportional to the fee and inversely proportional to that of weight. To account for the parent transactions, to the score of the transaction we add to it the score of its immediate parent transactions and the score assigned to the transaction is taken to be the mean of all the scores that have been together. Then the transaction are sorted in descending of order of their scores and a block is made out of the valid transactions.

The formula for the score of a transaction is as follows:\
<img src="https://render.githubusercontent.com/render/math?math=\text{score} = \frac{\frac{\text{fee}}{\text{weight}}%2B \text{scores of parents}}{\text{no.of parents} %2B 1}">

To run the code, run the following in you command line
```
python3 main.py
```