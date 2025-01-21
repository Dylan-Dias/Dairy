from flask import Flask, render_template, request
import pulp
import pandas as pd
import io
import contextlib
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def dashboard():
    solver_output = None  # ! Initialize variable to store solver output
    cows_data = None

    if request.method == 'POST':
        # ! Extract data from form
        cow_ids = request.form.getlist('cow_id')
        milk_yields = request.form.getlist('milk_yield')
        health_statuses = request.form.getlist('health')
        lactation_stages = request.form.getlist('lactation_stage')
        breeds = request.form.getlist('breed')
        enclosure_temps = request.form.getlist('enclosure_temp')
        outside_temps = request.form.getlist('outside_temp')
        countries = request.form.getlist('country')
        feeds = request.form.getlist('feed')
        ages = request.form.getlist('age')

        # ! Create DataFrame
        data = {
            'Cow_ID': [int(cid) for cid in cow_ids],
            'Milk_Yield_Liters': [float(my) for my in milk_yields],
            'Health': health_statuses,
            'Lactation_Stage': lactation_stages,
            'Breed': breeds,
            'Enclosure_Temperature': [float(temp) if temp.strip().replace('.', '', 1).isdigit() else 0.0 for temp in enclosure_temps],
            'Outside_Temperature': [float(temp) for temp in outside_temps],
            'Country': countries,
            'Feed_Type': feeds,
            'Age': [int(age) for age in ages],
            'Feed_Quant': [float(feed) if feed.strip().replace('.','', 1).isdigit() else 0.0 for feed in feed_quant],
            'Time_Milk': time_milk, # Assumption is a list of time values
        }

        df = pd.DataFrame(data)

        # ! Define parameters
        milking_capacity = 10  # ! Number of cows that can be milked at a time

        # ! Create MILP problem
        lp_problem = pulp.LpProblem("Dairy_Milking_Schedule", pulp.LpMaximize)
        cow_vars = pulp.LpVariable.dicts("Cow", df['Cow_ID'], cat="Binary")

        # ! Objective function: Maximize milk yield
        feed_impact = {'Corn': 1.1, 'Alfalfa': 1.05, 'Grass': 0.9}
        lp_problem += pulp.lpSum([
            cow_vars[row['Cow_ID']] * row['Milk_Yield_Liters'] * feed_impact.get(row['Feed_Type'], 1.0)
            for idx, row in df.iterrows()
            ])

        # ! Constraints
        lp_problem += pulp.lpSum([cow_vars[row['Cow_ID']] for idx, row in df.iterrows()]) <= milking_capacity

        # ! Example constraint: prioritize healthy cows
        health_priority = {'Healthy': 1, 'Mastitis': 0}
        lp_problem += pulp.lpSum([cow_vars[row['Cow_ID']] * health_priority[row['Health']] for idx, row in df.iterrows()]) >= 1

        # ! Capture solver output
        with io.StringIO() as buffer, contextlib.redirect_stdout(buffer):
            lp_problem.solve()
            solver_output = buffer.getvalue()  # ! Store solver output

        # ! Gather selected cows and their details
        selected_cows = [df[df['Cow_ID'] == cow_id] for cow_id, var in cow_vars.items() if pulp.value(var) == 1]
        cows_data = pd.concat(selected_cows) if selected_cows else None


    return render_template(
        'dashboard.html',
        cows=cows_data.to_dict(orient='records') if cows_data is not None else None,
        solver_output=solver_output
    )

if __name__ == '__main__':
    app.run(debug=True)


# ! Code for File Upload
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file is provided in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    try:
        # Process CSV or Excel file
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
        elif file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            return jsonify({'error': 'Unsupported file format. Please upload a CSV or Excel file.'}), 400
        
        # Extract the first row as JSON data
        data = df.iloc[0].to_dict()
        return jsonify(data)

    except Exception as e:
        return jsonify({'error': f'Failed to process file: {e}'}), 500
 