import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Sample Data (you can replace this with your actual dataset)
data = {
    'Lactation_Stage': ['Early', 'Mid', 'Late', 'Dry', 'Early', 'Mid'],
    'Age': [2, 5, 4, 6, 3, 2],
    'Enclosure_Temperature': [22, 25, 21, 19, 23, 24],
    'Outside_Temperature': [30, 28, 32, 29, 31, 30],
    'Feed_Type': ['Grass', 'Silage', 'Grass', 'Silage', 'Grass', 'Silage'],
    'Health': ['Good', 'Moderate', 'Good', 'Poor', 'Good', 'Moderate'],
    'Milk_Yield_Liters': [25, 22, 18, 10, 24, 20]
}

# Load data into a DataFrame
df = pd.DataFrame(data)

# Map categorical variables to numeric values
lactation_stage_mapping = {'Early': 1, 'Mid': 2, 'Late': 3, 'Dry': 4}
health_mapping = {'Good': 1, 'Moderate': 2, 'Poor': 3}
feed_type_mapping = {'Grass': 1, 'Silage': 2}

df['Lactation_Stage'] = df['Lactation_Stage'].map(lactation_stage_mapping)
df['Health'] = df['Health'].map(health_mapping)
df['Feed_Type'] = df['Feed_Type'].map(feed_type_mapping)

# Features and target
X = df[['Lactation_Stage', 'Age', 'Enclosure_Temperature', 'Outside_Temperature', 'Feed_Type', 'Health']]
y = df['Milk_Yield_Liters']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model for regression
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict milk yield on test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Decision-making logic: Recommend milking if the predicted yield is above a threshold (e.g., 20 liters)
threshold = 20  # You can adjust this threshold based on the context
milk_time_recommendation = []

for predicted_yield in y_pred:
    if predicted_yield >= threshold:
        milk_time_recommendation.append("Optimal time to milk")
    else:
        milk_time_recommendation.append("Not the best time to milk")

# Display the predictions and recommendations
for i in range(len(y_pred)):
    print(f"Predicted Milk Yield: {y_pred[i]:.2f} Liters - {milk_time_recommendation[i]}")

 