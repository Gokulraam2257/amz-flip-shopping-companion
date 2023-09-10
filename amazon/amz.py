import aiohttp
import asyncio

def search_amz(prod):
    async def main(prod):
    
        async with aiohttp.ClientSession() as ses:
            async with ses.get('https://www.amazon.in/s?k='+prod) as r:

                print("Status:", r.status)
                if r.status !=200:
                    return await main(prod)
                
                page = await r.text()

            return page      


    #prod = 'Realme Buds 2'
    all_prod = asyncio.run(main(prod))

    all = all_prod.split('<div class="a-section aok-relative s-image-fixed-height">')
    result = []
    i =1
    while i <= len(all):
        try:
            prod_link = "https://www.amazon.in" + all[i].split('<a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" target="_blank" href="')[1].split('"')[0]
            if '/gp/slredirect/' in prod_link:
                print('yes')
                continue
            name = all[i].split('<span class="a-size-medium a-color-base a-text-normal">')[1].split('</span>')[0]
            img = all[i].split('<img class="s-image" src="')[1].split('" srcset="')[0]
            price = int(all[i].split('<span class="a-price" data-a-size="xl" data-a-color="base"><span class="a-offscreen">')[1].split('</span>')[0].replace("₹", "").replace(',',''))
            rate = all[i].split('<span aria-label="')[1].split(' out')[0]
            result.append({'Name':name, 'Link' : prod_link,'Price':price, 'Image': img, 'Ratings': rate})
            
        except Exception as e:
            pass
            #print('error :', e)
           
        i+=1
        final = { "status": True,
  "total_result": len(all),
  "query": prod,
  'Result' : result}
    return final
    
#print( search_amz('redmi Note 5 pro'))