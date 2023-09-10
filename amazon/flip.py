import aiohttp
import asyncio
import json
def search_flip(prod):
    async def main(prod):
    
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://www.flipkart.com/search?q='+prod) as r:

                print("Status:", r.status)
                 
                page = await r.text()

            return page    
    all_prod = asyncio.run(main(prod))
    pro = all_prod.split('<img loading="eager" ')
    
    i=1
    result =[]
    while i < len(pro):
        try :
            link = "https://flipkart.com"+pro[i].split('target="_blank" rel="noopener noreferrer" href="')[1].split('?')[0]
            name = pro[i].split(' alt="')[1].split('" src=')[0]
            #print(i)
            if prod not in name :
                pass
            img = pro[i].split('src="')[1].split('"/></div>')[0]
            price = int(pro[i].split('<div class="_30jeq3')[1].split('">')[1].split('</div>')[0].replace('₹','').replace(',',''))
            rate = pro[i].split('<div class="_3LWZlK">')[1].split('<')[0]
            result.append({'Name' : name, 'Link': link,'Price' : price,'Image' : img,'Ratings':rate})
            i+=1
        except Exception as e:
            pass
            print('error',e)
            break
        final = { "status": True,
  "total_result": len(pro),
  "query": prod,
  'Result' : result}
    
    return final
#r= search_flip('realme Buds 2')
#print(r)