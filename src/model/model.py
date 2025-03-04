import pickle
from sklearn.linear_model import LogisticRegression

class SimpleModel:
    def __init__(self):
        # Initialize a logistic regression model as an example
        self.model = LogisticRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, filepath):
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
