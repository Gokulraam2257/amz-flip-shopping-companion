import requests
url = 'https://graph.facebook.com/v16.0/104875019237687/messages'
usr = 'Gokul Raam'
number = '918903408249'
name = 'Redmi Note 8 Pro'
    
h = {"Content-Type": "application/json",                         
     "Authorization": "Bearer EAAIlfUAt6BgBO2ZCl2zkcAMKWTAARQS6vVrrmrkDIFY85npbnzPEUiXUHuu8QxZAeI0FPZCaGSRepOStQuWRNnYvZBRp9T7i5IURBfhbZA20US4NjeqTTkBabQkqhyR9oAl3Snwfk8TXBS2BW05xKZCOE9VNikrLOoJZBbv0dtTtdaXsl27vHguJwWdwleAyhII57LtZBJc2ZBoYsrAbekdh6E88un5rO5b0zsgad"}
a = '''Hai *{}*, \n your Purchase Limit Is Crossed As You Buyed the *{}* .\n 
Be Cautious At You Purchase . \n\n Thank You For Using Our Service  
\n- *Admin*'''.format(usr,name)
d = {
    "messaging_product": "whatsapp",
    "to": number,
    "type": "text",
    "text": {
    "preview_url": True,
        "body": a,
        
    }
}
post =requests.post(url,json=d,headers=h)
s = post.status_code
js = post.json()
print(s,js)