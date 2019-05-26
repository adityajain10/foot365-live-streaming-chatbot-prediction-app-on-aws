import json
import os
import math
import dateutil.parser
import datetime
import time
import boto3 
import logging
from botocore.vendored import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

arr1=[]
arr2=[]
bus=[]
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
    
def close1(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response

def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
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


""" --- Functions that control the bot's behavior --- """

def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False

def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')

def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def lambda_handler(event, context):
    # TODO implement
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    print(event)
    #logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)

def dispatch(intent_request):
    #logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
    print(intent_request)
    intent_name = intent_request['currentIntent']['name']
    
    if intent_name == 'Greetings':
        return greeting_intent(intent_request)
    elif intent_name == 'fixture':
        return fixture_intent(intent_request)
    elif intent_name == 'matchresult':
        return match_intent(intent_request)
    elif intent_name == 'Footsuggest':
        return dining_suggestion_intent(intent_request)
    elif intent_name == 'uberintent':
        return uber_intent(intent_request)
    elif intent_name == 'ThankYouIntent':
        return thank_you_intent(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')

def greeting_intent(intent_request):
    return {
        'dialogAction': {
            "type": "ElicitIntent",
            'message': {
                'contentType': 'PlainText',
                'content': 'Hi there, how can I help?'}
        }
    }

def thank_you_intent(intent_request):
    return {
        'dialogAction': {
            "type": "ElicitIntent",
            'message': {
                'contentType': 'PlainText',
                'content': 'You are welcome!'}
        }
    }
def validate_dining_suggestion(team, date, city, phone):
    return build_validation_result(True, True, None)
    
def validate_uber_suggestion(uber):
    return build_validation_result(True, True, None)


def match_intent(intent_request):

    team = get_slots(intent_request)["team"]
    date1 = get_slots(intent_request)["fromdate"]
    date2 = get_slots(intent_request)["todate"]
    #city = get_slots(intent_request)["city"]
    print "phone is accepting"
    phone = get_slots(intent_request)["phone"]
    source = intent_request['invocationSource']
    



    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)
        validation_result = validate_dining_suggestion('', '', '', '')

        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}


        return delegate(output_session_attributes, get_slots(intent_request))
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='StandardSQS')
    msg = {"team" : team,"phone":phone, "start_date":date1, "end_date":date2}
    print('msg',msg)
    if phone:
        response = queue.send_message(MessageBody=json.dumps(msg))
        print(response)
        print "phone is accepted"

    return close(intent_request['sessionAttributes'],
             'Fulfilled',
             {'contentType': 'PlainText',
              'content': "We will send you the information shortly"})


def uber_intent(intent_request):
    uber = get_slots(intent_request)["uber"]
    print "phone is accepting"
    source = intent_request['invocationSource']


    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)

        validation_result = validate_uber_suggestion(uber)

        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}


        return delegate(output_session_attributes, get_slots(intent_request))


    

    resultData = "https://m.uber.com/looking/finalize?destination=%7B%22latitude%22:"+str(arr1[int(uber)-1])+",%22longitude%22:"+str(arr2[int(uber)-1])+",%22title%22:%22"+str(bus[int(uber)-1]).strip().replace(' ','%20')+"%22title%7D&vehicleView=a1111c8c-c720-46c3-8534-2fcdd730040d&link_text=View%20team%20roster&partner_deeplink=partner%3A%2F%2Fteam%2F9383"

    return close1(intent_request['sessionAttributes'],
             'Fulfilled',
             {'contentType': 'PlainText',
              'content': resultData})


def dining_suggestion_intent(intent_request):
    team = get_slots(intent_request)["team"]
    date = get_slots(intent_request)["date"]
    city = get_slots(intent_request)["city"]
    print "phone is accepting"
    phone = get_slots(intent_request)["phone"]
    source = intent_request['invocationSource']


    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)

        validation_result = validate_dining_suggestion(team, date, city, phone)

        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}


        return delegate(output_session_attributes, get_slots(intent_request))


    # Add Yelp API endpoint to get the data

    resultData = restaurantApiCall(team, date, city, phone)

    # resultData = ''
    return close(intent_request['sessionAttributes'],
             'Fulfilled',
             {'contentType': 'PlainText',
              'content': resultData})


def restaurantApiCall(team, date, city, phone):

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=Football%20match%20screening%20in+"+city+"&key=AIzaSyBPPIx4k5_Grm4NS1Rw0fvY61qq5dCfd9o"
    payload = ""
    

    response = requests.request("GET", url, data=payload)
    message = json.loads(response.text)
    textString = "Hello! These are some suggestions: "
    count = 1
    
    for business in message["results"]:
        textString = textString + "\n" + str(count) + "." + business["name"] + " Rating: "+str(business["rating"])
        count += 1
        arr1.append(business["geometry"]["location"]["lat"])
        arr2.append(business["geometry"]["location"]["lng"])
        #bb=str(business["name"])
        bus.append(str(business["name"]))
    print("arr:",arr1,arr2)
    textString = textString + "\n"+" Enjoy your Match"
    print(textString)
    return textString
