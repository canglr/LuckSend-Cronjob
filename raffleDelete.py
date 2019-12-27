import os
import json
from threading import Thread
from pip._vendor.colorama import Fore
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
    socialstatisticssf = relationship('Socialstatistics', backref='users', lazy=True)
    socialsavedf = relationship('Socialsaved', backref='users', lazy=True)
    socialreportssf = relationship('Socialreports', backref='users', lazy=True)


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
    date = Column(DateTime, nullable=False)
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


class Socialmedia(Base):
    __tablename__ = 'socialmedia'
    id = Column(Integer, primary_key=True)
    id_share = Column(String, nullable=False, unique=True)
    author_name = Column(String, nullable=False)
    media_id = Column(String, nullable=False)
    media_description = Column(String, nullable=False)
    media_image = Column(String, nullable=False)
    media_url = Column(String, nullable=False)
    provider_name = Column(String,nullable=False)
    delete = Column(Boolean, nullable=False)
    disable = Column(Boolean, nullable=False)
    verification = Column(Boolean, nullable=False)
    sponsor = Column(Boolean,nullable=False)
    creation_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)
    socialtagtargetsf = relationship('Socialtagtargets', backref='socialmedia', lazy=True)
    socialsavedf = relationship('Socialsaved', backref='socialmedia', lazy=True)
    socialstatisticsf = relationship('Socialstatistics', backref='socialmedia', lazy=True)
    socialcountrytargetsf = relationship('Socialcountrytargets', backref='socialmedia', lazy=True)
    socialreportsf = relationship('Socialreports', backref='socialmedia', lazy=True)


class Socialtagtargets(Base):
    __tablename__ = 'socialtagtargets'
    id = Column(Integer,primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)
    social_id = Column(Integer, ForeignKey('socialmedia.id'), nullable=False)


class Socialcountrytargets(Base):
    __tablename__ = 'socialcountrytargets'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    social_id = Column(Integer, ForeignKey('socialmedia.id'), nullable=False)


class Socialstatistics(Base):
    __tablename__ = 'socialstatistics'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    social_id = Column(Integer, ForeignKey('socialmedia.id'), nullable=False)
    clicks = Column(Boolean, nullable=False)
    creation_date = Column(DateTime, nullable=False)


class Socialsaved(Base):
    __tablename__ = 'socialsaved'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    social_id = Column(Integer, ForeignKey('socialmedia.id'), nullable=False)
    creation_date = Column(DateTime, nullable=False)


class Socialreports(Base):
    __tablename__ = 'socialreports'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    social_id = Column(Integer, ForeignKey('socialmedia.id'), nullable=False)
    description = Column(String, nullable=False)
    read = Column(Boolean, nullable=False)
    creation_date = Column(DateTime, nullable=False)


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


def raffle_delete_engine(raffle_id):
    try:
        session.query(Countrytargets).filter(Countrytargets.raffle_id == raffle_id).delete()
        session.query(Tagtargets).filter(Tagtargets.raffle_id == raffle_id).delete()
        session.query(Luckys).filter(Luckys.raffles_id == raffle_id).delete()
        session.query(Participants).filter(Participants.raffle_id == raffle_id).delete()
        session.query(Raffles).filter(Raffles.id == raffle_id).delete()
        session.commit()
    except:
        session.rollback()


def socialmedia_delete_engine(social_id):
    try:
        session.query(Socialreports).filter(Socialreports.social_id == social_id).delete()
        session.query(Socialsaved).filter(Socialsaved.social_id == social_id).delete()
        session.query(Socialstatistics).filter(Socialstatistics.social_id == social_id).delete()
        session.query(Socialcountrytargets).filter(Socialcountrytargets.social_id == social_id).delete()
        session.query(Socialtagtargets).filter(Socialtagtargets.social_id == social_id).delete()
        session.query(Socialmedia).filter(Socialmedia.id == social_id).delete()
        session.commit()
    except:
        session.rollback()


def raffle_delete_start():
    raffles_delete = session.query(Raffles).filter(Raffles.delete == True).all()
    for raffle in raffles_delete:
        if get_maintenance_mode() is False:
            thread_raffle_delete_engine = Thread(target=raffle_delete_engine, args=(raffle.id,))
            thread_raffle_delete_engine.start()
            thread_raffle_delete_engine.join()


def socialmedia_delete_start():
    socialmedias_delete = session.query(Socialmedia).filter(Socialmedia.delete == True).all()
    for socialmedia in socialmedias_delete:
        if get_maintenance_mode() is False:
            thread_socialmedia_delete_engine = Thread(target=socialmedia_delete_engine, args=(socialmedia.id,))
            thread_socialmedia_delete_engine.start()
            thread_socialmedia_delete_engine.join()


if get_maintenance_mode() is False:
    raffle_delete_start()
    socialmedia_delete_start()