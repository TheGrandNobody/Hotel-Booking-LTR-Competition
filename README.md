This repository implements the necessary framework to train a LambdaMART model (using RankLib) to rank the results of a hotel booking search engine from the ICDM 2013 Expedia Hotel Booking Search Kaggle Competition. 

## Ranklib Format
Training and testing uses RankLib, therefore you need to first convert your datasets from csv to ranklib format using:
```
python3 csv_to_ranklib.py INPUT_FILE_NAME.csv OUTPUT_FILE_NAME.txt
```
If you are running this for the training set, you HAVE to set the file name to train.txt. 

## Training
Then you may initiate training. Using default parameters, a training file `train.txt` and a validation file `valid.txt` this would be done as follows:
```
java -jar RankLib-2.18.jar -train train.txt -validate -valid.txt -ranker 6 -metric2t NDCG@5 -save model.txt
```
However, you'll want to tune parameters, so it's best to read further and follow the protocol below.

## Parameter Tuning with RankLib
Some of the most important parameters are:

- `tree` (the number of trees to be grown): The number of trees in the model affects its complexity, with more trees typically leading to more complex models. However, increasing the number of trees may also increase the risk of overfitting and will certainly increase computational demand.

- `leaf` (the number of leaves for each tree): This parameter determines the maximum depth or complexity of each individual tree. A higher number of leaves allows more complex interactions but also increases the risk of overfitting and computational cost.

- `shrinkage` (learning rate for boosting): The shrinkage parameter scales the contribution of each tree to the final model. A smaller shrinkage value can make the model more robust to noise but can also require more trees to achieve good performance, increasing computational cost.

- `mls` (minimum instances per leaf): The minimum instances per leaf is a regularization parameter that determines the minimum number of data points required to form a leaf in a tree. A higher value helps prevent overfitting by making trees less complex but can cause underfitting if set too high.

- `estop` (early stopping rounds): This is the number of rounds without improvement before training is stopped early. It helps to avoid overfitting and unnecessary computation by stopping training when the model's performance on a validation set is no longer improving.

You can also navigate to https://sourceforge.net/p/lemur/wiki/RankLib%20How%20to%20use/ to see the full list of parameters you can add to the training process.

## Protocol
### Grid Search
Start by performing a grid search to identify a good starting point. You might want to start wide, then narrow down the search space. For example, you could start by testing the number of trees from 1000 to 5000 in increments of 500, the number of leaves from 10 to 100 in increments of 10, and the learning rate from 0.1 to 1.0 in increments of 0.1.

Therefore, start with the following command and increment as needed:
```
java -jar RankLib-2.18.jar -train train.txt -validate valid.txt -ranker 6 -metric2t NDCG@5 -tree 1000 -leaf 10 -shrinkage 0.1 -mls 1 -estop 50 -save model.txt
```
### K-fold Cross Validation
Once that is done, and you think you have somewhat good parameters, move on to k-fold cross validation, whill help determine performance on unseen data. You can use the following command to perform k-fold cross validation, with `-kcv 5` corresponding to the number folds you want to use:
```
java -jar RankLib.jar -train train.txt -ranker 6 -tree 500 -leaf 10 -shrinkage 0.1 -mls 1 -estop 50 -kcv 5 -kcvmd models/ -kcvmn performance.txt
```
### Fine-tuning
Finally, you can fine-tune by performing a more detailed grid search around the earlier parameters you found that worked well. For example, if you found that 500 trees and 50 leaves give the best results, you could then test the number of trees from 400 to 600 in increments of 20, and the number of leaves from 40 to 60 in increments of 2.

## Testing
After training, you may test the model's performance by first creating the scores from the test set using:
```
java -jar RankLib-2.18.jar -load model.txt -rank test.txt -score score.txt  
```
And then formatting the scores into the submission format using:
```
python3 convert_scores.py
```