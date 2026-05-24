from dotenv import load_dotenv

import os, psycopg2

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / '.env')

try:
    connekt = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
    )
    curSor = connekt.cursor()
    print('Connected to the Database successfully')
except psycopg2.OperationalError as e:
    print(f'Something went wrong: {e}')

curSor.execute('''CREATE TABLE IF NOT EXISTS players_tbl(
            player_id bigserial PRIMARY KEY,  
            full_name text,
            date_of_birth date,
            weight numeric(5,2),
            height numeric(5,2),
            positions text
            );'''
            )

connekt.commit()

def add_player(curSor, connekt, name, dob, weight_input, height_input,position_input):
    curSor.execute(('''INSERT INTO players_tbl (full_name, date_of_birth, weight, height, positions)
            VALUES (%s, %s, %s, %s, %s) '''), (name, dob, weight_input, height_input,position_input))
    connekt.commit()
    print('Player registered.')

def remove_player(curSor,connekt,player_id):
    curSor.execute('DELETE FROM players_tbl WHERE player_id = %s', (player_id, ))
    connekt.commit()

curSor.execute('''CREATE TABLE IF NOT EXISTS performance_tbl(
            player_id bigint REFERENCES players_tbl(player_id),
            goals_scored integer,
            goals_saved integer,
            assists integer,
            clears integer,
            fouls_commited integer,
            passes_attempted integer,
            passes_completed integer,
            passing_accuracy numeric GENERATED ALWAYS AS 
               (ROUND((passes_completed * 100.0 / NULLIF(passes_attempted, 0)), 2)) STORED,
            remarks text
            );'''
            )

connekt.commit()

def record_performance(curSor, connekt, which_player, goals_scored, goals_saved, assists, clears, fouls, passes_made, passes_done, remarks):
    curSor.execute(('''INSERT INTO performance_tbl (player_id,goals_scored,goals_saved,assists,clears,fouls_commited,passes_attempted,passes_completed,remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s) '''), (which_player, goals_scored, goals_saved, assists, clears, fouls, passes_made, passes_done, remarks))
    connekt.commit()
    print('Performance Recorded.')

def view_performance(curSor):
    curSor.execute('''SELECT * FROM public.performance_tbl''')
    rows = curSor.fetchall()
    print(f"{'ID':<5} {'Goals Scored':<20} {'Goals Saved':<20} {'Assists':<20} {'Clears':<20} {'Fouls':<20} {'Total Passes':<20} {'Complete Passes':<20} {'Remarks':<30}")
    print("-" * 75)
    for row in rows:
         print(f"|{row[0]:<5} | {row[1]:<5} | {row[2]:<5} | {row[3]:<5} | {row[4]:<5} | {row[5]:<5} | {row[6]:<5} | {row[7]:<5} | {row[8]:<5} | {row[9]:<30} | ")

def update_performance(curSor,connekt):
    ask_pf_id = input("Enter the player id of the player to update:  ")
    pf_column_choice = int(input('''Where would you like to make changes?
                          1. Goals scored
                          2. Goals saved
                          3. Assists made
                          4. Clears done
                          5. Fouls commited
                          6. Passes attempted
                          7. Passes completed
                          8. Remarks about player
                          9. Exit
                          '''))
    while pf_column_choice != 9:    #goals_scored, goals_saved, assists, clears, fouls, passes_made, passes_done, remarks
        if (pf_column_choice) == 1: #goals_scored,goals_saved,assists,clears,fouls_commited,passes_attempted,passes_completed,remarks
            update_goals = input('Enter updated player goalscore: ') 
            curSor.execute("UPDATE performance_tbl SET goals_scored = %s WHERE player_id = %s", (update_goals, ask_pf_id))
        elif (pf_column_choice) == 2:
            update_saves = input('Enter updated player saves: ')
            curSor.execute("UPDATE performance_tbl SET goals_saved = %s WHERE player_id = %s", (update_saves, ask_pf_id))
        elif (pf_column_choice) == 3:
            assists = input("Enter updated player assists: ")
            curSor.execute("UPDATE performance_tbl SET assists = %s WHERE player_id = %s", (assists, ask_pf_id))
        elif (pf_column_choice) == 4:
            clears = input("Enter updated ball clears: " )
            curSor.execute("UPDATE performance_tbl SET clears = %s WHERE player_id = %s", (clears, ask_pf_id))
        elif (pf_column_choice) == 5:
            foul_record = input("Enter new fouls commited: ")
            curSor.execute("UPDATE performance_tbl SET fouls_commited = %s WHERE player_id = %s", (foul_record, ask_pf_id))
        elif (pf_column_choice) == 6:
            passes_total = input("Enter number of passes attempted : ")
            curSor.execute("UPDATE performance_tbl SET passes_attempted = %s WHERE player_id = %s", (passes_total, ask_pf_id))
        elif (pf_column_choice) == 7:
            successful_passes = input("Enter number of passes completed: ")
            curSor.execute("UPDATE performance_tbl SET passes_completed = %s WHERE player_id = %s", (successful_passes, ask_pf_id))
        elif (pf_column_choice) == 8:
            new_remarks = input("Enter your remarks about the player: ")
            curSor.execute("UPDATE performance_tbl SET remarks = %s WHERE player_id = %s", (new_remarks, ask_pf_id))
        else:
            print("Invalid Selection![Select from 1-9]")
        pf_column_choice = int(input('''Where would you like to make changes?
                          1. Goals scored
                          2. Goals saved
                          3. Assists made
                          4. Clears done
                          5. Fouls commited
                          6. Passes attempted
                          7. Passes completed
                          8. Remarks about player
                          9. Exit
                          '''))
        connekt.commit()

def remove_performance(curSor,connekt,player_id):
    curSor.execute('DELETE FROM performance_tbl WHERE player_id = %s', (player_id, ))
    connekt.commit()


