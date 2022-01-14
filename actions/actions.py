from typing import Any, Text, Dict, List
from rasa_sdk.events import FollowupAction, ActionExecuted

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from typing import Text, List, Optional


class Validate_already_have_agent(FormValidationAction):
    def name(self) -> Text:
        return "validate_already_have_agent"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
        if not tracker.get_slot("want_to_continue"):
            slots_mapped_in_domain.append("goodbye")

        return slots_mapped_in_domain



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
                "'who_is', ", "'nlu_fallback', ", "'repeat', ",
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
        three_no = ['reject','already_done']
        four_yes = ['confirm', 'morning','afternoon','evening']
        two_yes = ['confirm', 'age']
        reply = 'utter_goodbye'
        if len_a < 4 and only_intents[-1] in ['afternoon', 'morning', 'evening']:
            reply = 'utter_busy_call_back'

        if only_intents[-1] == "repeat":
            reply = only_actions[-1]
            

        if len_a == 1:
            reply = 'utter_goodbye'
        elif len_a == 2:
            if only_intents == ['start_conversation', 'confirm']:
                reply = 'utter_discuss_nomination'
            elif only_intents == ['start_conversation', 'reject']:
                reply = 'utter_discuss_nomination'
        elif len_a == 3:
            if only_intents in [['start_conversation']+[x]+[x] for x in ['reject','already_done', 'confirm']]:
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
            if only_intents in [['start_conversation']+[x]+[x]+['confirm'] for x in ['reject','already_done', 'confirm']]:
                reply = 'utter_appointment_call_time'
            elif only_intents in [['start_conversation']+[x]+[x]+['reject'] for x in ['reject','already_done', 'confirm']]:
                reply = 'utter_convincing'
            elif only_intents in [['start_conversation']+[x]+[x]+['already_done'] for x in ['reject','already_done', 'confirm']]:
                reply = 'utter_done_nomination'

        elif len_a == 5:
            if only_intents in [['start_conversation']+[x]+[x]+[i]+['confirm'] for i in ['reject','already_done']\
            for x in ['reject','already_done', 'confirm']]:
                reply = 'utter_appointment_call_time'
            elif only_intents[:-1] in [['start_conversation']+[x]+[x]+['confirm'] for x in ['reject','already_done', 'confirm']]\
                and only_intents[-1] in ['confirm','morning','afternoon','evening']:
                reply = 'utter_age_info'
            elif only_intents in [['start_conversation']+[x]+[x]+['confirm'] for x in ['reject','already_done', 'confirm']]:
                reply = 'utter_appointment_call_time'
        elif len_a == 6:
            if only_intents[:-1] in [['start_conversation']+[x]+[x]+[i]+['confirm'] for i in ['reject','already_done'] for x in ['reject','already_done', 'confirm']]\
                and only_intents[-1] in ['confirm','morning','afternoon','evening']:
                reply = 'utter_age_info'
            elif only_intents in [['start_conversation', 'confirm', 'confirm']+[x]+['confirm']+ [i] for i in ['confirm', 'morning','afternoon','evening']\
                 for x in ['reject','already_done']]:
                reply = 'utter_age_info'
            elif only_intents in [['start_conversation']+[i]+[i]+['confirm']+[ii]+ [iii] for i in yes_no for ii in four_yes for iii in two_yes]:
                reply = 'utter_acknowledgement_age'
        elif len_a == 7:
            if only_intents in [['start_conversation']+[i]+[i]+[ii]+['confirm']+ [iii] + [iiii] for i in yes_no for ii in three_no for iii in four_yes for iiii in two_yes]:
                reply = 'utter_acknowledgement_age'
              

        dispatcher.utter_message(response = reply)
        return []


