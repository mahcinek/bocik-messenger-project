import os
import sys
import json

import requests
from flask import Flask, request



def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

app = create_app()
#hadrkodowane dane w szablonie do zmiany
#https://graph.facebook.com/1347510408605737?access_token=EAAEGLZAp4dEkBABeXxaRDIQGBkzE5cSv0NBwHFsvKxcgPrRR1DCnkT2Ugs9SdDlGmGPYuokgrJ3OJLZBRgzICEGXt5dVqUQativxqwzpgBiBwNl0MmImZB8GcjcPwMj9DFj0KZB75LF9sLpVq3Vc1qj4KPNyM2q5Ut2ngBa2cAZDZD
app.config['TESTING'] = True

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

tok="EAAEGLZAp4dEkBABeXxaRDIQGBkzE5cSv0NBwHFsvKxcgPrRR1DCnkT2Ugs9SdDlGmGPYuokgrJ3OJLZBRgzICEGXt5dVqUQativxqwzpgBiBwNl0MmImZB8GcjcPwMj9DFj0KZB75LF9sLpVq3Vc1qj4KPNyM2q5Ut2ngBa2cAZDZD"
@app.route('/', methods=['POST'])
def webhook():
    token ="Pfy5udy0R98KnsgvbPo1KIaIbeM" #hardkondowany token zmienic przy pordukcji
    # endpoint

    data = request.get_json()

    def get_token():
        return requests.get("https://graph.facebook.com/oauth/access_token?client_id=288267911590985&client_secret=dca90cbc4ea68a43962dd3aa51d9c089&grant_type=client_credentials").content

    def get_user(id):
        r = requests.get("https://graph.facebook.com/" + id + "?access_token=" + tok)
        return r.json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # jest wiadomosc

                    sender_id = messaging_event["sender"]["id"]        # messenger id wysylajacego
                    recipient_id = messaging_event["recipient"]["id"]  # messenger id odbiorcy
                    message_text = messaging_event["message"]["text"]  # text wiadomosci

                if (message_text=="test"):
                    send_message(sender_id,"thanks!")
                elif (message_text=="Hi"):
                    jsonn=get_user(sender_id)
                    send_message(sender_id,"Witaj " +jsonn.get("first_name") + " "+ jsonn.get("last_name") )
                elif (message_text=="whoami"):
                    jsonn=get_user(sender_id)
                    send_message(sender_id, jsonn.get("first_name") + " "+ jsonn.get("last_name") )
                elif (message_text=="1"):
                    send_message(sender_id, "Wybrano 1")
                elif (message_text=="2"):
                    send_message(sender_id, "Wybrano 2")
                elif (message_text=="getToken"):
                    token = get_token()
                    a, b = token.split("|")
                    token=b
                    send_message(sender_id,b)
                elif (message_text=="getPerson"):
                    get_user(sender_id,token)
                elif (message_text=="Id"):
                    send_message(sender_id,sender_id)
                elif(message_text=="question"):
                    send_quick_question(sender_id,"question",["1","2"])
                else: send_message(sender_id, "error")

                if messaging_event.get("delivery"):  # potwierdzenie dostarczenia
                    pass

                if messaging_event.get("optin"):  # optin
                    pass

                if messaging_event.get("postback"):  # kliniecie na postback
                    pass

    return "ok", 200

def send_quick_question (recipient_id, message_text,options): #szybie pytanie
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": options[0],
                    "payload": "first",
                },
                {
                    "content_type": "text",
                    "title": options[1],
                    "payload": "second",
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_message(recipient_id, message_text): #wyslij odpowiedz

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # log do heroku
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
