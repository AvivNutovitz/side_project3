import boto3
import botocore
from botocore import exceptions
from keras.models import model_from_json
from io import BytesIO
import pydicom
import numpy as np

"""
event:
{
    BucketName: "",
    ModelFile: "",
    WeightsFile: "",
    Data: 
}
"""


def retrieve_model_from_bucket(bucket, model, weights):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket).download_file(model, '/tmp/model.json')
        s3.Bucket(bucket).download_file(weights, '/tmp/model.h5')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


def load_pydicom_data(raw_data):
    dcm_data = pydicom.read_file(BytesIO(raw_data))
    im = dcm_data.pixel_array
    downsampled = im[::4, ::4]
    # Convert from single-channel grayscale to 3-channel RGB
    im = np.stack([downsampled] * 3, axis=2)
    return im


def compile_downloaded_model():
    with open('/tmp/model.json', 'r') as json_model_file:
        loaded_json = json_model_file.read()
        model = model_from_json(loaded_json)
        model.load_weights("/tmp/model.h5")
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model


def predict_handler(event, context):
    # Start by asserting the event
    if not (all(k in event for k in ("BucketName", "ModelFile", "WeightsFile", "Data"))):
        return {"Not all keys exist"}

    # Download the model files
    retrieve_model_from_bucket(event['BucketName'], event['ModelFile'], event['WeightsFile'])

    # Get the compiled model
    model = compile_downloaded_model()

    # Load the data into pydicom
    input_image = load_pydicom_data(event['Data'])

    # Do the actual prediction
    prediction = model.predict(input_image)

    # Return the prediction from the lambda
    return {"Prediction": str(prediction)}
