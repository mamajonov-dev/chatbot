import requests


def getconvertvalut(fromvalut, tovalut, amount):
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={tovalut}&from={fromvalut}&amount={amount}"

    payload = {}
    headers = {
        "apikey": "GeXbjjj6Mgd71cM0DTG8nm4PVKha8L79"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    result = response.json()

    return result, status_code




def getsymols():


    url = "https://api.apilayer.com/exchangerates_data/symbols"

    payload = {}
    headers = {
        "apikey": "Your api Ozdbekini"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    result = response.json()
    return result
