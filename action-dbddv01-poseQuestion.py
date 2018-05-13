#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import random

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

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

#def subscribe_intent_callback(hermes, intentMessage):
#    conf = read_configuration_file(CONFIG_INI)
#    action_wrapper(hermes, intentMessage, conf)




def action_reponse(hermes, intentMessage):
    
    current_session_id = intentMessage.session_id
    answer = intentMessage.slots.answer_capitale.first().value

    if answer == "Paris":
      result_sentence = "Bravo c'est la bonne réponse"
    else :
      result_sentence = "Soit je n'ai pas compris, soit la réponse est fausse"

    hermes.publish_end_session(current_session_id, result_sentence)

  return


# attention les noms propres sont en minuscule
  	
if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("dbddv01:getReponse", action_reponse) \
.start()
