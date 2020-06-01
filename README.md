# machinelearningpipeline
This repo has sample code to create an API to predict if a domian is DGA or not using AWS sagemaker and apigateway. It also have terraform script for deployment.

## Data Setup 
### DGA generations code
I have taken old code from these two repo and changed it to python 3 version
https://github.com/andrewaeva/DGA/blob/master/dga_wordlists/main.py

https://github.com/baderj/domain_generation_algorithms  

New code and docker file to generate DGA are in:
https://github.com/aftabalam01/machinelearningpipeline/tree/master/src/dataset
### NoteBook to clean up and create final data
https://github.com/aftabalam01/machinelearningpipeline/blob/master/src/notebooks/Benign_dataSetup_explore.ipynb

## Build and train model
https://github.com/aftabalam01/machinelearningpipeline/blob/master/src/notebooks/Build-deploy-dga-xgboost_exp5.ipynb
*Sample code with tensorflow and using sagemaker script mode
https://github.com/aftabalam01/machinelearningpipeline/blob/master/src/notebooks/Build%20Tensorflow%20LSTM%20model-sagemaker.ipynb
*model script
https://github.com/aftabalam01/machinelearningpipeline/blob/master/src/notebooks/tf-model.py

### Lambda functions to integration between apigateway and model endpoint
https://github.com/aftabalam01/machinelearningpipeline/tree/master/src/lambda

### Finally test code to test endpoint
https://github.com/aftabalam01/machinelearningpipeline/blob/master/src/Test/TestCode.py
