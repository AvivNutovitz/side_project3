import numpy as np  # linear algebra
from keras.applications import inception_v3
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, Input
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split, StratifiedKFold
import os
from google.cloud import storage
import tempfile

K_FOLDS = 5
NUM_CLASSES = 2
RANDOM_SEED = 7
FULLY_CONNECTED_LAYER_SIZE = 1024
DEFAULT_LEARNING_RATE = 0.0001
MIN_DELTA = 0.01
PATIENCE = 7


class InceptionDicomModel:
    def __save_blob(self, bucket_name, source_file, dest_blob):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(dest_blob)

        blob.upload_from_filename(source_file)
        print("saved file "+ source_file )

    def __create_model(self):
        np.random.seed(RANDOM_SEED)
        base_model = inception_v3.InceptionV3(weights=None, include_top=False)
        # modify inception_v3
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(FULLY_CONNECTED_LAYER_SIZE, activation='relu')(x)
        predictions = Dense(NUM_CLASSES, activation='softmax')(x)
        self.__model = Model(inputs=base_model.input, outputs=predictions)
        for layer in base_model.layers:
            layer.trainable = False

        self.__model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(lr=self.__default_learning_rate), metrics=['acc'])

    def fit(self, X, Y):
        # split into folds
        folds = list(StratifiedKFold(n_splits=K_FOLDS, shuffle=True, random_state=RANDOM_SEED).split(X, Y))
        es = EarlyStopping(
            monitor='vai_loss',
            min_delta=MIN_DELTA,
            patience=PATIENCE,
            verbose=1,
            mode='max'
        )

        for j, (train_idx, val_idx) in enumerate(folds):
            print('\nFold ', j)
            X_train_cv = X[train_idx]
            y_train_cv = Y[train_idx]
            X_valid_cv = X[val_idx]
            y_valid_cv = Y[val_idx]

            self.__model.fit(X_train_cv, y_train_cv,
                             verbose=self.__verbose,
                             batch_size=self.__batch_size,
                             epochs=self.__epochs,
                             callbacks=[es])

            print(self.__model.evaluate(X_valid_cv, y_valid_cv))

    def save_model_to_bucket(self, bucket_name, model_prefix_name):
        # Create json and h5 files
        model_json = self.__model.to_json()
        with open(os.path.join(tempfile.gettempdir(), "model.json"), "w") as json_file:
            json_file.write(model_json)
        self.__model.save_weights(os.path.join(tempfile.gettempdir(), "model.h5"))

        # Save them to bucket
        self.__save_blob(bucket_name,
                         os.path.join(tempfile.gettempdir(), "model.json"),
                         model_prefix_name + "_model.json")
        self.__save_blob(bucket_name,
                         os.path.join(tempfile.gettempdir(), "model.h5"),
                         model_prefix_name + "_model.h5")

    def __init__(self, learning_rate=DEFAULT_LEARNING_RATE, epochs=5, batch_size=5, verbose=False):
        self.__default_learning_rate = learning_rate
        self.__model = None
        self.__epochs = epochs
        self.__batch_size = batch_size
        self.__verbose = verbose
        self.__create_model()
