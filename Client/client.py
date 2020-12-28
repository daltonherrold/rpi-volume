import requests

IP = 'http://192.168.1.11:5000'

def get_processes():
    return requests.get(IP+'/get_all_volume').json()['processes']


def increment(name):
    data = {
        'process': name,
    }
    response = requests.post(IP+'/increment_process_volume', data=data)
    return response.json()


def decrement(name):
    data = {
        'process': name,
    }
    response = requests.post(IP+'/decrement_process_volume', data=data)
    return response.json()
