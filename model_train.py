import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from joblib import dump

# Load your dataset
data = pd.read_csv('spoilage_data.csv')  # Use your actual filename

# Split features and target
X = data[['temperature', 'humidity', 'transport_time', 'distance']]
y = data['shelf_life_remaining']

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create and train the model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save the trained model to a file
dump(model, 'shelf_life_model.joblib')

print("✅ Model trained and saved as shelf_life_model.joblib")