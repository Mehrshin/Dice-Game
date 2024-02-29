import random
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import flash
app = Flask(__name__)
app.secret_key = '12345' 

player1_name = ""
player2_name = ""
current_player = ""
player1_points = 0
player2_points = 0
dice_result = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    global player1_name, player2_name, current_player, player1_points, player2_points, dice_result

    player1_name = request.form['player1Name']
    player2_name = request.form['player2Name']
    current_player = player1_name
    player1_points = 0
    player2_points = 0
    dice_result = 0
    
    flash('Game has started!')
    return render_template('game.html', player1=player1_name, player2=player2_name, current_player=current_player, player1_points=player1_points, player2_points=player2_points, dice_result=dice_result)


@app.route('/roll_dice', methods=['POST'])
def roll_dice():
    global current_player, player1_points, player2_points, dice_result

    dice_result = roll_dice_result()

    if dice_result == 1:
        reset_current_player_score()
        flash(f"{current_player} rolled a 1, so they lost their turn!")
        switch_player()
    else:
        update_score(dice_result)
        
    if check_winner():
        flash(f"{current_player} is the winner!")
        return redirect(url_for('show_winner'))
    return render_template('game.html', player1=player1_name, player2=player2_name, current_player=current_player, player1_points=player1_points, player2_points=player2_points, dice_result=str(dice_result))

@app.route('/hold', methods=['POST'])
def hold():
    global current_player
    switch_player()
    if check_winner():
        return redirect(url_for('show_winner'))
    return render_template('game.html', player1=player1_name, player2=player2_name, current_player=current_player, player1_points=player1_points, player2_points=player2_points)

def roll_dice_result():
    return random.randint(1, 6)


def switch_player():
    global current_player
    if current_player == player1_name:
        current_player = player2_name
    else:
        current_player = player1_name
        

def update_score(score):
    global current_player, player1_points, player2_points
       
    if current_player == player1_name:
        player1_points += score
    else:
        player2_points += score
        
    check_winner()
    
def reset_current_player_score():
    global current_player, player1_points, player2_points

    if current_player == player1_name:
        player1_points = 0
    else:
        player2_points = 0

def check_winner():
    global player1_name, player2_name, player1_points, player2_points
    
    if player1_points >= 20 or player2_points >= 20:
        winner = player1_name if player1_points >= 20 else player2_name
        flash(f"{winner} is the winner!")
        return True
        # return redirect(url_for('login'))
    return False

@app.route('/winner')
def show_winner():
    return render_template('winner.html', winner=player1_name if player1_points >= 20 else player2_name, player1=player1_name, player2=player2_name, current_player=current_player, player1_points=player1_points, player2_points=player2_points)



if __name__ == '__main__':
    app.run()


