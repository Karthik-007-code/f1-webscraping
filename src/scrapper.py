#this file is used for getting the response by making the request on to the url 

import requests
def geting_req(F1_url,header):
    try:
        response=requests.get(F1_url,header)
        print(f"Succesfully got the response(HTML page) in response.content") # in response.content we can get the whole html page 
        return response.content
    except Exception as e:
        print(e)
        return e


