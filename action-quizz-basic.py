#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
import random
import sys

from hermes_python.hermes import Hermes
from hermes_python.ontology import *


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

#global compteur
global question
global bonne_reponse
global etape_du_jeu
global sentence


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()



MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


INTENT_START_QUIZ = "dbddv01:start_lesson"
INTENT_ANSWER = "dbddv01:give_answer"
INTENT_INTERRUPT = "dbddv01:interrupt"
INTENT_DOES_NOT_KNOW = "dbddv01:does_not_know"

INTENT_FILTER_GET_ANSWER = [
    INTENT_ANSWER,
    INTENT_INTERRUPT,
    INTENT_DOES_NOT_KNOW
]
# Initialisation des données
# Ouvre geo.txt et capture le pays comme question et la capitale comme reponse.
# charge la reponse dans un dictionnaire de question
f = open("geoutf.txt", "r")
question_dict = {}
for line in f:
    entry = line.strip().split(",")
    questiondata = entry[2]
    answerdata = entry[1]
    question_dict[questiondata] = answerdata

f.close()
info_donnee = list(question_dict.keys())


def nouvelle_question():
	global bonne_reponse
	question_cible = random.choice(info_donnee)
        bonne_reponse = str(question_dict[question_cible])
	#compteur=compteur+1
	return(question_cible)

def correct_answer(answer):
	intro = " Votre réponse "+str(answer)+" est correcte. Bravo. Voici la question suivante"
	random_question = str(nouvelle_question())
        say_question = " Quelle est le nom de la capitale du pays nommé :  " + random_question
	sentence = intro + say_question
	return(sentence)
	
def incorrect_answer(answer):
	global bonne_reponse
	intro = " Votre réponse "+str(answer)+" est incorrecte. Dommage. La bonne réponse était " + bonne_reponse + "... Concentrez-vous ! Voici la question suivante : "
	random_question = str(nouvelle_question())
        say_question = " Quelle est le nom de la capitale du pays nommé :  " + random_question
	sentence = intro + say_question
	return(sentence)

	
def user_request_quiz(hermes, intent_message):
       
        intro="Bienvenue dans le quizz des capitales... Voici les questions pour les champions..."
	random_question = str(nouvelle_question())
        say_question = " Quelle est le nom de la capitale du pays nommé :  " + random_question
	sentence = intro + say_question
	hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_ANSWER)
	
    
def user_gives_answer(hermes, intent_message):
    global bonne_reponse       
    answer = None
    session_id = intent_message.session_id
    

    if intent_message.slots.answer:
        answer = intent_message.slots.answer.first().value
		
        if answer == bonne_reponse:
            sentence = str(correct_answer(answer))
        else:
            sentence = str(incorrect_answer(answer))
			
	hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_ANSWER)

def user_does_not_know(hermes, intent_message):
    global bonne_reponse
    session_id = intent_message.session_id
    intro = " Ok pas de soucis. La bonne réponse était " + bonne_reponse + "... Concentrez-vous ! Voici la question suivante : "
    random_question = str(nouvelle_question())
    say_question = " Quelle est le nom de la capitale du pays nommé :  " + random_question
    sentence = intro + say_question

    hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_ANSWER)

def user_quits(hermes, intent_message):
    #User wants to quit
    session_id = intent_message.session_id
    sentence = " Très bien nous abandonnons la partie. Pour rejouer n'hésitez pas à me le demander"
    hermes.publish_end_session(session_id, sentence)


def session_started(hermes, session_started_message):
    # function for initialization purpose whenever the game start
    #print("sessionID: {}".format(session_started_message.session_id))
    #print("session site ID: {}".format(session_started_message.site_id))
    #print("sessionID: {}".format(session_started_message.custom_data))

    session_id = session_started_message.session_id
    custom_data = session_started_message.custom_data
    sentence = " intention de démarrage de session atteinte. contenu de custom data égale " + str(custom_data)

   
def session_ended(hermes, session_ended_message):
    #fonction to clean any data whenever the game is over
    session_id = session_ended_message.session_id
    session_site_id = session_ended_message.site_id



with Hermes(MQTT_ADDR) as h:

    h.subscribe_intent(INTENT_START_QUIZ, user_request_quiz) \
        .subscribe_intent(INTENT_INTERRUPT, user_quits) \
        .subscribe_intent(INTENT_DOES_NOT_KNOW, user_does_not_know) \
        .subscribe_intent(INTENT_ANSWER, user_gives_answer) \
	.subscribe_session_ended(session_ended) \
        .subscribe_session_started(session_started) \
        .start()
