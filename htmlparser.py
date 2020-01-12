from bs4 import BeautifulSoup
from db import Database
import time
import sqlite3


class HTMLParser(object):

    def __init__(self, db_file, lower, upper):
        # Project ID is determined by the GCLOUD_PROJECT environment variable
        #cred = credentials.Certificate("~/Keys/SueChef-cedbfca53fd7.json")
        #app = firebase_admin.initialize_app(cred)
        #self.db = firestore.Client()
        self.db = Database('parsed.db')
        self.time = time.time()
        self.conn = sqlite3.connect(db_file)
        c = self.conn.cursor()
        self.data = c.execute("SELECT domain,url,content FROM sites limit ?, ?", (lower,upper))
        self.cursor = self.conn.cursor()
        self.recipe = []
        self.total = 232596
    
    def len_of_data(self):
        count = 0
        for i in self.data:
            if i:
                count += 1
        print (count)
    
    def parse_data(self):
        directions = []
        ingredients = []
        tags = []
        num = 1
        for domain,url,html in self.data:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('span', 'o-AssetTitle__a-HeadlineText')
            img = soup.find('img', 'o-AssetMultiMedia__a-Image')
            author = soup.find('span', 'o-Attribution__a-Name')
            headline = soup.find_all('dt', 'o-RecipeInfo__a-Headline')
            description = soup.find_all('dd', 'o-RecipeInfo__a-Description')
            ingredients_list = soup.find_all('label', "o-Ingredients__a-ListItemText")
            directions_list = soup.find_all('div', "o-Method__m-Body")
            tags_list = soup.find_all('a', 'o-Capsule__a-Tag')

            if img:
                img = img.get('src')

            if tags_list:
                for i in tags_list:
                    tags.append(i.contents[0])
            if title:
                title = title.contents[0]
            
            if author:
                if len(author.contents) == 1:
                    author = author.contents[0].split()
                else:
                    author = author.contents[1].contents[0]

            if not ingredients_list:
                continue
            
            if directions_list:
                for i in directions_list[0].find_all('p'):
                    directions.append(' '.join(i.contents[0].split()))

            if ingredients_list:
                for item in ingredients_list:
                    if item.contents and not None:
                        ingredients.append(item.contents[0])

            
            self.recipe.append({'id': num, 'contents': 
                                    {
                                    'url': domain + url, 
                                    'author': author,
                                    'title': title,
                                    'image': img,
                                    'ingredients': ingredients , 
                                    'directions': directions
                                    },
                                    'tags': tags
                                })
            
            
            if headline and description:
                for h, d in zip(headline, description):
                    header = h.contents[0].strip(" \n:")
                    description = d.contents[0].strip(" \n")
                    self.recipe[num-1]['contents'].update({header: description})
            current = self.recipe[num-1]['contents']
            cook_time = ''
            prep_time = ''
            inactive_time = ''
            total_time = ''
            level = ''
            servings = ''
            if 'Yield' in current:
                servings = current['Yield']
            if 'Prep' in current:
                prep_time = current['Prep']
            if 'Cook' in current:
                cook_time = current['Cook']
            if 'Inactive' in current:
                inactive_time = current['Inactive']
            if 'Total' in current:
                total_time = current['Total']
            if 'Active' in current:
                cook_time = current['Active']
            if 'Level' in current:
                level = current['Level']
            if self.db.isDuplicate(current['url']):
                directions = []
                ingredients = []
                tags = []
                num += 1
                continue
            print (current['title'])
            self.db.setRecipe(current['url'],
                            current['title'],
                            current['author'],
                            current['image'],
                            prep_time,
                            cook_time,
                            inactive_time,
                            total_time,
                            servings,
                            level,
                            current['ingredients'],
                            current['directions']
                            # self.recipe['tags']
                            )
            directions = []
            ingredients = []
            tags = []
            num += 1
        
        #self.push_data(self.recipe, multi=True)
        """ for k,v in self.recipe[-2]['contents'].items():
            if k == 'ingredients' or k == 'directions':
                print (k.upper() + ":")
                if v:
                    if isinstance(v, int):
                        continue
                    for item in v:
                        print(item)
                
            else:
                if v and k:
                    print (k.upper() + ": " + v)
        """
        #print (self.recipe[-3])
    """ def push_data(self, data, multi):
        if multi:
            for item in data:
                self.db.collection(u'recipes').document(item['contents']['title']).set(item)
        
        print (len(self.recipe))
        print ("operation took " + str(time.time() - self.time) + " seconds.") """