import pulp
import pandas as pd

# Sample Data
data = {
    'Age_ID': [15, 20, 30, 50, 100, 20],
    'Breed': ['Holstein', 'Jersey', 'Shorthorn', 'Ayrshire', 'BrownSwiss', 'Guernsey'],
    'Health': ['Healthy', 'Mastitis', 'Healthy', 'Healthy', 'Mastitis', 'Healthy'],
    'Milking_Frequency': ['2', '2', '2', '4', '2', '2',],
    'Living_Conditions': ['Good', 'Good', 'Bad', 'Good', 'Good', 'Great',],
    'Lactation_Stage': ['Early', 'Late', 'Mid', 'Dry', 'Early', 'Dry',],
    'Feed': ['Alfalfa', 'Grain', 'Grain', 'Corn', 'Barley', 'Barley',],
    'Yield': [50, 25, 12, 34, 80, 2,]
} 

# Dataframe 
df = pd.DataFrame(data)

# Amount of cows that can me milked at a time 

milking_capacity = 10 # 10 cows milked at a time 

# Creating the MILP problem 
lp_problem = pulp.LpProblem("Dairy_Milking_Schedule", pulp.LpMaximize)

# Create decision variables: whether a cow is selected for milking (binary: 1 = milking, or 0 = not milking)
cow_vars = pulp.LpVariable.dicts("Cow", df['Age_ID'], cat="Binary")

# Define the objective function: Maximize milk yields 
lp_problem += pulp.lpSum([cow_vars[row['Age_ID']] * row['Yield'] for idx, row in df.iterrows()])

# Constraints 
# 1. Milking capacity constraint: Only `milking_capacity` cows can be milked at the same time
lp_problem += pulp.lpSum([cow_vars[row['Age_ID']] for idx, row in df.iterrows()]) <= milking_capacity

# 2. Health priority: Cows with mastitis should be milked first (higher priority)
health_priority = {
    'Healthy': 1,
    'Mastitis': 3
}

# Cows with Mastitis should have higher priority for milking
lp_problem += pulp.lpSum([cow_vars[row['Age_ID']] * health_priority[row['Health']] for idx, row in df.iterrows()]) >= 1  # At least 1 mastitis cow should be milked

# 3. Lactation Stage: For simplicity, let's prioritize cows in the 'Early' and 'Mid' lactation stages.
lactation_priority = {
    'Early': 3,
    'Mid': 2,
    'Late': 1,
    'Dry': 0
}

# Add lactation stage priority
lp_problem += pulp.lpSum([cow_vars[row['Age_ID']] * lactation_priority[row['Lactation_Stage']] for idx, row in df.iterrows()]) >= 2  # At least 2 early or mid lactation cows should be milked

# Solve the MILP problem
lp_problem.solve()

# Print the results
print("MILP Optimization (Maximize Milk Yield):")
print(f"Status: {pulp.LpStatus[lp_problem.status]}")

# Display selected cows and their details
selected_cows = []
for cow_id, var in cow_vars.items():
    if pulp.value(var) == 1:
        selected_cows.append(df[df['Age_ID'] == cow_id])

# Output the selected cows for milking
if selected_cows:
    print("\nOptimal Milking Schedule:")
    for idx, row in pd.concat(selected_cows).iterrows():
        print(f"Cow {row['Age_ID']} (Breed: {row['Breed']}, Yield: {row['Yield']} liters) is selected for milking.")
else:
    print("\nNo cows were selected for milking based on the constraints.")

# Calculate the total milk yield
total_yield = sum([row['Yield'] for idx, row in pd.concat(selected_cows).iterrows()])
print(f"\nTotal Milk Yield: {total_yield} liters")
