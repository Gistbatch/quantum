import numpy as np

from data_utils import generate_dataset
from utils import transform, unitaries

DIMENSION = 4


def init_weights(dimension):
    weights = []
    for _ in range(dimension - 1):
        weight = np.random.random(4**2)  #TODO check init of wheights
        weights.append(weight)
    return weights


if __name__ == "__main__":
    (x_train, y_train), (x_test, y_test) = generate_dataset(DIMENSION)
    image = x_train[0].flatten()
    features = transform(image)
    weights = init_weights(DIMENSION**2)
    unitaries_ = unitaries(weights)
    print(features, weights[0], unitaries_[0])