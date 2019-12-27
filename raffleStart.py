import sys
import os
import json
from random import randint
from threading import Thread
import shortuuid
from pip._vendor.colorama import Fore
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
engine = create_engine('postgresql+psycopg2://lucksend:XD9pLYDxaqZHlJaBVSum6uWIyC4Q1Dob@127.0.0.1/Raffles')

DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    mail_adress = Column(String, nullable=False)
    name = Column(String, nullable=False)
    profile_picture = Column(String, nullable=False)
    local = Column(String, nullable=False)
    profile_link = Column(String, nullable=False)
    provider_name = Column(String, nullable=False)
    provider_id = Column(String, nullable=False)
    verification = Column(Boolean, nullable=False)
    id_share = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)
    raffleslerf = relationship('Raffles', backref='users', lazy=True)
    feedbacksf = relationship('Feedbacks', backref='users', lazy=True)
    participantsf = relationship('Participants', backref='users', lazy=True)
    keysf = relationship('Keys', backref='users', lazy=True)
    luckysf = relationship('Luckys', backref='users', lazy=True)


class Raffles(Base):
    __tablename__ = 'raffles'
    id = Column(Integer, primary_key=True)
    id_share = Column(String, nullable=False,unique=True)
    user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    title = Column(String, nullable=False)
    contact_information = Column(String, nullable=False)
    description = Column(String, nullable=False)
    expiration = Column(DateTime, nullable=False)
    status = Column(Boolean, nullable=False)
    processing = Column(Boolean, nullable=False)
    completed = Column(Boolean, nullable=False)
    delete = Column(Boolean, nullable=False)
    disable = Column(Boolean, nullable=False)
    winners = Column(Integer, nullable=False)
    reserves = Column(Integer, nullable=False)
    raffle_date = Column(DateTime, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)
    luckysf = relationship('Luckys', backref='raffles', lazy=True)
    tagstargetf = relationship('Tagtargets', backref='raffles', lazy=True)
    countrytargetf = relationship('Countrytargets', backref='raffles', lazy=True)


class Feedbacks(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    description = Column(String, nullable=False)
    read = Column(Boolean, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)


class Participants(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    raffle_id = Column(Integer, nullable=False)
    creation_date = Column(DateTime, nullable=False)


class Keys(Base):
    __tablename__ = 'keys'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    key = Column(String, nullable=False)
    device_key = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    expiration = Column(DateTime, nullable=False)
    device_information_id = Column(Integer, ForeignKey('deviceinformation.id'),nullable=False)


class Luckys(Base):
    __tablename__ = 'luckys'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    raffles_id = Column(Integer, ForeignKey('raffles.id'),nullable=False)
    secret_key = Column(String, nullable=False, unique=True)
    status = Column(Boolean, nullable=False)
    check_key = Column(Boolean, nullable=False)
    creation_date = Column(DateTime, nullable=False)


class Deviceinformation(Base):
    __tablename__ = 'deviceinformation'
    id = Column(Integer,primary_key=True)
    brand = Column(String,nullable=False)
    model = Column(String,nullable=False)
    release = Column(String,nullable=False)
    creation_date = Column(DateTime, nullable=False)
    keysf = relationship('Keys', backref='deviceinformation', lazy=True)


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag_name = Column(String,nullable=False)
    creation_date = Column(DateTime, nullable=False)
    tagsf = relationship('Tagtargets', backref='tags', lazy=True)


class Tagtargets(Base):
    __tablename__ = 'tagtargets'
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)
    raffle_id = Column(Integer, ForeignKey('raffles.id'), nullable=False)
    creation_date = Column(DateTime, nullable=False)


class Countries(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    country_code = Column(String, nullable=False)
    Countriesf = relationship('Countrytargets', backref='countries', lazy=True)


class Countrytargets(Base):
    __tablename__ = 'countrytargets'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    raffle_id = Column(Integer, ForeignKey('raffles.id'), nullable=False)


class Countrymultilang(Base):
    __tablename__ = 'countrymultilang'
    id = Column(Integer, primary_key=True)
    multi_code = Column(String, nullable=True)
    country_code = Column(String, nullable=False)
    country_name = Column(String, nullable=False)


class Versions(Base):
    __tablename__ = 'versions'
    id = Column(Integer,primary_key=True)
    versions_name = Column(String,nullable=False)
    versions_description = Column(String,nullable=True)
    versions_code = Column(String,nullable=False)
    versions_secret_key = Column(String,nullable=False)
    contact_secret_key = Column(String,nullable=False)
    creation_date = Column(DateTime, nullable=False)
    expiration = Column(DateTime, nullable=False)


class Logs(Base):
    __tablename__ = 'logs'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ip_address = Column(String, nullable=False)
    action = Column(String,nullable=False)
    data = Column(JSON,nullable=True)
    creation_date = Column(DateTime, nullable=False)


def uuid_short():
    sec = randint(0, 2)
    if sec == 0:
        sonuc = shortuuid.ShortUUID().random(length=16)
    elif sec == 1:
        sonuc = shortuuid.ShortUUID().random(length=18)
    elif sec == 2:
        sonuc = shortuuid.ShortUUID().random(length=20)
    return sonuc


def add_log(action, user_id, data):
    log = Logs()
    log.user_id = user_id
    log.ip_address = "SYSTEM"
    log.action = action
    log.data = data
    log.creation_date = datetime.utcnow()
    session.add(log)
    session.commit()
    return True


def get_maintenance_mode():
    try:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        json_file = open(ROOT_DIR + "/settings.json", "r")
        settings = json.loads(json_file.read())
        json_file.close()
        maintenance_mode = settings["maintenance_mode"]
        if maintenance_mode:
            print(Fore.RED+" #Maintenance mode enabled")
        else:
            print(Fore.GREEN+" #Maintenance mode disable")
        return maintenance_mode
    except ValueError as e:
        print(e)
        return True


def add_lock(raffle_id_share,data):
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    raffle_lock = open(ROOT_DIR+"\\raffle_lock\\"+raffle_id_share+".lock", "w")
    raffle_lock.write(data)
    raffle_lock.close()


def delete_lock(raffle_id_share):
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    os.remove(ROOT_DIR+"\\raffle_lock\\"+raffle_id_share+".lock")


def raffle_start_engine(user_id,raffle_id,raffle_id_share,winner_count,reserve_count):
    try:
        raffle = session.query(Raffles).filter_by(id=raffle_id).first()
        if raffle.processing is False and raffle.completed is False:
            add_lock(raffle_id_share, json.dumps({"raffle_id": raffle_id, "id_share": raffle_id_share}))
            raffle_update = session.query(Raffles).filter(Raffles.id == raffle_id).first()
            raffle_update.processing = True
            raffle_update.last_update = datetime.utcnow()
            session.add(raffle_update)
            session.commit()
            participant_list = []
            winners_list = []
            reserves_list = []
            winners_count = winner_count
            reserves_count = reserve_count
            participants = session.query(Participants).filter(raffle_id == Participants.raffle_id).all()
            for participant in participants:
                participant_list.append(participant.user_id)
            print("toplam sayı:" + str(len(participant_list)))
            for i in range(0, winners_count):
                participant_count = len(participant_list)
                rnd = randint(0, participant_count - 1)
                print("rastgele sayı:" + str(rnd))
                winners_list.append(participant_list[rnd])
                participant_list.remove(participant_list[rnd])
            if reserves_count is not 0:
                for i in range(0, reserves_count):
                    participant_count = len(participant_list)
                    rnd = randint(0, participant_count - 1)
                    reserves_list.append(participant_list[rnd])
                    participant_list.remove(participant_list[rnd])
            lucky_check = session.query(Luckys).filter(Luckys.raffles_id == raffle_id).count()
            if lucky_check is not 0:
                session.query(Luckys).filter(Luckys.raffles_id == raffle_id).delete()
                session.commit()
            for winners in winners_list:
                lucky = Luckys()
                lucky.user_id = winners
                lucky.raffles_id = raffle_id
                lucky.secret_key = uuid_short()
                lucky.status = True
                lucky.check_key = False
                lucky.creation_date = datetime.utcnow()
                session.add(lucky)
                session.commit()
                print(winners)
            for reserves in reserves_list:
                lucky = Luckys()
                lucky.user_id = reserves
                lucky.raffles_id = raffle_id
                lucky.secret_key = uuid_short()
                lucky.status = False
                lucky.check_key = False
                lucky.creation_date = datetime.utcnow()
                session.add(lucky)
                session.commit()
                print(reserves)
            raffle_update = session.query(Raffles).filter(Raffles.id == raffle_id).first()
            raffle_update.processing = False
            raffle_update.completed = True
            raffle_update.last_update = datetime.utcnow()
            session.add(raffle_update)
            session.commit()
            add_log("raffle_engine_successful", user_id, "{}")
            delete_lock(raffle_id_share)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        add_log("raffle_engine_fail", user_id, json.dumps({"error_msg": exc_value}))
        raffle_update = session.query(Raffles).filter(Raffles.id == raffle_id).first()
        raffle_update.processing = False
        raffle_update.status = False
        raffle_update.last_update = datetime.utcnow()
        session.add(raffle_update)
        session.commit()
        delete_lock(raffle_id_share)


def raffle_start():
    raffles = session.query(Raffles).filter(Raffles.raffle_date < datetime.utcnow()).filter(Raffles.status == True).filter(Raffles.processing == False).filter(Raffles.completed == False).all()
    if raffles is not None:
        for raffle in raffles:
            if get_maintenance_mode() is False:
                thread_raffle_engine = Thread(target=raffle_start_engine, args=(raffle.user_id,raffle.id,raffle.id_share,raffle.winners,raffle.reserves))
                thread_raffle_engine.start()
                thread_raffle_engine.join()


if get_maintenance_mode() is False:
    raffle_start()
