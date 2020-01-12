import sqlite3 
#import firebase_admin
#from google.cloud import firestore
#from firebase_admin import credentials

class Database(object): 
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        c = self.conn.cursor()
        c.execute('''PRAGMA foreign_keys = ON''')
        c.execute('''CREATE TABLE IF NOT EXISTS recipe
            (id INTEGER PRIMARY KEY, 
            url text, 
            author text, 
            title text, 
            image text, 
            prep_time int, 
            cook_time int,
            total_time int,
            inactive_time,
            yield int, 
            level int
            )
        ''')
        c.execute('''CREATE TABLE IF NOT EXISTS primary_ingredient
            (id INTEGER PRIMARY KEY,
            name text
            )
        ''')
        c.execute('''CREATE TABLE IF NOT EXISTS ingredient
            (id INTEGER PRIMARY KEY,
            recipe_id int,
            name text, 
            calories int NULL, 
            saturated int, 
            monounsaturated int, 
            polyunsaturated int, 
            cholesterol int, 
            sodium int, 
            potassium int, 
            fiber int, 
            sugar int, 
            protein int, 
            vitamin_a int, 
            vitamin_b6 int, 
            vitamin_c int, 
            vitamin_d int, 
            calcium int, 
            iron int, 
            magnesium int, 
            FOREIGN KEY('recipe_id') REFERENCES recipe('id')
            )
        ''')
        c.execute('''CREATE TABLE IF NOT EXISTS ingredients_list
            (id INTEGER PRIMARY KEY, 
            qty int, 
            ingredient_id int, 
            recipe_id int,
            FOREIGN KEY('ingredient_id') REFERENCES ingredient('id'),
            FOREIGN KEY('recipe_id') REFERENCES recipe('id')
            )
        ''')
        c.execute('''CREATE TABLE IF NOT EXISTS direction
            (id INTEGER PRIMARY KEY, 
            step text,
            stepNum int,
            recipe_id int,
            FOREIGN KEY('recipe_id') REFERENCES recipe('id')
            )
        ''')
        
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def setRecipe(self, url, title, author, image, prep_time, cook_time, inactive_time, total_time, servings, level, ingredients, directions):
        """
        store the content for a given id and relative url
        """
        if not author:
            author = 'none'
        if isinstance(author, str):
            pass
        else:
            author = author[0]

        self.cursor.execute("INSERT INTO recipe (url,author,title,image,prep_time,cook_time, inactive_time, total_time, yield,level) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (url, author, title, image, prep_time, cook_time, inactive_time, total_time, servings, level))
        recipe_id = self.cursor.lastrowid
        for i in ingredients:
            self.cursor.execute("INSERT INTO ingredient (recipe_id, name) VALUES (?,?)", (recipe_id, i))
        for d in directions:
            self.cursor.execute("INSERT INTO direction (recipe_id, step) VALUES (?, ?)", (recipe_id, d))
        """ for t in tags:
            self.cursor.execute("INSERT INTO recipe (recipe_id, tag) VALUES (?, ?)", (recipe_id, t)) """
        self.conn.commit()
    
    def isDuplicate(self, url):
        self.cursor.execute("SELECT id FROM recipe WHERE url=?",
            (url,))
        row = self.cursor.fetchone()
        if row is not None:
            return True
        else:
            return False

    def getRecipe(self, id):
        """
        return the content for a given id and relative url
        """
        self.cursor.execute("SELECT * FROM recipe WHERE id=?", (id,))
        recipe = self.cursor.fetchone()
        self.cursor.execute("SELECT name FROM ingredient WHERE recipe_id = ?", (id,))
        ingredients = self.cursor.fetchall()
        self.cursor.execute("SELECT step FROM direction WHERE recipe_id = ?", (id,))
        directions = self.cursor.fetchall()
        if recipe:
            return recipe, ingredients, directions

    def get_urls(self, id):
        """
        return all the URLS within a id
        """
        self.cursor.execute("SELECT url FROM recipe WHERE id=?", (id,))
        # could use fetchone and yield but I want to release
        # my cursor after the call. I could have create a new cursor tho.
        # ...Oh well
        return [row[0] for row in self.cursor.fetchall()]