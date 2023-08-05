# Transaction Validator
<hr> 

## - TransactionValidators
<br />

- This package will contain many methods that will help validating transactions taxes.<br />
- In TransactionValidators you can find **3** main methods :- <br />
    1. **validateTransactionFolder** (transactionFolder)<br />
        > print(validateTransactionFolder("transactionFolder/))<br />
        \# output:  [{True, 'transactionFolder/foo.xml'}, {False, 'transactionFolder/boo.json'}]
    2. **validateTransactionsFile** (transactionFile)<br />
        > print(validateTransactionsFile("foo.xml"))<br />
        \# output:  True  // example
    3. **validateTransaction** (dictTransaction)<br />
        > print(validateTransaction(dicTransaction))<br />
        \# output:  False // example

<hr>

##  - gRPC
<br />

- Also you will find a gRPC module that have **validator_server.py** and **validator_client.py**. <br />
- You just need to run the validator_server, then it can accept any validator_client remote call.<br />
    > python validator_server.py
- To call the gRPC you need to run the validator_client with a parameter of the required file to check.<br />
    > python validator_client.py "test.xml"
    \# It is using **validateTransactionFile** method. (Boolean output)
<hr>

- Contact me at : **ba.2912.98@gmail.com**
