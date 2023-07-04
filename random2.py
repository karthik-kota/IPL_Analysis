import sqlite3
import pandas as pd

# df=pd.read_csv(r"all bowling stats.csv")

conn = sqlite3.connect('ipl.db')
cur = conn.cursor()

# for i in range(len(df)):
#   Pos = df.loc[i]['Pos']
#   player = df.loc[i]['Player']
#   team = df.loc[i]['Team']
#   matches = df.loc[i]['Matches']
#   inn = df.loc[i]['Inn']
#   Balls = df.loc[i]['Balls']
#   Wickets = df.loc[i]['Wickets']
#   Five_Ws = df.loc[i]['Five_Ws']
#   Year = df.loc[i]['Year']

#   cur.execute(f"insert into bowling values ('{Pos}','{player}','{team}','{matches}','{inn}','{Balls}','{Wickets}','{Five_Ws}','{Year}')")
 
#cur.execute('''create table batting(Pos int,Player varchar(50),Team varchar(50),Matches int,Inn int,Runs int,Strike_Rate float,Fours int,Sixes int)''')
#cur.execute('ALTER TABLE batting ADD COLUMN Year int')
#cur.execute('''create table bowling(Pos int,Player varchar(50),Team varchar(50),Matches int,Inn int,Balls int,Wickets int,Five_Ws int,Year int)''')
cur.execute('select * from batting')
#conn.commit()



