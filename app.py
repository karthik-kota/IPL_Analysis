import sqlite3
from flask import Flask, jsonify, request, render_template
import seaborn as sns
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np


app = Flask(__name__)

@app.route('/')
def home():  
    return render_template('index.html')
#=====================================================================
@app.route("/show-batting")
def batting_show():
    conn = sqlite3.connect('ipl.db')
    cn=conn.cursor()
    cn.execute('select * from batting')
    data=[]
    for i in cn.fetchall():
        bplayer={}
        bplayer['Pos'] = i[0]
        bplayer['Player'] = i[1]
        bplayer['Team'] = i[2]
        bplayer['Matches'] = i[3]
        bplayer['Inn'] = i[4]
        bplayer['Runs'] = i[5]
        bplayer['Strike Rate'] = i[6]
        bplayer['Fours'] = i[7]
        bplayer['Sixes'] = i[8]
        bplayer['Year'] = i[9]
        data.append(bplayer)
    #print(data)
    return render_template('show-batting.html',data = data)
#=============================================================================
@app.route("/show-bowling")
def bowling_show():
    conn = sqlite3.connect('ipl.db')
    cn=conn.cursor()
    cn.execute('select * from bowling')
    data=[]
    for i in cn.fetchall():
        bplayer={}
        bplayer['Pos'] = i[0]
        bplayer['Player'] = i[1]
        bplayer['Team'] = i[2]
        bplayer['Matches'] = i[3]
        bplayer['Inn'] = i[4]
        bplayer['Balls'] = i[5]
        bplayer['Wickets'] = i[6]
        bplayer['Five_Ws'] = i[7]
        bplayer['Year'] = i[8]
        data.append(bplayer)
    #print(data)
    return render_template('show-bowling.html',data = data)

@app.route('/Compare-Players', methods=['GET', 'POST'])
def compareinn():
    return render_template('compare.html')

#====================================Top 5 Four========================================
@app.route('/Four-Players', methods=['GET', 'POST'])
def topfour():
    conn = sqlite3.connect('ipl.db')
    cn = conn.cursor()
    df = pd.read_sql_query('SELECT * FROM batting', conn)

    if request.method == 'POST':
        selected_year = request.form.get('select-year')
        if selected_year:
            year = df[df['Year'] == int(selected_year)]
            g = year.groupby('Player').sum()
            x = g.sort_values(by='Fours', ascending=False).head()
            
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.barplot(y=x.index, x=x['Fours'], ax=ax)
            
            image_stream = io.BytesIO()
            fig.savefig(image_stream, format='png')
            image_stream.seek(0)

            encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

            return render_template('graphindex.html', graph=encoded_image)

    default_year = 2021
    year = df[df['Year'] == default_year]
    g = year.groupby('Player').sum()
    x = g.sort_values(by='Fours', ascending=False).head()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(y=x.index, x=x['Fours'], ax=ax)
    
    image_stream = io.BytesIO()
    fig.savefig(image_stream, format='png')
    image_stream.seek(0)

    encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return render_template('graphindex.html', graph=encoded_image, default_year=default_year)



#=============================Indivual player batting===================================================
@app.route('/playeranalysis', methods=['GET', 'POST'])
def panalysis():
    conn = sqlite3.connect('ipl.db')
    cn = conn.cursor()
    player_names = pd.read_sql_query('SELECT Player FROM batting', conn)['Player'].tolist()
    
    selected_player = request.form.get('search-player')
    if selected_player is None:
        selected_player = player_names[0]  # Default selected player
    
    df = pd.read_sql_query('SELECT * FROM batting', conn)
    x = df[df['Player'] == selected_player]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=x['Year'], y=x['Runs'], ax=ax)
    
    # Save the plot image to a BytesIO object
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the plot image to base64
    encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    
    return render_template('Indivualbatting.html', graph=encoded_image, player_names=player_names, selected_player=selected_player)

#=============================Indivual Player bowling===============================
@app.route('/Indbowling', methods=['GET', 'POST'])
def Indibowling():
    conn = sqlite3.connect('ipl.db')
    cn = conn.cursor()
    player_names = pd.read_sql_query('SELECT Player FROM bowling', conn)['Player'].tolist()
    
    selected_player = request.form.get('search-player')
    if selected_player is None:
        selected_player = player_names[0]  # Default selected player
    
    df = pd.read_sql_query('SELECT * FROM bowling', conn)
    x = df[df['Player'] == selected_player]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=x['Year'], y=x['Wickets'], ax=ax)
    
    # Save the plot image to a BytesIO object
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the plot image to base64
    encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')
    
    return render_template('Indivualbowling.html', graph=encoded_image, player_names=player_names, selected_player=selected_player)
#============================Top 5 Players Sixes==============================

@app.route('/topsixes', methods=['GET', 'POST'])
def topfivesixes():
    conn = sqlite3.connect('ipl.db')
    cn = conn.cursor()
    data = pd.read_sql_query('SELECT * FROM batting', conn)
    
    selected_year = request.args.get('year')
    if selected_year:
        y = data[data['Year'] == int(selected_year)]
    else:
        selected_year = "2021"  # Set default year if no selection is made
        y = data[data['Year'] == int(selected_year)]
    
    g = y.groupby('Player').sum()
    sor = g.sort_values(by='Sixes', ascending=False).head()
    
    # Check if data is available
    if not sor.empty:
        plt.figure(figsize=(12, 8))
        sns.barplot(x=sor['Sixes'], y=sor.index)
        plt.xlabel('Sixes', fontsize=25)
        plt.ylabel('Player', fontsize=25)
        plt.title(f'Top Players by Sixes in {selected_year} IPL', fontsize=25)
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        plot_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        return render_template('sixes.html', graph=plot_image, default_year=selected_year)
    else:
        return render_template('sixes.html', default_year=selected_year)

#===============================Top 5 player based on Wickets===============

@app.route('/topWickets', methods=['GET', 'POST'])
def topfivewickets():
    conn = sqlite3.connect('ipl.db')
    cn = conn.cursor()
    data = pd.read_sql_query('SELECT * FROM bowling', conn)
    
    selected_year = request.args.get('year')
    if selected_year:
        ys = data[data['Year'] == int(selected_year)]
    else:
        selected_year = "2021"  # Set default year if no selection is made
        ys = data[data['Year'] == int(selected_year)]
    
    gs = ys.groupby('Player').sum()
    so = gs.sort_values(by='Wickets', ascending=False).head()

    
    # Check if data is available
    if not so.empty:
        plt.figure(figsize=(23, 16))
        sns.barplot(x=so['Wickets'], y=so.index)
        plt.xlabel('Wickets', fontsize=25)
        plt.ylabel('Player', fontsize=20)
        plt.title(f'Top Players by Wickets in {selected_year} IPL', fontsize=25)

        # Set the font size of y-axis labels
        #plt.yticks(fontsize=30)
        plt.gca().tick_params(axis='y', labelsize=20)
    
        # Set the font size of x-axis labels
        plt.gca().tick_params(axis='x', labelsize=20)
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        plot_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        return render_template('Wickets.html', graph=plot_image, default_year=selected_year)
    else:
        return render_template('Wickets.html', default_year=selected_year)
    
#==========================Compare Players battind===============================
@app.route('/compareplayer', methods=['GET', 'POST'])
def battingcompare():
    conn = sqlite3.connect('ipl.db')
    cn = conn.cursor()
    df = pd.read_sql_query('SELECT Player, Runs, Strike_Rate FROM batting', conn)

    # Get the player names from the database
    player_names = pd.read_sql_query('SELECT Player FROM batting', conn)['Player'].tolist()

    # Get the selected players from the dropdowns
    player1 = request.form.get('dropdown1')
    player2 = request.form.get('dropdown2')

    # Filter the DataFrame for selected players
    filtered_df = df[df['Player'].isin([player1, player2])]

    if filtered_df.empty:
        return render_template('comparebatting.html', player_names=player_names)

    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Set the width of each bar
    bar_width = 0.35

    # Get unique players for x-axis labels
    unique_players = filtered_df['Player'].unique()

    # Create the x-axis positions for the bars
    x = np.arange(len(unique_players))

    # Initialize empty arrays for runs and strike rate values
    runs_values = np.zeros(len(unique_players))
    strike_rate_values = np.zeros(len(unique_players))

# Fill the runs and strike rate values arrays
    for i, player in enumerate(unique_players):
        runs_values[i] = filtered_df.loc[filtered_df['Player'] == player, 'Runs'].values[0]
        strike_rate_values[i] = filtered_df.loc[filtered_df['Player'] == player, 'Strike_Rate'].values[0]


    # Plot the bars for runs and strike rate
    runs_bars = plt.bar(x - bar_width/2, runs_values, width=bar_width, align='center', color='blue', alpha=0.7, label=f'{player1} - Runs')
    strikerate_bars = plt.bar(x + bar_width/2, strike_rate_values, width=bar_width, align='center', color='red', alpha=0.7, label=f'{player2} - Strike Rate')

    # Set the x-axis tick labels
    plt.xticks(x, unique_players)

    # Set the labels and title
    plt.xlabel('Player')
    plt.ylabel('Runs / Strike Rate')
    plt.title('Runs and Strike Rate for Selected Players')
    plt.legend()

    # Add value labels on top of each bar
    for bar1, bar2 in zip(runs_bars, strikerate_bars):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        plt.text(bar1.get_x() + bar1.get_width() / 2, height1, int(height1), ha='center', va='bottom')
        plt.text(bar2.get_x() + bar2.get_width() / 2, height2, int(height2), ha='center', va='bottom')

    # Save the plot to a buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # Encode the plot image as base64
    plot_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    return render_template('comparebatting.html', plot_image=plot_image, player_names=player_names)

#======================Compare Players bowlings=============================================
@app.route('/comparebowling', methods=['GET', 'POST'])
def bowlingcompare():
    conn = sqlite3.connect('ipl.db')
    cn = conn.cursor()
    df = pd.read_sql_query('SELECT Player, Matches, Wickets FROM bowling', conn)

    # Get the player names from the database
    player_names = pd.read_sql_query('SELECT Player FROM bowling', conn)['Player'].tolist()

    # Get the selected players from the dropdowns
    player1 = request.form.get('dropdown1')
    player2 = request.form.get('dropdown2')

    # Filter the DataFrame for selected players
    filtered_df = df[df['Player'].isin([player1, player2])]

    if filtered_df.empty:
        return render_template('comparebowling.html', player_names=player_names)

    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Set the width of each bar
    bar_width = 0.35

    # Get unique players for x-axis labels
    unique_players = filtered_df['Player'].unique()

    # Create the x-axis positions for the bars
    x = np.arange(len(unique_players))

    # Initialize empty arrays for runs and strike rate values
    runs_values = np.zeros(len(unique_players))
    strike_rate_values = np.zeros(len(unique_players))

# Fill the runs and strike rate values arrays
    for i, player in enumerate(unique_players):
        runs_values[i] = filtered_df.loc[filtered_df['Player'] == player, 'Matches'].values[0]
        strike_rate_values[i] = filtered_df.loc[filtered_df['Player'] == player, 'Wickets'].values[0]


    # Plot the bars for runs and strike rate
    runs_bars = plt.bar(x - bar_width/2, runs_values, width=bar_width, align='center', color='blue', alpha=0.7, label=f'{player1} - Matches')
    strikerate_bars = plt.bar(x + bar_width/2, strike_rate_values, width=bar_width, align='center', color='red', alpha=0.7, label=f'{player2} - Wickets')

    # Set the x-axis tick labels
    plt.xticks(x, unique_players)

    # Set the labels and title
    plt.xlabel('Player')
    plt.ylabel('Matches / Wickets')
    plt.title('Matches and Wickets Rate for Selected Players')
    plt.legend()

    # Add value labels on top of each bar
    for bar1, bar2 in zip(runs_bars, strikerate_bars):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        plt.text(bar1.get_x() + bar1.get_width() / 2, height1, int(height1), ha='center', va='bottom')
        plt.text(bar2.get_x() + bar2.get_width() / 2, height2, int(height2), ha='center', va='bottom')

    # Save the plot to a buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # Encode the plot image as base64
    plot_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    return render_template('comparebowling.html', plot_image=plot_image, player_names=player_names)



if __name__ == '__main__':
    app.run()















