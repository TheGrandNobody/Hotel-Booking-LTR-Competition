This repository implements the necessary framework to train a LambdaMART model (using RankLib) to rank the results of a hotel booking search engine from the ICDM 2013 Expedia Hotel Booking Search Kaggle Competition. 

## Ranklib Format
Training and testing uses RankLib, therefore you need to first convert your datasets from csv to ranklib format using:
```
python3 csv_to_ranklib.py INPUT_FILE_NAME.csv OUTPUT_FILE_NAME.txt
```

## Training
Then you may initiate training. Using default parameters, this would be done as follows:
```
java -jar RankLib-2.18.jar -train train.txt -ranker 6 -metric2t NDCG@5 -save model.txt
```
Otherwise, navigate to https://sourceforge.net/p/lemur/wiki/RankLib%20How%20to%20use/ to see the full list of parameters you can add to the training process.

## Testing
Finally, you may test the model's performance using:
```
java -jar RankLib-2.18.jar -load model.txt -test test.txt -metric2T NDCG@5 -idv performance.txt
```