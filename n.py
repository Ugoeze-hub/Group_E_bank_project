from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# Example data
X = [[1], [2], [3], [4], [5]]
y = [0, 0, 1, 1, 1]
# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Training Data:", X_train, y_train)
print("Test Data:", X_test, y_test)