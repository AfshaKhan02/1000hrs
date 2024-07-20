import streamlit as st
import sqlite3
from datetime import datetime

# Initialize database connection
conn = sqlite3.connect('progress.db')
c = conn.cursor()

# Create table if not exists
c.execute('''
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_title TEXT,
    total_hours INTEGER,
    hours_spent REAL DEFAULT 0,
    last_updated TIMESTAMP
)
''')
conn.commit()
 



# Title of the Streamlit app
st.title('Goal Progress Tracker')

# Step 1: Input goal title
goal_title = st.text_input('Enter your goal title (e.g., Python, Data Science):')

# Step 2: Select total hours for the goal
total_hours = st.selectbox('Select total hours for this goal:', [1, 10, 100, 1000, 10000])

# Step 3: Add the goal to the database
if st.button('Add Goal'):
    if goal_title and total_hours:
        c.execute('INSERT INTO progress (goal_title, total_hours, last_updated) VALUES (?, ?, ?)', 
                  (goal_title, total_hours, datetime.now()))
        conn.commit()
        st.success('Goal added!')

# Display existing goals and their progress
st.header('Your Goals')
c.execute('SELECT id, goal_title, total_hours, hours_spent FROM progress')
goals = c.fetchall()

for goal in goals:
    goal_id, goal_title, total_hours, hours_spent = goal
    st.subheader(goal_title)
    st.text(f'Progress: {hours_spent}/{total_hours} hours')

    # Timer
    hours, minutes = st.columns(2)
    with hours:
        input_hours = st.number_input('Hours', min_value=0, max_value=23, step=1, key=f'{goal_id}_hours')
    with minutes:
        input_minutes = st.number_input('Minutes', min_value=0, max_value=59, step=1, key=f'{goal_id}_minutes')
    
    if st.button(f'Update {goal_title}', key=f'{goal_id}_update'):
        time_spent = input_hours + input_minutes / 60
        new_hours_spent = hours_spent + time_spent
        c.execute('UPDATE progress SET hours_spent = ?, last_updated = ? WHERE id = ?', 
                  (new_hours_spent, datetime.now(), goal_id))
        conn.commit()
        st.success(f'{goal_title} updated!')
        st.experimental_rerun()
