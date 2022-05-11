from typing import Any, Text, Dict, List
from rasa_sdk.events import FollowupAction, ActionExecuted

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from typing import Text, List, Optional



# class action_trigger_conversion_form(Action):

#     def name(self) -> Text:
#         return "action_trigger_conversion_form"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         a = tracker.events

#         only_actions = []
#         only_intents = []

#         for x in a:
#             if x['event'] == 'user':
#                 only_intents.append(x['parse_data']['intent']['name'])
#             elif x['event'] == 'bot':
#                 try:
#                     only_actions.append(x['metadata']['utter_action'])
#                 except:
#                     pass

#         # if only_intents[-1] == "speak_twice":
#         #     reply = only_actions[-1] 
#         if only_actions[-1] == 'utter_greeting_sharon_prudential':
#             dispatcher.utter_message(response = 'utter_greeting_repeat_sharon_prudential')
#             return []

#         else:
#             rules =  {'already_have_agent': 'already_have_agent'}
#             reply_action = rules[only_intents[-1]]
#             dispatcher.utter_message(text = reply_action)
#             return [FollowupAction(name=reply_action)]
        

        
class Validate_already_have_agent(FormValidationAction):
    ACTIONS = []
    def name(self) -> Text:
        return "validate_already_have_agent"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
        action = tracker.get_intent_of_latest_message()
        actions = []

        ret=slots_mapped_in_domain.copy()
        if not tracker.get_slot("want_to_continue"):
            ret.append('goodbye')

        print(self.ACTIONS.count('already_have_agent'))
        if action == "already_done" or self.ACTIONS.count('already_have_agent') >= 2:
            ret.clear()
            ret = ["goodbye"]
        self.ACTIONS.append(action)
        # print("{}, action:{}, reply: {}, intent: {}".format(self.name(), ret))

        print(self.name(), action, ret)
        return ret

        
class action_rule_only_once(Action):

    def name(self) -> Text:
        return "action_rule_only_once"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        a = tracker.events

        only_actions = []
        only_intents = []

        for x in a:
            if x['event'] == 'user':
                only_intents.append(x['parse_data']['intent']['name'])
            elif x['event'] == 'bot':
                try:
                    only_actions.append(x['metadata']['utter_action'])
                except:
                    pass

        
        if only_actions[-1] == 'utter_greeting_sharon_prudential':
            reply = 'utter_greeting_repeat_sharon_prudential'
        
        else:
            reply = ''
            for intent in ['question_related_to_age_info',
                        'not_singaporean',
                        'question_speak_chinese',
                        'question_related_to_fees',
                        'question_related_to_scam',
                        'question_related_to_manager',
                        'question_related_to_singpass_checking',
                        'question_related_to_distribution',
                        'question_related_to_disclosure_details',
                        'question_related_to_who_i_can_nominate',
                        'question_related_to_witness',
                        'cpf_account_distribution',
                        'objection_i_am_agent']:
                if only_intents.count(intent) > 1:
                    reply = 'utter_goodbye'

            
            if reply != 'utter_goodbye':
                rules = {'question_related_to_age_info':'utter_age_question',
                        'not_singaporean':'utter_goodbye',
                        'question_speak_chinese':'utter_chinese_audio',
                        'question_related_to_fees':'utter_cost_info',
                        'question_related_to_scam':'utter_scam_reply',
                        'question_related_to_manager':'utter_manager_introduction',
                        'question_related_to_singpass_checking':'utter_regarding_singpass',
                        'question_related_to_distribution':'utter_distributions_info',
                        'question_related_to_disclosure_details':'utter_disclose_nomination_info',
                        'question_related_to_who_i_can_nominate':'utter_nomination_criteria_info',
                        'question_related_to_witness':'utter_witness_info',
                        'cpf_account_distribution': 'utter_types_of_account_distribution',
                        'objection_i_am_agent': 'utter_goodbye'}

                reply = rules[only_intents[-1]]
        print("{}, action: {}, reply: {}, intent: {}".format(self.name(), only_actions[-1], reply, only_intents[-1]))
  
        dispatcher.utter_message(response = reply)
        return []



class action_fast_sharon(Action):

    def name(self) -> Text:
        return "action_fast_sharon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        a = tracker.events

        only_actions = []
        only_intents = []

        for x in a:
            if x['event'] == 'user':
                only_intents.append(x['parse_data']['intent']['name'])
            elif x['event'] == 'bot':
                try:
                    only_actions.append(x['metadata']['utter_action'])
                except:
                    pass

                
        #only_intents = ["start_conversation","confirm","reject","confirm","who_is","confirm","confirm","age"]        



        rules = [ "'already_have_agent', 'confirm'",
                "'who_is', ", "'nlu_fallback', ", "'repeat', ",  "'question_why_cpf_and_prudential', ", 
                "'looking_for', ",
                "'question_related_to_singpass_checking', ",
                "'question_related_to_fees', ", "'question_related_to_age_info', ", 
                "'question_related_to_scam', ",
                "'question_related_to_distribution', ",
                "'question_related_to_disclosure_details', ",
                "'question_related_to_numbers', ",
                "'cpf_account_distribution', ",
                "'question_related_to_witness', ",
                "'question_related_to_who_i_can_nominate', ",
                "'objection_i_am_agent', ",
                "'question_speak_chinese', "]  

        for r in rules:
            only_intents = str(only_intents).replace(r, "")
        only_intents = str(only_intents).replace("'","").replace(" ","")[1:-1] 
        only_intents = [x for x in only_intents.split(",") if x!= ""]

        # intents for ca : confirm, reject, already_done, already_have_agent, morning, 'afternoon','evening, 
        len_a = len(only_intents)

        yes_no = ['reject','already_done', 'confirm']
        two_no = ['reject','already_done']
        five_yes = ['confirm', 'morning','afternoon','evening', 'date_day']
        two_yes = ['confirm', 'age']
        after_greeting = ['morning', 'afternoon', 'evening', 'age', 'date_day', 'confirm', 'reject', 'already_done']
        reply = 'utter_goodbye'
        if len_a < 4 and only_intents[-1] in ['afternoon', 'morning', 'evening', 'date_day']:
            reply = 'utter_busy_call_back'

        if only_intents[-1] == "repeat":
            reply = only_actions[-1]
            

        if len_a == 1:
            reply = 'utter_discuss_nomination'
        elif len_a == 2:
            if only_intents in [['start_conversation', x] for x in after_greeting]:
                reply = 'utter_discuss_nomination'
        elif len_a == 3:
            if only_intents in [['start_conversation']+[x]+[xx] for x in after_greeting for xx in ['reject','already_done', 'confirm'] ]:
                reply = 'utter_purpose'
            # elif only_intents == ['start_conversation', 'confirm', 'reject']:
            #     reply = 'utter_convincing'
            # elif only_intents == ['start_conversation', 'confirm', 'already_done']:
            #     reply = 'utter_done_nomination'
            # elif only_intents == ['start_conversation', 'confirm']:
            #     reply = 'utter_agent_followup'
        elif len_a == 4:
            # contains any of the rejections
            # if only_intents in [['start_conversation']+[x]+[x]+['confirm'] for x in ['reject','already_done']]:
            #     reply = 'utter_appointment_call_time'
            if only_intents in [['start_conversation']+[x]+[xx]+[t] for x in after_greeting for xx in ['reject','already_done', 'confirm'] for t in ['afternoon', 'morning', 'evening', 'date_day', 'confirm']]:
                reply = 'utter_appointment_call_time'
            elif only_intents in [['start_conversation']+[x]+[xx]+['reject'] for x in after_greeting for xx in ['reject','already_done', 'confirm']]:
                reply = 'utter_convincing'
            elif only_intents in [['start_conversation']+[x]+[xx]+['already_done'] for x in after_greeting for xx in ['reject','already_done', 'confirm']]:
                reply = 'utter_done_nomination'

        elif len_a == 5:
            if only_intents in [['start_conversation']+[x]+[xx]+[i]+[t] for i in ['reject','already_done']\
            for x in after_greeting for xx in ['reject','already_done', 'confirm'] for t in ['afternoon', 'morning', 'evening', 'date_day', 'confirm']]:
                reply = 'utter_appointment_call_time'
            elif only_intents[:-1] in [['start_conversation']+[x]+[xx]+[t] for x in after_greeting for xx in ['reject','already_done', 'confirm'] for t in ['afternoon', 'morning', 'evening', 'date_day', 'confirm'] ]\
                and only_intents[-1] in ['confirm','morning','afternoon','evening', 'date_day']:
                reply = 'utter_age_info'
            # elif only_intents in [['start_conversation']+[x]+[xx]+['confirm'] for x in ['reject','already_done', 'confirm'] for xx in ['reject','already_done', 'confirm']]:
            #     reply = 'utter_appointment_call_time'
        elif len_a == 6:
            if only_intents[:-1] in [['start_conversation']+[x]+[xx]+[i]+[t] for i in ['reject','already_done'] for x in after_greeting for xx in ['reject','already_done', 'confirm'] for t in ['afternoon', 'morning', 'evening', 'date_day', 'confirm'] ]\
                and only_intents[-1] in ['confirm','morning','afternoon','evening', 'date_day']:
                reply = 'utter_age_info'
            # elif only_intents in [['start_conversation', 'confirm', 'confirm']+[x]+['confirm']+ [i] for i in ['confirm', 'morning','afternoon','evening', 'date_day']\
            #      for x in ['reject','already_done']]:
            #     reply = 'utter_age_info'
            elif only_intents in [['start_conversation']+[x]+[xx]+[t]+[ii]+ [iii] for x in after_greeting for xx in yes_no for ii in five_yes for iii in two_yes for t in ['afternoon', 'morning', 'evening', 'date_day', 'confirm']]:
                reply = 'utter_acknowledgement_age'
        elif len_a == 7:
            if only_intents in [['start_conversation']+[x]+[xx]+[ii]+[t]+ [iii] + [iiii] for x in after_greeting for xx in yes_no for ii in two_no for iii in five_yes for iiii in two_yes for t in ['afternoon', 'morning', 'evening', 'date_day', 'confirm']]:
                reply = 'utter_acknowledgement_age'
              

        #solve the multiscript
        print("{}, action: {}, reply: {}, intent: {}".format(self.name(), only_actions[-1], reply, only_intents[-1]))

        if only_intents[-1] == "already_done" and only_actions[-1] == "utter_ask_want_to_continue":
            return []
        #solve already-done
        if only_intents[-1] == "already_done":
            reply = "utter_done_nomination"

        #solve the already-done count
        if only_intents.count('already_done') >= 2:
            reply = "utter_ask_goodbye"
        
        #slolve already-done with reject
        print(only_intents, only_actions)
        if only_intents[-1] == "reject" and "utter_ask_want_to_continue" in only_actions:
            reply = "utter_ask_goodbye"


        print("{}, action: {}, reply: {}, intent: {}".format(self.name(), only_actions[-1], reply, only_intents[-1]))
        
        dispatcher.utter_message(response = reply)
        return []


class action_busy_reply(Action):

    def name(self) -> Text:
        return "action_busy_reply"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        a = tracker.events

        only_actions = []
        only_intents = []

        for x in a:
            if x['event'] == 'user':
                only_intents.append(x['parse_data']['intent']['name'])
            elif x['event'] == 'bot':
                try:
                    only_actions.append(x['metadata']['utter_action'])
                except:
                    pass
        


        replies = 	{ "already_have_agent":"utter_agent_followup",
						"who_is": "utter_ask_am_i_ashley",
						"utter_fallback":  "nlu_fallback",
						"question_why_cpf_and_prudential" : "utter_value_added_service", 
						"looking_for":"utter_ask_am_i_ashley",
						"question_related_to_scam": "utter_scam_reply",
						"question_related_to_distribution": "utter_distributions_info",
						"question_related_to_disclosure_details": "utter_disclose_nomination_info",
						"question_related_to_numbers": "utter_numbers_info",
						"cpf_account_distribution":  "utter_types_of_account_distribution",
						"question_related_to_witness":"utter_witness_info",
						"call_back_to_another_party": "utter_call_others",
						"question_related_to_who_i_can_nominate": "utter_nomination_criteria_info",
                        "question_why_cpf_and_prudential":"utter_value_added_services",
                        "question_related_to_email_request":"utter_ask_email",
                        "afternoon":"utter_greeting_sharon_prudential"
				    }
       
        print('action_busy_reply', only_intents, only_actions)
        for intent, ans in replies.items():
            if intent == only_intents[-1]:
                reply = ans
                break
            else:
                reply = 'utter_ask_goodbye'

        if only_intents.count('busy') > 1:
                reply = 'utter_ask_goodbye'

        print("{}, action: {}, reply: {}, intent: {}".format(self.name(), only_actions[-1], reply, only_intents[-1]))
        dispatcher.utter_message(response = reply)
        return []


