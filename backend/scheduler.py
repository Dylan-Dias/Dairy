import pulp
import pandas as pd


def optimize_milking_schedule(data, milking_capacity=10):
    # Create the MILP problem
    lp_problem = pulp.LpProblem("Dairy_Milking_Schedule", pulp.LpMaximize)

    # Convert data to a dataframe
    df = pd.DataFrame(data)

    # Decision variables
    cow_vars = pulp.LpVariable.dicts("Cow", df['Age_ID'], cat="Binary")

    # Objective function: Maximize milk yield
    lp_problem += pulp.lpSum([cow_vars[row['Age_ID']] * row['Yield'] for idx, row in df.iterrows()])

    # Constraints
    lp_problem += pulp.lpSum([cow_vars[row['Age_ID']] for idx, row in df.iterrows()]) <= milking_capacity  # Capacity
    lp_problem += pulp.lpSum([cow_vars[row['Age_ID']] * (row['Health'] == 'Mastitis') for idx, row in df.iterrows()]) >= 1  # At least 1 mastitis cow

    # Solve the problem
    lp_problem.solve()

    # Extract results
    selected_cows = [row['Age_ID'] for idx, row in df.iterrows() if pulp.value(cow_vars[row['Age_ID']]) == 1]
    total_yield = sum(row['Yield'] for idx, row in df.iterrows() if row['Age_ID'] in selected_cows)

    return {
        "selected_cows": selected_cows,
        "total_yield": total_yield,
        "status": pulp.LpStatus[lp_problem.status]
    }
