Google cloud platform (GCP) Readme:

this is a shot menu of the GCP component in the project.
I used this tutorial as a guide line:
https://towardsdatascience.com/how-to-train-machine-learning-models-in-the-cloud-using-cloud-ml-engine-3f0d935294b3

the structure of work was as follow:
I created an account, there A had a bucket were all data is stored, ML job monitor to run train jobs
I had an issue with limitations from GCP and was able to train the model only on 200 examples before got cut of by GCP

in the most basic form the job will take the data from the bucket train the model and save .json +.h5 file back in the bucket.
+ I added an EarlyStopping as a callback to stop the model when the improvement of the model is not increasing

in order to fit to the template the project there are 5 python files (+setup & requirements) 
moreover there is the jupyter notebook with the answers to the 3 questions

the python files are:
task.py that gets the arguments from the GCP cli and pass it to the model
preprocessor.py the pre-process the data before running the model
model.py witch based on the inception_v3 model of keras,
this file fit and save the model in the bucket
and the last file is secrets.py the hold the GOOGLE_API_JSON file name that is part of the key (to connect to GCP)

in order to run the training stage I used GCP cli (locally) by typing 'gcloud init' form the bash (root)
the command structure was as follow: 

set in advance:

#!/bin/bash
TRAIN_DATA_PATHS=path/to/training/data
OUTPUT_DIR=path/to/output/location
JOBNAME=my_ml_job_$(date -u +%y%m%d_%H%M%S)
REGION='us-central1'
BUCKET='my-bucket-name'

gcloud ml-engine jobs submit training $JOBNAME \
		--job-dir aviv-nutovitz-test-b1 
		--data_bucket aviv-nutovitz-test-b1
		--max_data_size 200
		--epochs 50
        --verbose 1
        -- \  # Required.
        --train_data_paths $TRAIN_DATA_PATHS \
        --output_dir $OUTPUT_DIR\
        --batch_size 100\


