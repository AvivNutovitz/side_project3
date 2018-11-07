import argparse
from .preprocessor import PreProcessor
from .model import InceptionDicomModel
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Training arguments
    parser.add_argument(
        '--job-dir',
        help='The name of the bucket to extract data from',
        required=True
    )
    parser.add_argument(
        '--data_bucket',
        help='The name of the bucket to extract data from',
        required=True
    )
    parser.add_argument(
        '--max_data_size',
        help='Max data size to read from bucket',
        type=int,
        default=10
    )
    parser.add_argument(
        '--batch_size',
        help='Batch size',
        type=int,
        default=50
    )
    parser.add_argument(
        '--epochs',
        help='Num of Epochs',
        type=int,
        default=50
    )
    parser.add_argument(
        '--verbose',
        help='Verbosity level',
        dest='verbose', action='store_true'
    )
    args = parser.parse_args()

    # Get the preprocessed data
    preproc = PreProcessor(args.data_bucket, max_data_size=args.max_data_size)
    training_data, training_labels = preproc.get_preprocessed_data()

    # Get the training model
    model = InceptionDicomModel(verbose=args.verbose,
                                batch_size=args.batch_size,
                                epochs=args.epochs)

    model.fit(np.array(training_data), np.array(training_labels))

    model.save_model_to_bucket(args.data_bucket, 'z_project')
