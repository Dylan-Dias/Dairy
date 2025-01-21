import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load data from Excel file
file_path = r"C:\Users\Dylan\Desktop\Cow_Data_Sample.xlsx"
df = pd.read_excel(file_path)

# Debug: Check initial data
print("Initial DataFrame:")
print(df.head())
print(df.info())

# Map Lactation_Stage to numeric codes
lactation_stage_mapping = {
    "Early": 1,
    "Mid": 2,
    "Late": 3,
    "Dry": 4
}
df['Lactation_Stage'] = df['Lactation_Stage'].map(lactation_stage_mapping)

# Ensure correct data types
df['Enclosure_Temperature'] = pd.to_numeric(df['Enclosure_Temperature'], errors='coerce')
df['Outside_Temperature'] = pd.to_numeric(df['Outside_Temperature'], errors='coerce')
df['Milk_Yield_Liters'] = pd.to_numeric(df['Milk_Yield_Liters'], errors='coerce')
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

# Drop rows with invalid data
df = df.dropna()

# Debug: Check data after preprocessing
print("DataFrame after preprocessing:")
print(df.head())
print(df.shape)  # Ensure there are rows and columns

# Ensure there are rows to proceed
if df.shape[0] == 0:
    raise ValueError("The dataset is empty after preprocessing. Check your Excel file and preprocessing steps.")

# Features and target
X = df[['Lactation_Stage', 'Age', 'Enclosure_Temperature', 'Outside_Temperature', 'Feed_Type', 'Health']]
y = df['Milk_Yield_Liters']

# Encode categorical variables (Feed_Type and Health) as dummy variables
X = pd.get_dummies(X, columns=['Feed_Type', 'Health'], drop_first=True)

# Debug: Check features and target
print("Features (X):")
print(X.head())
print("Target (y):")
print(y.head())

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize XGBoost Regressor
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation:")
print("Mean Squared Error:", mse)
print("R^2 Score:", r2)
