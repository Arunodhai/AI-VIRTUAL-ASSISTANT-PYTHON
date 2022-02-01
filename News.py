import  requests

#use newsapi API

api_address = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=YOUR API KEY' #change country = us to get news from usa
json_data =  requests.get(api_address).json()

ar=[]

def news():
    for i in range(5):
        ar.append("News "+str(i+1)+", "+ json_data['articles'][i]['title']+".")

    return ar
