#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser


from hermes_python.hermes import Hermes
from hermes_python.ontology import *


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

global numero_de_question
global liste_ville
global liste_capitale


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
# database
liste_pays = ["france","grande bretagne","belgique","pays bas","autriche"]
liste_capitale = ["paris","londres","bruxelles","amsterdam","vienne"]
numero_de_question = 0


def user_request_quiz(hermes, intent_message):
    #print("User is asking for a quiz")
    #number_of_questions = 1
    #tables = []
    #if intent_message.slots.number:
    #    number_of_questions = intent_message.slots.number.first().value
    #if intent_message.slots.table:
    #    tables = [intent_message.slots.table.first().value]
    #session_state, sentence = tt.start_quiz(number_of_questions, tables)
    #tt.save_session_state(SessionsStates, intent_message.session_id, session_state)
    global numero_de_question
    question = " Quelle est le nom de la capitale en " + liste_pays[numero_de_question]
    sentence = " Attention voici la question :" + question
    
    hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_ANSWER)

    
def user_gives_answer(hermes, intent_message):
    #print("User is giving an answer")
    global numero_de_question
    answer = None
    session_id = intent_message.session_id
    #sentence = " étape de réponse atteinte sans capture. question suivante"
    #session_state = SessionsStates.get(session_id)

    if intent_message.slots.answer:
        answer = intent_message.slots.answer.first().value
        if answer == liste_capitale[numero_de_question]:
            resultat = " Votre réponse "+str(answer)+" est correcte. Bravo. Voici la question suivante"
            if numero_de_question < 4:
                
                numero_de_question = numero_de_question + 1
                question = " Quelle est le nom de la capitale en " + liste_pays[numero_de_question]
            else:
                numero_de_question = 0
                question = " Quelle est le nom de la capitale en " + liste_pays[numero_de_question]
            sentence = resultat + question
            hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_ANSWER)
        
        else:
            resultat = " Désolé, la bonne réponse était " + liste_capitale[numero_de_question] + ". Attention voici une nouvelle question "
	
            if numero_de_question < 4:
                numero_de_question = numero_de_question + 1
                question = "Quelle est le nom de la capitale en " + liste_pays[numero_de_question]
            else:
                numero_de_question = 0
                question = "Quelle est le nom de la capitale en " + liste_pays[numero_de_question]
            sentence = resultat + question
            hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_ANSWER)	
    #if not continues:
        #hermes.publish_end_session(session_id, sentence)
        #tt.remove_session_state(SessionsStates, session_id)
        #return

   # hermes.publish_continue_session(session_id, sentence, INTENT_FILTER_GET_ANSWER)


def user_does_not_know(hermes, intent_message):
    #print("User does not know the answer")
    session_id = intent_message.session_id
    global numero_de_question
    resultat = " Désolé, la bonne réponse était " + liste_capitale[numero_de_question] + ". Attention voici une nouvelle question "
    if numero_de_question < 4:
        numero_de_question = numero_de_question + 1
        question = " Quelle est le nom de la capitale en " + liste_pays[numero_de_question]
    else:
        numero_de_question = 0
        question = "Quelle est le nom de la capitale en " + liste_pays[numero_de_question]	
			
    sentence = resultat + question
    hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_ANSWER)
    
    



    #sentence = "étape du je ne sais pas atteinte. la bonne reponse était bla bla, question suivante "
    #sentence, continues = tt.user_does_not_know(session_id, SessionsStates)

    #if not continues:
    #    hermes.publish_end_session(session_id, sentence)
    #    tt.remove_session_state(SessionsStates, session_id)
    #    return

    #hermes.publish_continue_session(session_id, sentence, INTENT_FILTER_GET_ANSWER)


def user_quits(hermes, intent_message):
    #print("User wants to quit")
    session_id = intent_message.session_id
    sentence = " Très bien nous abandonnons la partie. Pour rejouer n'hésitez pas à me le demander"
    #tt.remove_session_state(SessionsStates, session_id)
    hermes.publish_end_session(session_id, sentence)


def session_started(hermes, session_started_message):
    # function for initialization purpose whenever the game start
    # permet de tester si la demande est logique
    #print("sessionID: {}".format(session_started_message.session_id))
    #print("session site ID: {}".format(session_started_message.site_id))
    #print("sessionID: {}".format(session_started_message.custom_data))

    session_id = session_started_message.session_id
    custom_data = session_started_message.custom_data
#liste_pays = ["france","grande bretagne","belgique","pays bas","allemagne"]
#liste_capitale = ["paris","londre","bruxelles","amsterdam","berlin"]
#numero_de_question = 0


    sentence = " intention de démarrage de session atteinte. contenu de custom data égale " + str(custom_data)

    #if custom_data:
    #    if SessionsStates.get(custom_data):
    #        SessionsStates[session_id] = SessionsStates[custom_data]
    #        SessionsStates.pop(custom_data)


def session_ended(hermes, session_ended_message):
    #fonction to clean any data whenever the game is over
    session_id = session_ended_message.session_id
    session_site_id = session_ended_message.site_id
    sentence = "intention de session terminée atteinte. contenu de session et de site passé par fonction"
    #if SessionsStates.get(session_id) is not None:
    #    hermes.publish_start_session_action(site_id=session_site_id,
    #                                        session_init_text="",
    #                                        session_init_intent_filter=INTENT_FILTER_GET_ANSWER,
    #                                        session_init_can_be_enqueued=False,
    #                                        custom_data=session_id)



with Hermes(MQTT_ADDR) as h:

    h.subscribe_intent(INTENT_START_QUIZ, user_request_quiz) \
        .subscribe_intent(INTENT_INTERRUPT, user_quits) \
        .subscribe_intent(INTENT_DOES_NOT_KNOW, user_does_not_know) \
        .subscribe_intent(INTENT_ANSWER, user_gives_answer) \
        .subscribe_session_ended(session_ended) \
        .subscribe_session_started(session_started) \
        .start()
