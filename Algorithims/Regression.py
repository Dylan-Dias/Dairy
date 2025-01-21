import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Sample data (real farm data should be used for better accuracy)
data = {
    'Age_ID': [15, 20, 30, 50, 100, 20],
    'Breed': ['Holstein', 'Jersey', 'Shorthorn', 'Ayrshire', 'BrownSwiss', 'Guernsey'],
    'Health': ['Healthy', 'Mastitis', 'Healthy', 'Healthy', 'Mastitis', 'Healthy'],
    'Milking_Frequency': ['2', '2', '2', '4', '2', '2'],
    'Living_Conditions': ['Good', 'Good', 'Bad', 'Good', 'Good', 'Great'],
    'Lactation_Stage': ['Early', 'Late', 'Mid', 'Dry', 'Early', 'Dry'],
    'Feed': ['Alfalfa', 'Grain', 'Grain', 'Corn', 'Barley', 'Barley'],
    'Yield': [50, 25, 12, 34, 80, 2]  # Milk yield in liters (numeric)
}

# Dataframe
df = pd.DataFrame(data)

# Convert categorical features to numerical ones (one-hot encoding for categorical variables)
df = pd.get_dummies(df, columns=['Breed', 'Health', 'Milking_Frequency', 'Living_Conditions', 'Lactation_Stage', 'Feed'])

# Split into features (X) and target (y)
X = df.drop(columns=['Age_ID', 'Yield'])  # Features
y = df['Yield']  # Target variable (Milk Yield)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Output predicted milk yield
print(f"Predicted Milk Yields: {y_pred}")
