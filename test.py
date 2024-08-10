import datetime

# engine = create_engine("sqlite:///app.db", echo=True )
# Session = sessionmaker(bind=engine)


# class Base(DeclarativeBase):
#     def create_db():
#         Base.metadata.create_all(engine)

#     def drop_db():
#         Base.metadata.drop_all(engine)


# class User_profil(Base):
#     __tablename__ = "user_profil"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     us_id: Mapped[int] = mapped_column()
#     user_info: Mapped[str] = mapped_column()
#     user_name: Mapped[str] = mapped_column()
#     user_psevdo: Mapped[str] = mapped_column()


# def update_profil_info(name, id, info, psevdo):
#     with Session() as session:
#         session.commit()

#         indexnw = session.query(User_profil).filter_by(us_id=id).first()
#         if indexnw:
#             if info:
#                 indexnw.user_info=info
#             if name:
#                 indexnw.user_name=name
#             if psevdo:
#                 indexnw.user_psevdo=psevdo

#         else:
#             new_user = User_profil(user_name=name, us_id=id, user_info=info, user_psevdo=psevdo)
#             session.add(new_user)
#         session.commit()

# def Select_us_ptofil(us_id):
#     with Session() as session:
#         info = session.query(User_profil).filter_by(us_id = us_id).first()
#         print(info)
#         if info:
#             return info
#         else:
#             return None

# @app.route("/prot3", methods = ["POST"])
# def prot3():
#     response_data = []
#     us_n = request.form["us_n"]
#     us_p = request.form["psevdo"]
#     us_t = request.form["us_text"]

#     profil_check = Select_us_ptofil(session["USER_ID"])

#     if profil_check and (us_n or us_p or us_t):
#         update_profil_info(us_n,session["USER_ID"],us_t,us_p)
#         profil_ino = Select_us_ptofil(session["USER_ID"])
#         print(profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id)
#         print("profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id 111111111111111111111111111111111111111")
#         data = {
#             'u_nme': profil_ino.user_name,
#             'psevdo': profil_ino.user_psevdo,
#             'u_info': profil_ino.user_info,
#             'id_u': profil_ino.us_id
#         }
#         response_data.append(data)

#     elif profil_check:
#         profil_ino = Select_us_ptofil(session["USER_ID"])
#         print(profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id)
#         print("profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id22222222222222222222222222222222222222222222222222222222")
#         data = {
#             'u_nme': profil_ino.user_name,
#             'psevdo': profil_ino.user_psevdo,
#             'u_info': profil_ino.user_info,
#             'id_u': profil_ino.us_id
#         }
#         response_data.append(data)

#     elif us_n or us_p or us_t:
#         update_profil_info(us_n,session["USER_ID"],us_t,us_p)
#         print("profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id3333333333333333333333333333333333333333333333333333333")
#         profil_ino = Select_us_ptofil(session["USER_ID"])
#         data = {
#             'u_nme': profil_ino.user_name,
#             'psevdo': profil_ino.user_psevdo,
#             'u_info': profil_ino.user_info,
#             'id_u': profil_ino.us_id
#         }
#         response_data.append(data)

#     elif profil_check == None and (us_n == None or us_p == None or us_t == None):
#         print("profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id444444444444444444444444444444444444444444444444444444444444")

#         data = {
#             'u_nme': "Нічого не знайдено",
#             'psevdo': "Нічого не знайдено",
#             'u_info': "Нічого не знайдено, та ви можите записати інформацію про себе по кнопці знизу",
#             'id_u': session["USER_ID"]
#         }
#         response_data.append(data)

#     else:
#         print(
#             "profil_ino.user_name,profil_ino.user_psevdo,profil_ino.user_info,profil_ino.us_id5555555555555555555555555555555555555555555555555555555555555555555")
#         # ТУТ МАЄ БУТИ ЯКАСЬ ФУНКЦІ ЩОБ ВЗЯТИ ДАНІ ПРО БІБЛІОТЕКУ Я ПРОСТО З НИМИ НЕ ОСОБЛИВО РОЗІБРАВСЯ
#         # І ПОТІМ ІНФОРМАЦІЯ З ФУНКЦІЇ ПЕРЕДАЄТЬСЯ В JAVA SCRIPT
#         # ps_inf = function_to_get_element()
#         # for i in ps_inf:
#         #     encoded_image = base64.b64encode(i[4]).decode('utf-8') #число 4 це порядковий індекс фотки
#         #     data = {
#         #         'image': f'data:image/jpeg;base64,{encoded_image}',
#         #         'game_href': link,
#         #         'game_description': "game_description",
#         #     }
#         #     response_data.append(data)

#     return jsonify({"message": response_data}), 200


from flask import Flask
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler

def configure_logging():
    # Clear existing handlers to avoid duplicate logging
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    # Configure a new handler with the desired filename
    handler = TimedRotatingFileHandler(filename=f"logs/{datetime.datetime.now().strftime("%d.%m.%Y")}.log", when='midnight', interval=1, backupCount=7)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

configure_logging()

app = Flask(__name__)

@app.route('/')
def main():
  return "testing logging levels."

if __name__ == '__main__':
  app.run(debug=True)