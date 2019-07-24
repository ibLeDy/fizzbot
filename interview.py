"""
GET question
POST answer
take url from POST if 200
GET new question
"""
import requests
import json
import os


def make_url(next_url):
    api_url = "https://api.noopschallenge.com/fizzbot"
    base_url = api_url.split(".com")[0]
    return base_url + ".com" + next_url

def check_data(data):
    useful_keys = ["numbers"]
    common_keys = ["message", 
                   "nextQuestion",
                   "exampleResponse",
                   "rules"]

    for k, v in data.items():
        
        if k in useful_keys:
            print("I found something", k, v)
        
        elif k not in common_keys:
            print('I found something: "', k, v, '"')
        


def start_interview():
    url = "https://api.noopschallenge.com/fizzbot"
    r = requests.get(url)
    data = json.loads(r.text)
    os.system("clear")
    print(data["message"])
    check_data(data)
    input("Press intro to begin with the Iterviewing Process =>")
    next_url = make_url(data["nextQuestion"])
    return r.status_code, next_url

def continue_interview(status_code, next_url):
    if status_code == 200:
        r = requests.get(next_url)
        data = json.loads(r.text)

        try:
            next_url = make_url(data["nextQuestion"])
        except KeyError:
            os.system("clear")
            print(data["message"])
            check_data(data)
            answer = input("\nYou may now enter your answer: ")
            head = {'Content-Type': 'application/json'}
            payload = {"answer": answer}
            result = requests.post(next_url, data=json.dumps(payload))
            data = json.loads(result.text)
            
            try:
                next_url = make_url(data["nextQuestion"])
                if next_url and result.status_code == 200:
                    return result.status_code, next_url
                else:
                    os.system("clear")
                    print("Something happened", result.status_code, result.reason)
                    input("Press intro to continue =>")
            
            except KeyError:
                os.system("clear")
                print("\nWrong answer", result.status_code, result.reason)
                input("Press intro to continue =>")
    
    else:
        os.system("clear")
        print("ERROR", r.status_code, r.reason)
        input("Press intro to continue =>")

status_code, next_url = start_interview()
interview, next_url = continue_interview(status_code, next_url)

while interview == 200:
    continue_interview(interview, next_url)
