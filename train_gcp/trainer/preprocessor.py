import pydicom
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from io import StringIO, BytesIO
import os
from google.cloud import storage
from .secrets import GOOGLE_API_JSON_FILE_NAME


class PreProcessor:
    def __init__(self, working_bucket, max_data_size=30):
        self.__working_bucket = working_bucket
        self.__max_data_size = max_data_size

    def __download_blob_to_memory(self, source_blob_name):
        """Downloads a blob from the bucket."""
        # js_file = "{}{}{}".format(self.data_folder, os.sep, GOOGLE_API_JSON_FILE_NAME)
        # storage_client = storage.Client.from_service_account_json(js_file)
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(self.__working_bucket)
        blob = bucket.blob(source_blob_name)

        return blob.download_as_string()

    def get_preprocessed_data(self):
        self.data_folder = "{}{}".format(os.getcwd(), os.sep)
        io = self.__download_blob_to_memory('stage_1_train_labels.csv')
        # read csv train file
        train_labeles = pd.read_csv(StringIO(io.decode("UTF-8")), index_col='patientId')

        # get images
        list_of_images = []
        list_of_lables = []

        training_size = min(self.__max_data_size, len(train_labeles))
        for patientId, target in zip(train_labeles.index[:training_size], train_labeles.Target[:training_size]):
            dcm_file_name = 'stage_1_train_images/{}.dcm'.format(patientId)
            io = self.__download_blob_to_memory(dcm_file_name)
            dcm_data = pydicom.read_file(BytesIO(io))
            im = dcm_data.pixel_array
            downsampled = im[::4, ::4]
            # Convert from single-channel grayscale to 3-channel RGB
            im = np.stack([downsampled] * 3, axis=2)
            list_of_images.append(im)
            list_of_lables.append(target)

        return list_of_images, list_of_lables
