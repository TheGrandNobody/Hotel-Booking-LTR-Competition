This repository implements the necessary framework to train a LambdaMART model (using RankLib) to rank the results of a hotel booking search engine from the ICDM 2013 Expedia Hotel Booking Search Kaggle Competition. 

## Ranklib Format
Training and testing uses RankLib, therefore you need to first convert your datasets from csv to ranklib format using:
```
python3 csv_to_ranklib.py INPUT_FILE_NAME.csv OUTPUT_FILE_NAME.txt
```

## Training
Then you may initiate training. Using default parameters, this would be done as follows:
```
java -jar RankLib-2.18.jar -train train.txt -validate -valid.txt -ranker 6 -metric2t NDCG@5 -save model.txt
```
## Parameter Tuning with RankLib
Some of the most important parameters are:

- `tree` (the number of trees to be grown): The number of trees in the model affects its complexity, with more trees typically leading to more complex models. However, increasing the number of trees may also increase the risk of overfitting and will certainly increase computational demand.

- `leaf` (the number of leaves for each tree): This parameter determines the maximum depth or complexity of each individual tree. A higher number of leaves allows more complex interactions but also increases the risk of overfitting and computational cost.

- `shrinkage` (learning rate for boosting): The shrinkage parameter scales the contribution of each tree to the final model. A smaller shrinkage value can make the model more robust to noise but can also require more trees to achieve good performance, increasing computational cost.

- `mls` (minimum instances per leaf): The minimum instances per leaf is a regularization parameter that determines the minimum number of data points required to form a leaf in a tree. A higher value helps prevent overfitting by making trees less complex but can cause underfitting if set too high.

- `estop` (early stopping rounds): This is the number of rounds without improvement before training is stopped early. It helps to avoid overfitting and unnecessary computation by stopping training when the model's performance on a validation set is no longer improving.

### Protocol
Start by performing a grid search to identify a good starting point. You might want to start wide, then narrow down the search space. For example, you could start by testing the number of trees from 100 to 1000 in increments of 100, the number of leaves from 10 to 100 in increments of 10, and the learning rate from 0.1 to 1.0 in increments of 0.1.

```
java -jar RankLib-2.18.jar -train train.txt -validate valid.txt -ranker 6 -metric2t NDCG@5 -tree 100 -leaf 10 -shrinkage 0.1 -mls 1 -estop 100 -save model.txt
```

Otherwise, navigate to https://sourceforge.net/p/lemur/wiki/RankLib%20How%20to%20use/ to see the full list of parameters you can add to the training process.

## Testing
Finally, you may test the model's performance using:
```
java -jar RankLib-2.18.jar -load model.txt -test test.txt -metric2T NDCG@5 -idv performance.txt
```