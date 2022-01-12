from typing import Any, Text, Dict, List
from rasa_sdk.events import FollowupAction, ActionExecuted

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class action_fast_sharon(Action):

    def name(self) -> Text:
        return "action_fast_sharon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        a = tracker.events

        story_list = []
        only_intents = []

        for x in a:
            if x['event'] == 'user':
                story_list.append(x['parse_data']['intent']['name'])
                only_intents.append(x['parse_data']['intent']['name'])
            elif x['event'] == 'bot':
                try:
                    story_list.append(x['metadata']['utter_action'])
                except:
                    pass

                
        #only_intents = ["start_conversation","confirm","reject","confirm","who_is","confirm","confirm","age"]        

            
        rules = ["'reject', 'already_done'",
                "'who_is', ", "'nlu_fallback', ",
                "'looking_for', ",
                "'question_related_to_singpass_checking', ",
                "'question_related_to_fees', ",
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

        yes_no = ['reject','already_done','already_have_agent', 'confirm']
        three_no = ['reject','already_done','already_have_agent']
        four_yes = ['confirm', 'morning','afternoon','evening']
        two_yes = ['confirm', 'age']
        reply = 'utter_goodbye'
        if len_a < 4 and only_intents[-1] in ['afternoon', 'morning', 'evening']:
            reply = 'utter_busy_call_back'

            
        if len_a == 1:
            reply = 'utter_goodbye'
        elif len_a == 2:
            if only_intents == ['start_conversation', 'confirm']:
                reply = 'utter_discuss_nomination'
            elif only_intents == ['start_conversation', 'reject']:
                reply = 'utter_discuss_nomination'
        elif len_a == 3:
            if only_intents in [['start_conversation', 'confirm']+[x] for x in ['reject','already_done','already_have_agent', 'confirm']]:
                reply = 'utter_purpose'
            # elif only_intents == ['start_conversation', 'confirm', 'reject']:
            #     reply = 'utter_convincing'
            # elif only_intents == ['start_conversation', 'confirm', 'already_done']:
            #     reply = 'utter_done_nomination'
            # elif only_intents == ['start_conversation', 'confirm', 'already_have_agent']:
            #     reply = 'utter_agent_followup'
            elif only_intents == ['start_conversation', 'reject', 'confirm']:
                reply = 'utter_purpose'
        elif len_a == 4:
            # contains any of the rejections
            # if only_intents in [['start_conversation', 'confirm']+[x]+['confirm'] for x in ['reject','already_done','already_have_agent']]:
            #     reply = 'utter_appointment_call_time'
            if only_intents in [['start_conversation', 'confirm']+[x]+['confirm'] for x in ['reject','already_done','already_have_agent', 'confirm']]:
                reply = 'utter_appointment_call_time'
            elif only_intents[:-1] == ['start_conversation', 'reject', 'confirm']\
                and only_intents[-1] in ['confirm']:
                reply = 'utter_appointment_call_time'
            elif only_intents in [['start_conversation', 'confirm']+[x]+['reject'] for x in ['reject','already_done','already_have_agent', 'confirm']]:
                reply = 'utter_convincing'
            elif only_intents in [['start_conversation', 'confirm']+[x]+['already_done'] for x in ['reject','already_done','already_have_agent', 'confirm']]:
                reply = 'utter_done_nomination'
            elif only_intents in  [['start_conversation', 'confirm']+[x]+['already_have_agent'] for x in ['reject','already_done','already_have_agent', 'confirm']]:
                reply = 'utter_agent_followup'
            elif only_intents == ['start_conversation', 'reject', 'confirm', 'reject']:
                reply = 'utter_convincing'
            elif only_intents == ['start_conversation', 'reject', 'confirm', 'already_done']:
                reply = 'utter_done_nomination'
            elif only_intents == ['start_conversation', 'reject', 'confirm', 'already_have_agent']:
                reply = 'utter_agent_followup'
        elif len_a == 5:
            if only_intents in [['start_conversation', 'confirm']+[x]+[i]+['confirm'] for i in ['reject','already_done','already_have_agent']\
            for x in ['reject','already_done','already_have_agent', 'confirm']]:
                reply = 'utter_appointment_call_time'
            elif only_intents[:-1] in [['start_conversation', 'confirm']+[x]+['confirm'] for x in ['reject','already_done','already_have_agent', 'confirm']]\
                and only_intents[-1] in ['confirm','morning','afternoon','evening']:
                reply = 'utter_age_info'
            elif only_intents in [['start_conversation', 'reject', 'confirm']+[x]+['confirm'] for x in ['reject','already_done','already_have_agent']]:
                reply = 'utter_appointment_call_time'
            elif only_intents in [['start_conversation', 'confirm']+[x]+['confirm'] for x in ['reject','already_done','already_have_agent', 'confirm']]:
                reply = 'utter_appointment_call_time'
        elif len_a == 6:
            if only_intents[:-1] in [['start_conversation', 'confirm']+[x]+[i]+['confirm'] for i in ['reject','already_done','already_have_agent'] for x in ['reject','already_done','already_have_agent', 'confirm']]\
                and only_intents[-1] in ['confirm','morning','afternoon','evening']:
                reply = 'utter_age_info'
            elif only_intents in [['start_conversation', 'confirm', 'confirm']+[x]+['confirm']+ [i] for i in ['confirm', 'morning','afternoon','evening']\
                 for x in ['reject','already_done','already_have_agent']]:
                reply = 'utter_age_info'
            elif only_intents[:-1] == ['start_conversation', 'reject', 'confirm', 'confirm']\
                and only_intents[-1] in ['confirm','morning','afternoon','evening']:
                reply = 'utter_age_info'
            elif only_intents in [['start_conversation', 'reject', 'confirm']+[x]+['confirm']+ [i] for i in ['confirm', 'morning','afternoon','evening']\
                 for x in ['reject','already_done','already_have_agent']]:
                reply = 'utter_age_info'
            elif only_intents in [['start_conversation', 'confirm']+[i]+['confirm']+[ii]+ [iii] for i in yes_no for ii in four_yes for iii in two_yes]:
                reply = 'utter_goodbye_conversion'
            elif only_intents in [['start_conversation', 'reject']+['confirm']+['confirm']+[i]+[ii] for i in four_yes for ii in two_yes]:
                reply = 'utter_goodbye_conversion'
        elif len_a == 7:
            if only_intents in [['start_conversation', 'confirm']+[i]+[ii]+['confirm']+ [iii] + [iiii] for i in yes_no for ii in three_no for iii in four_yes for iiii in two_yes]:
                reply = 'utter_goodbye_conversion'
            elif only_intents in [['start_conversation', 'reject']+['confirm']+[i]+['confirm']+[ii]+[iii] for i in three_no for ii in four_yes for iii in two_yes]:
                reply = 'utter_goodbye_conversion'
                

        dispatcher.utter_message(response = reply)
        return []


