import psycopg2

# Establish the connection
conn = psycopg2.connect(
    dbname="postgres", 
    user="root", 
    password="root", 
    host="localhost", 
    port="5432"
)

# Create a cursor object to interact with the database
cur = conn.cursor()

create_table_query = '''
CREATE TABLE "Cowlibrate" (
    id SERIAL PRIMARY KEY,
    milk_yield FLOAT NOT NULL,
    health VARCHAR(255) NOT NULL,
    lactation_stage VARCHAR(255) NOT NULL,
    breed VARCHAR(255) NOT NULL,
    enclosure_temp FLOAT,
    outside_temp FLOAT,
    country VARCHAR(255) NOT NULL,
    feed_type VARCHAR(255) NOT NULL,
    age INT NOT NULL
);
'''

# Execute the query
cur.execute(create_table_query)
# Execute the query with double quotes to preserve the case-sensitive table name
cur.execute('SELECT * FROM "Cowlibrate"')

# Fetch and print the results
rows = cur.fetchall()
for row in rows:
    print(row)

conn.commit()
# Close the connection
cur.close()
conn.close()

print("Table 'Cowlibrate' created successfully")