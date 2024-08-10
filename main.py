import datetime

from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, jsonify
import os
import sqlite3
# import time
from sqlalchemy import Table, Column ,create_engine , String, ForeignKey
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase , sessionmaker, Mapped, mapped_column, relationship
import requests
from flask_restful import Api, Resource
from googletrans import LANGUAGES
import os, os.path
from flask_mail import Mail, Message
from time import sleep
from jinja2 import Environment, FileSystemLoader
import random
import logging
from logging.handlers import TimedRotatingFileHandler
import requests
from flask import send_file
import matplotlib.pyplot as plt
import io
from datetime import datetime

engine = create_engine("sqlite:///default.db", echo=False)

Session = sessionmaker(bind=engine)
#owm key: f68c228a96e5e4ece4a10a990838364c


class Base(DeclarativeBase):
    def createdb(self):
        Base.metadata.create_all(engine)

    def dropdb(self):
        Base.metadata.drop_all(engine)

logging.basicConfig(filename=f'logs/{datetime.now().strftime("%d.%m.%Y")}.log', level=logging.INFO)

app = Flask(__name__)
api = Api(app)

def configure_logging():
    # Clear existing handlers to avoid duplicate logging
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    # Configure a new handler with the desired filename
    handler = TimedRotatingFileHandler(filename=f"logs/{datetime.now().strftime("%d.%m.%Y")}.log", when='midnight', interval=1, backupCount=7)
    handler.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    app.logger.addHandler(handler)

configure_logging()


app.config['CATEGORIES'] = ['Action', 'Adventure', 'RPG']
app.config['SECRET_KEY'] = "SUSSY-BAKA"
app.config['PERMANENT_SESSION_LIFETIME'] = 36000
app.config['MAIL_SERVER'] = 'smtp.ukr.net'

app.config['MAIL_PORT'] = 465

app.config['MAIL_USERNAME'] = "dregoscat@ukr.net"

app.config['MAIL_PASSWORD'] = "7ucXCWAlYXxRYGsV"

app.config['MAIL_DEFAULT_SENDER'] = "dregoscat@ukr.net"

app.config['MAIL_USE_TLS'] = False

app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.app_context().push()




from collections import defaultdict


# Dictionary to hold visit count per date
visit_count = defaultdict(int)



@app.route('/stats')
def stats():
    # Generate a bar chart
    fig, ax = plt.subplots()
    dates = sorted(visit_count.keys())
    counts = [visit_count[date] for date in dates]
    
    ax.bar(dates, counts)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Visits')
    ax.set_title('Number of Visits by Date')
    plt.xticks(rotation=45, ha='right')  # Rotate date labels for better readability

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')



class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    private: Mapped[bool] = mapped_column()
    profile_picture: Mapped[str] = mapped_column(String(100))
    # pl_id: Mapped[str] = mapped_column(String(50),ForeignKey('pl.id'))

# class Pl(Base):
#     __tablename__ = 'pl'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     html_path: Mapped[str] = mapped_column(String(100)) # path to html file with description, images, structure, crafts (like for minecraft), etc.
    


class Game(Base):
    __tablename__ = 'game'
    name: Mapped[str] = mapped_column(String(50), primary_key=True)
    image_path: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(500))
    html_path: Mapped[str] = mapped_column(String(100)) # path to html file with description, images, structure, crafts (like for minecraft), etc.


class Notes(Base):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(primary_key=True)
    game: Mapped[str] = mapped_column(ForeignKey('game.name'))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    note: Mapped[Optional[str]] = mapped_column(String(100000))


class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    game: Mapped[str] = mapped_column(ForeignKey('game.name'))
    username: Mapped[str] = mapped_column(ForeignKey('users.username'))
    date: Mapped[str] = mapped_column(String(100))
    time: Mapped[str] = mapped_column(String(100))
    comment: Mapped[str] = mapped_column(String(1000))
    profile_picture: Mapped[str] = mapped_column(String(100))


class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(primary_key=True)
    game: Mapped[str] = mapped_column(ForeignKey('game.name'))
    category: Mapped[str] = mapped_column()


class Lib_item(Base):
    __tablename__ = 'library'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(String(50), ForeignKey('game.name'))



def removeFromLib(user_id, name):
    with Session() as session:
        lib_item = session.query(Lib_item).filter_by(user_id=user_id, name=name).first()
        session.delete(lib_item)
        session.commit()

def selectNote(user_id):
    with Session() as session:
        return session.query(Notes).filter_by(user_id=user_id).first()

def newNote(game, user_id):
    with Session() as session:
        new_note = Notes(game=game, user_id=user_id)
        session.add(new_note)
        session.commit()

def selectNotes(user_id):
    with Session() as session:
        return session.query(Notes).filter_by(user_id=user_id).all()

def updateNote(note, id):
    with Session() as session:
        print(id)
        student = session.query(Notes).filter_by(id=id).first()
        student.note = note
        session.commit()

def newGame(name, image_path, description, html_path):
    with Session() as session:
        new_game = Game(name=name, image_path=image_path, description=description, html_path=html_path)
        session.add(new_game)
        session.commit()
        
def newCategory(game, category):
    with Session() as session:
        new_category = Category(game=game, category=category)
        session.add(new_category)
        session.commit()
        
def newLibItem(user_id, name):
    with Session() as session:
        new_lib_item = Lib_item(user_id=user_id, name=name)
        session.add(new_lib_item)
        session.commit()

def newUser(email, username, password, private, profile_picture):
    with Session() as session:
        new_user = Users(username=username, email=email, password=password, private=private, profile_picture=profile_picture)
        session.add(new_user)
        session.commit()

def newComment(game, username, comment, profile_picture):
    with Session() as session:
        date = datetime.datetime.now().strftime("%d.%m.%Y")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        new_comment = Comment(game=game, username=username, date=date, time=time, comment=comment, profile_picture=profile_picture)
        session.add(new_comment)
        session.commit()

def selectComments(game):
    with Session() as session:
        return session.query(Comment).filter_by(game=game).all()

def selectUsers():
    with Session() as session:
        return session.query(Users).all()
    
def selectUser(email):
    with Session() as session:
        return session.query(Users).filter_by(email=email).first()
    
def selectGames():
    with Session() as session:
        return session.query(Game).all()
    
def selectGamebyName(name):
    with Session() as session:
        return session.query(Game).filter_by(name=name).first()
    
def selectGamesByCategory(category):
    with Session() as session:
        categories = session.query(Category).filter_by(category=category).all()
    
        games = []
        for i in categories:
            sgames = session.query(Game).filter_by(name=i.game).all()
            games.append(sgames)
        return games
    
def selectGamesByLib(id):
    with Session() as session:
        lib = session.query(Lib_item).filter_by(user_id=id).all()
        games = []
        for game in lib:
            g = session.query(Game).filter_by(name=game.name).first()
            games.append(g)

        return games
            

def selectCategories():
    with Session() as session:
        return session.query(Category).all()

def selectCategoriesByGame(game):
    with Session() as session:

        return session.query(Category).filter_by(game=game).all()
    
def selectLibItems():
    with Session() as session:
        return session.query(Lib_item).all()
def selectLibItemsById(id, game):
    with Session() as session:
        return session.query(Lib_item).filter_by(user_id=id, name=game).all()
    
def selectGamesByQuery(query:str, categories:list):
    with Session() as session:
        kns = [] #kns = keynames
        kws = [] # kws = description keywords
        games = []
        query = query.lower()
        broke = False
        qcategories = []
        for i in session.query(Game).all():
            for q in session.query(Category).filter_by(game=i.name).all():
                qcategories.append(q.category)
                
                for k in categories:
                    if k in qcategories:
                        
                        continu = True
                    else:
                        continu = False
                        
                        break
                try:
                    print(qcategories)
                    print(categories)
                    print(continu)
                except:
                    pass
                
                try:
                    if query == '' and q.category == '':
                        qcategories = []
                        q.category = ''
                        query = ''
                        categories = []
                        broke = True
                        break
                
                    elif query == '' and continu:
                        games.append(i)
                    elif continu:
                        for j in query.lower().split(" "):
                            if j in i.description.lower():
                                print('ok1')
                                kws.append(j)
                                games.append(i)

                        else:
                            if query.lower() in i.name.lower():
                                print('ok2')
                                kns.append(i.name)
                                games.append(i)
                    
                        
                    else:
                        continue
                except:
                    if query:
                        for j in query.lower().split(" "):
                            if j in i.description.lower():
                                print('ok1')
                                kws.append(j)
                                games.append(i)
                        if query.lower() in i.name.lower():
                            print('ok2')
                            kns.append(i.name)
                            games.append(i)
                    pass
            if broke:
                broke = False
                break
            unique_list = list(dict.fromkeys(games))
            print(unique_list)
        res = {'games':unique_list, 'criteries':{'kws':kws, 'kns':kns, 'categories':categories}} #ex. {'games':['Rust', 'Minecraft'], 'criteries':{ 'kws':['survival], 'kns':[] 'categiries':['Adventure']}}
        return res
# print(selectGamesByQuery("ru", ['Adventure']))
            
    

def updateInfo(username, email, password):
    with Session() as sessionn:
        sessionn.query(Users).filter_by(email=email).update({'username':username, 'email':email, 'password':password})
        sessionn.commit()
        

def generate_token():
    token = ""
    rnd_str = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(32):
        token += random.choice(rnd_str)
    print('1111111111111111111111')
    print(session.get('token'))
    session['token'] = token
    print(session['token'])
    print('1111111111111111111111')
    return token


def send_forgot_password(email):
    link = "http://127.0.0.1:5000/reset-password?email=" + email + "&token=" + generate_token()
    msg = Message("Password Reset", recipients=[email])
    msg.body = "Click the link below to reset your password:"
    msg.html = "<a href='" + link + "'>Click here</a>"
    mail.send(msg)
    return True


def updatePassword(email, password):
    with Session() as sessionn:
        sessionn.query(Users).filter_by(email=email).update({'password':password})
        sessionn.commit()


def update_profil_info(name, id, info, psevdo):
    with Session() as session:
        session.commit()

        indexnw = session.query(User_profil).filter_by(us_id=id).first()
        if indexnw:
            if info:
                indexnw.user_info=info
            if name:
                indexnw.user_name=name
            if psevdo:
                indexnw.user_psevdo=psevdo

        else:
            new_user = User_profil(user_name=name, us_id=id, user_info=info, user_psevdo=psevdo)
            session.add(new_user)
        session.commit()

def Select_us_ptofil(us_id):
    with Session() as session:
        info = session.query(User_profil).filter_by(us_id = us_id).first()
        print(info)
        if info:
            return info
        else:
            return None




@app.route("/prot3", methods = ["POST"])
def prot3():
    response_data = []
    us_n = request.form["us_n"]
    us_p = request.form["psevdo"]
    us_t = request.form["us_text"]

    profil_check = Select_us_ptofil(session["USER_ID"])

    if profil_check and (us_n or us_p or us_t):
        update_profil_info(us_n,session["USER_ID"],us_t,us_p)
        profil_ino = Select_us_ptofil(session["USER_ID"])
        print(profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id)
        print("profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id 111111111111111111111111111111111111111")
        data = {
            'u_nme': profil_ino.user_name,
            'psevdo': profil_ino.user_psevdo,
            'u_info': profil_ino.user_info,
            'id_u': profil_ino.us_id
        }
        response_data.append(data)

    elif profil_check:
        profil_ino = Select_us_ptofil(session["USER_ID"])
        print(profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id)
        print("profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id22222222222222222222222222222222222222222222222222222222")
        data = {
            'u_nme': profil_ino.user_name,
            'psevdo': profil_ino.user_psevdo,
            'u_info': profil_ino.user_info,
            'id_u': profil_ino.us_id
        }
        response_data.append(data)

    elif us_n or us_p or us_t:
        update_profil_info(us_n,session["USER_ID"],us_t,us_p)
        print("profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id3333333333333333333333333333333333333333333333333333333")
        profil_ino = Select_us_ptofil(session["USER_ID"])
        data = {
            'u_nme': profil_ino.user_name,
            'psevdo': profil_ino.user_psevdo,
            'u_info': profil_ino.user_info,
            'id_u': profil_ino.us_id
        }
        response_data.append(data)

    elif profil_check == None and (us_n == None or us_p == None or us_t == None):
        print("profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id444444444444444444444444444444444444444444444444444444444444")

        data = {
            'u_nme': "Нічого не знайдено",
            'psevdo': "Нічого не знайдено",
            'u_info': "Нічого не знайдено, та ви можите записати інформацію про себе по кнопці знизу",
            'id_u': session["USER_ID"]
        }
        response_data.append(data)

    else:
        print(
            "profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id5555555555555555555555555555555555555555555555555555555555555555555")
        # ТУТ МАЄ БУТИ ЯКАСЬ ФУНКЦІ ЩОБ ВЗЯТИ ДАНІ ПРО БІБЛІОТЕКУ Я ПРОСТО З НИМИ НЕ ОСОБЛИВО РОЗІБРАВСЯ
        # І ПОТІМ ІНФОРМАЦІЯ З ФУНКЦІЇ ПЕРЕДАЄТЬСЯ В JAVA SCRIPT
        # ps_inf = function_to_get_element()
        # for i in ps_inf:
        #     encoded_image = base64.b64encode(i[4]).decode('utf-8') #число 4 це порядковий індекс фотки
        #     data = {
        #         'image': f'data:image/jpeg;base64,{encoded_image}',
        #         'game_href': link,
        #         'game_description': "game_description",
        #     }
        #     response_data.append(data)

    return jsonify({"message": response_data}), 200

def removeNote(id):
    with Session() as session:
        print(id)
        student = session.query(Notes).filter_by(id=id).first()
        session.delete(student)
        session.commit()

@app.route("/<nothing>")
def nothing(nothing):

    # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    return render_template('nothing.html', reg=session.get('reg'), id=selectUser(session.get('email')).id)

@app.route("/mushrooms/<path:filename>")
def send_mushrooms(filename):
    return send_from_directory('mushrooms', filename)


@app.route("/capybara/<path:filename>")
def send_capybara(filename):
    return send_from_directory('capybara', filename)

@app.route("/gamecontent/<path:gamename>/<path:filename>")
def send_gamecontent(gamename, filename):
    return send_from_directory('gamecontent/'+gamename, filename)

@app.route("/gameicons/<path:filename>")
def send_gameicons(filename):
    return send_from_directory('gameicons', filename)

@app.route("/images/<path:filename>")
def send_images(filename):
    return send_from_directory('images', filename)

@app.route("/games/<path:filename>")
def send_games(filename):
    return send_from_directory('games', filename)

@app.route("/profile-images/<path:filename>")
def send_profile_images(filename):
    return send_from_directory('profile-images', filename)

@app.route("/static/<path:filename>")
def send_static(filename):
    return send_from_directory('static', filename)

#--------------------------------------------------------------------------------------------------
@app.route("/notes", methods=['GET','POST'])
def notes():
     # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    if request.method == 'GET':
        if session.get('reg') == True:
            games = selectGames()
            notes = selectNotes(selectUser(session.get('email')).id)

            return render_template('notes.html', notes=notes, games=games, count=len(notes))
        else:
            return render_template('nothing.html', reg=session.get('reg'), id=selectUser(session.get('email')).id)
    elif request.method == 'POST':
        try:
            if session.get('reg') == True:
                us = selectUser(session.get('email'))
                games = selectGames()
                
                print('id: ',request.form.get('id'))
                removeNote(request.form.get('id'))
                notes = selectNotes(us.id)
                return render_template('notes.html', notes=notes, games=games, count=len(notes), success='successfully deleted')
            else:
                return render_template('nothing.html', reg=session.get('reg'), id=selectUser(session.get('email')).id)
        except:
            print('F*ck you!')
            us = selectUser(session.get('email'))
            games = selectGames()
            notes = selectNotes(us.id)
            return render_template('notes.html', notes=notes, games=games, count=len(notes), success='successfully deleted')

@app.route("/notes_", methods=['POST'])
def notes_():
    
    if session.get('reg') == True:
        us = selectUser(session.get('email'))
        newNote(request.form.get('game'), us.id)
        return jsonify({'message':'<p class="text-success italic">Successfully added note</p>'})
    else:
        return jsonify({'message':'<p class="text-danger italic">You are not logged in!</p>'})


@app.route("/notes__", methods=['POST'])
def notes__():
    if session.get('reg') == True:
        us = selectUser(session.get('email'))
        notes = selectNote(us.id)
        print(request.form.get('note'))
        updateNote(request.form.get('note'), request.form.get('id'))
        return jsonify({'message':'<p class="text-success italic">Successfully changed note</p>'})
    else:
        return jsonify({'message':'<p class="text-danger italic">You are not logged in!</p>'})
    


@app.route("/notes_del_", methods=['POST'])
def notes_del__():
    if session.get('reg') == True:
        us = selectUser(session.get('email'))
        # notes = selectNote(us.id)
        print('id: ',request.form.get('id'))
        removeNote(request.form.get('id'))
        return jsonify({'message':'<p class="text-success italic">Successfully deleted note</p>'})
    else:
        return jsonify({'message':'<p class="text-danger italic">You are not logged in!</p>'}) 
#--------------------------------------------------------------------------------------------------


@app.route("/remove-from-lib_", methods=['POST'])
def remove_from_lib_():
    if session.get('reg') == True:
        us = selectUser(session.get('email'))
        removeFromLib(us.id, request.form.get('name'))
        return jsonify({'message':'<p class="text-success italic">Successfully removed from library</p>'})
        
    else:
        return jsonify({'message':'You are not logged in!'})

@app.route("/reset-password")
def reset_password():
     # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    print('----------------------')
    print(request.args.get('token'))
    print(request.args.get('token'))
    print('----------------------')
    print(request.args.get('email'))
    if session.get('token') == request.args.get('token'):
        return render_template("reset_password.html", email=request.args.get('email'), token=request.args.get('token'))
    else:
        return render_template("nothing.html", reg=session.get('reg'), id=selectUser(session.get('email')).id)
    
@app.route("/reset-password_", methods=['POST'])
def reset_password_():
    print(request.form.get('email'))
    password = request.form.get('password')
    email = request.form.get('email')
    if email:
        us = selectUser(email)
        if us != None:
            updatePassword(email, password)
            session['reg'] = True
            session['email'] = email
            return jsonify({'message':'<p class="text-success italic">Successfully reset password</p>'})
        else:
            return jsonify({'message':'<p class="text-danger italic">Account not found</p>'})
    else:
        return jsonify({'message':'<p class="text-danger italic">Email not found</p>'})

@app.route("/")
def index():
     # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    if "reg" in session:
        pass
    else:
        session["reg"] = False

    return render_template("index.html", reg=session.get('reg'), main_page=True)


@app.route('/comments_', methods=['POST'])
def comments():
    if session.get('reg') == True:
        print('reg')
        us = selectUser(session.get('email'))
        comments = selectComments(request.form.get('name'))
        newComment(request.form.get('name'), us.username, request.form.get('comment'), us.profile_picture)
        return jsonify({'message':F'''<div class="comment">
            <div class="comment-author">
                <img src="/profile-images/.png" alt=""/>
                <p>You</p>
            </div>
            
            <p class="italic comment-text">{request.form.get('comment')}</p>
            <p class="comment-added">{datetime.datetime.now().strftime("%d.%m.%Y")} | {datetime.datetime.now().strftime("%H:%M:%S")}</p>
        </div>
                        <p class="text-success italic">Successfully added comment</p>'''})
    else:
        print('not reg')
        return jsonify({'message':'<p class="text-danger italic">You are not logged in!</p>'})


@app.route('/forgot-password_', methods=['POST'])
def forgot_password():
    email = request.form.get('email')
    if email:
        us = selectUser(email)
        if us != None:
            send_forgot_password(email)
            return jsonify({'message':'<p class="text-success italic">Successfully sent email with instructions</p>'})
        else:
            return jsonify({'message':'<p class="text-danger italic">Account not found</p>'})
    else:
        return jsonify({'message':'<p class="text-danger italic">Email not found</p>'})




@app.route('/search', methods=['POST'])
def search_func():
     # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    # query = request.args.get('q')
    query = request.form.get('q')
    print(query)
    # print(query1)
    categories = []
    # index = 0
    print(request.form)
    for i in range(len(app.config['CATEGORIES'])):
        print(i)
        print(request.form.get('categories'+str(i)))
        # index += 1
        if request.form.get('categories'+str(i)) == 'on':
            categories.append(app.config['CATEGORIES'][i])
    print(categories)
    results = render_template('search.html', games=selectGamesByQuery(query, categories))
    return jsonify({'message':results})


@app.route('/game')
def game_page():
     # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    print('-----------')
    game = request.args.get('name')
    print(game)
    game_obj= selectGamebyName(game.title())
    print(game_obj)
    # Set up Jinja2 environment with the custom loader
    env = Environment(loader=FileSystemLoader('games'))
    
    # Load and render the template
    template = env.get_template(game_obj.html_path.split('/')[-1])
    for i in selectComments(game.title()):
        print(i)
        print(i.comment)
    
    rendered_html = template.render(game=game_obj, reg=session.get('reg'), comments=selectComments(game.title()))
    
    
    return rendered_html

        
    
@app.route('/game_', methods=['POST'])
def game_():
    if session.get('reg') == True:
        us = selectUser(session.get('email'))
        try:
            id = us.id
        except:
            return jsonify({'message':'You are not logged in!'})

        _ = selectLibItemsById(id, request.form.get('name'))
        if len(_) == 0:
            newLibItem(id, request.form.get('name'))
            return jsonify({'message':'Successfully added to library'})
        elif len(_) == 1:
            return jsonify({'message':'This game is already in your library'})
        else:
            return jsonify({'message':'Something went wrong'})
    else:
        return jsonify({'message':'You are not logged in!'})



@app.route('/reg', methods=['GET'])
def reg_page():
     # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    if session.get('reg') == True:
        return render_template('already-logged.html', reg=session.get('reg'))
    else:
        return render_template('reg.html', reg=session.get('reg'))

@app.route('/reg_', methods=['POST'])
def reg_():
    if 'form_name' in request.form:
        if request.form.get('form_name') == 'sign-up':
            # registration
            print('Registration')
            name = request.form.get('username')
            email = request.form.get('semail')
            password = request.form.get('spassword')
            us = selectUser(email)
            if us != None:
                return jsonify({'message':'This email is already registered'})
            else:
                print(f"name: {name}")
                newUser(email, name, password, False, 'default.png')
                session['reg'] = True
                session['email'] = email
                return jsonify({'message':'Successfully registered <a href="/">Go Home</a>'})
        elif request.form.get('form_name') == 'login':
            #loginization
            print('Login')
            users = selectUsers()
            for i in users:
                if i.email == request.form.get('email'):
                    if i.password == request.form.get('password'):
                        session['reg'] = True
                        session['email'] = i.email
                        return jsonify({'message':'Successfully logged in <a href="/">Go Home</a>'})
                    else:
                        return jsonify({'message':'Wrong password'})
                elif i.username == request.form.get('email'):
                    if i.password == request.form.get('password'):
                        session['reg'] = True
                        session['email'] = i.email
                        return jsonify({'message':'Successfully logged in <a href="/">Go Home</a>'})
                
            return jsonify({'message':'Accound not found'})
    else:
        print('What the heck!?')
        
@app.route('/profile')
def profile():
     # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    if session.get('reg') == True:
        user = selectUser(session.get('email'))
        games = selectGamesByLib(user.id)
        print('---')
        print(games)
        print(user)
        return render_template('profile.html', user=user, lib=games, reg=session.get('reg'))
    else:
        return render_template('nothing.html', reg=session.get('reg'), id=selectUser(session.get('email')).id)


@app.route('/logout')
def logout():
    # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    session["reg"] = False
    session["email"] = None
    return redirect('/')


@app.route('/profile_', methods=['POST'])
def profile_():
    
    try:
        updateInfo(request.form.get('username'), request.form.get('email'), request.form.get('password'))
        return jsonify({'message':'Successfully updated'})
    except:
        return jsonify({'message':'Something went wrong'})

def selectUserByUsername(username):
    with Session() as session:
        return session.query(Users).filter_by(username=username).first()

@app.route('/profile/view/<username>')
def profile_view(username):
     # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    user = selectUserByUsername(username)
    games = selectGamesByLib(user.id)
    print('---')
    print(games)
    print(user)
    if user == None or user.private == True:
        return render_template('private.html')
    else:
        return render_template('view-profile.html', user=user, lib=games, reg=session.get('reg'))

def updateProfileImg(id, img):
    with Session() as session:
        indexnw = session.query(Users).filter_by(id=id).first()
        if indexnw:
            indexnw.profile_picture = img
            session.commit()

@app.route('/won_', methods=['POST'])
def won_():
    if session.get('reg') == True:
        us = selectUser(session.get('email'))
        print(us.id)
        newNote("You won!", us.id)
        updateProfileImg(us.id, "CAPYBARA.png")
        
    else:
        pass
    
@app.route('/happybara_mystery')
def happybara_mystery():
     # Get today's date as a string
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment visit count for the date
    visit_count[today] += 1

    return render_template('happybara_mystery.html')

# @app.route('/prototype', methods=['GET'])
# def prototype():
#     return render_template('prototype.html')

base = Base()
# base.createdb()
@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found", 404


# newGame("Raid Shadow Legends", "/gameicons/raidshadowlegends.png", "description", '/games/raidshadowlegends.html')
# newGame("Rust", "/gameicons/rust.png", "Survival game", '/games/rust.html')
# newGame("Minecraft", "/gameicons/minecraft.png", "Very interesting game cubic game about building, mining, crafting, trading, fighting, exploring and more", '/games/minecraft.html')
# newGame("Undertale", "/gameicons/undertale.png", "description", '/games/undertale.html')
# newUser("vladyslav.bankovskyi@gmail.com", "DregoScat", "@TesT1232", False, 'default.png')
# newUser("lobanovk232@gmail.com", "fish_fish456", "Tel.0983782350", False, 'CAPYBARA.png')
# newCategory("Raid Shadow Legends", "Action")
# newCategory("Minecraft", "Adventure")
# newCategory("Minecraft", "RPG")
# newCategory("Undertale", "Action")
# newCategory("Undertale", "Adventure")

# newCategory("Rust", "Action")
# newCategory("Rust", "Adventure")
# newCategory("Rust", "RPG")


if __name__ == "__main__":
    app.run(debug=True)