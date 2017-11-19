import time
import os
import logging

import job_importer, faq


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


print('Loading function')


""" --- Helper functions --- """
def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def elicitIntent(session_attributes, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitIntent',
            'message': message
        }
    }

    return response


def build_response_card(title, subtitle, options):
    """
    Build a responseCard with a title, subtitle, and an optional set of 
    options which should be displayed as buttons.
    """
    buttons = None
    if options:
        buttons = []
        for i in range(min(5, len(options))):
            buttons.append(options[i])

    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'buttons': buttons
        }]
    }


# def confirmIntent(session_attributes, intent_name, message, slots, slots_to_elicit):
#     response = {
#         'sessionAttributes': session_attributes,
#         'dialogAction': {
#             'intentName': intent_name,
#             'slots': slots,
#             'slotToElicit': slots_to_elicit,
#             'type': 'ConfirmIntent',
#             'message': message
#         }
#     }

#     return response


def elicit_slot(session_attributes,
                intent_name,
                slots,
                slot_to_elicit,
                message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }

def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def validate_job_criteria(job_position,
                          job_location,
                          job_level):
    position_types = ['manager', 'tester', 'developer', 'java developer', 'software developer', 'qa']
    if job_position and job_position.lower() not in position_types:
        return build_validation_result(
            False,
            'slotPosition',
            'We do not have {}, would you like a different type of position ? Our most popular position is developer.'.format(job_position))

    types = ['professional', 'young_talent']
    if job_level and job_level.lower() not in types:
        return build_validation_result(
            False,
            'slotLevel',
            'We do not have {}, would you like a different level? Our most popular level is professional.'.format(job_level))

    location_types = ['timisoara', 'freiburg']
    if job_location and job_location.lower() not in location_types:
        return build_validation_result(
            False, 
            'slotLocation',
            'We do not have {}, would you like a different location ? Our most popular location is Freiburg.'.format(job_location))

    return build_validation_result(True, None, None)


def request_jobs(search_job_title, position):
    job_html = job_importer.get_html_jobs(
        search_job_title=search_job_title,
        position=job_importer.Position[position] if position else None)
    return list(job_importer.parse_jobs(job_html))


""" --- Methods used for intents --- """
def sayHello_findJob(intent_request):
    """ Performs the search job intent """

    job_position = get_slots(intent_request)["slotPosition"]
    job_location = get_slots(intent_request)["slotLocation"]
    job_level = get_slots(intent_request)["slotLevel"]
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)

        validation_result = validate_job_criteria(job_position, job_location, job_level)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] else {}
        return delegate(output_session_attributes, get_slots(intent_request))

    jobs = request_jobs(job_position, job_level)

    return close(
        intent_request['sessionAttributes'],
        'Fulfilled',
        {'contentType': 'PlainText',
         'content': 'I found {} positions for you. The most relevant result is {}{}.'.format(
             len(jobs),
             "https://recruitingapp-2388.umantis.com",
             jobs[0]["job_link"])})


def findAllJobs(intent_request):
    jobs = request_jobs(None, None)

    return close(
        intent_request['sessionAttributes'],
        'Fulfilled',
        {'contentType': 'PlainText',
         'content': 'I found {} positions for you. Have a look at {}.'.format(
             len(jobs),
             "https://recruitingapp-2388.umantis.com/Jobs/All")})


def answer_faq(intent_request, faq_type):
    return close(
        intent_request['sessionAttributes'],
        "Fulfilled",
        {'contentType': 'PlainText',
         'content': faq.get_content(faq_type)})


def startBot(intent_request):
    return close(
        intent_request['sessionAttributes'],
        'Fulfilled',
        {'contentType': 'PlainText',
         'content': 'How can I help?'})


""" --- Intents --- """
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    logger.debug(
        'dispatch userId={}, intentName={}'.format(
            intent_request['userId'],
            intent_request['currentIntent']['name']))
    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'SearchJob':
        return sayHello_findJob(intent_request)
    elif intent_name == 'SearchAllJobs':
        return findAllJobs(intent_request)
    elif intent_name == 'AskStelleNochVakant':
        return answer_faq(intent_request, faq.FaqType.JOB_STILL_VACANT)
    elif intent_name == 'AskIsJobFulltimeOrParttime':
        return answer_faq(intent_request, faq.FaqType.JOB_FULL_OR_PARTTIME)
    elif intent_name == 'StartBot':
        return startBot(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()

    return dispatch(event)
