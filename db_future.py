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
            (id int auto_increment, 
            url text, 
            author text, 
            title text, 
            image text, 
            ingredients_list int, 
            prep_time int, 
            cook_time int, 
            yield int, 
            level int, 
            PRIMARY KEY('id')
            )
        ''')
        c.execute('''CREATE TABLE IF NOT EXISTS primary_ingredient
            (id int auto_increment,
            name text,
            PRIMARY KEY('id')
            )
        ''')
        c.execute('''CREATE TABLE IF NOT EXISTS ingredient
            (id int auto_increment,
            recipe_ID int NULL,
            name text, 
            calories int, 
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
            PRIMARY KEY('id'),
            FOREIGN KEY('recipe_id') REFERENCES recipe('id')
            )
        ''')
        c.execute('''CREATE TABLE IF NOT EXISTS ingredients_list
            (id int auto_increment, 
            qty int, 
            ingredient_id int, 
            recipe_id int, 
            PRIMARY KEY('id'), 
            FOREIGN KEY('ingredient_id') REFERENCES ingredient('id'),
            FOREIGN KEY('recipe_id') REFERENCES recipe('id')
            )
        ''')
        c.execute('''CREATE TABLE IF NOT EXISTS directions_list
            (id int auto_increment, 
            step text,
            stepNum int,
            recipe_id int,
            PRIMARY KEY('id'),
            FOREIGN KEY('recipe_id') REFERENCES recipe('id')
            )
        ''')
        
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def setRecipe(self, url, title, author, image, prep_time, cook_time, servings, level, ingredients, directions):
        """
        store the content for a given id and relative url
        """
        self.cursor.execute("INSERT INTO recipes VALUES (?,?,?,?,?,?,?,?)",
            (url, title, author, image, prep_time, cook_time, servings, level))
        recipe_id = self.cursor.lastrowid
        for i in ingredients:
            self.cursor.execute("INSERT INTO ingredient VALUES (?,?)", (recipe_id, i))
        for d in directions:
            self.cursor.execure("INSERT INTO direction", (recipe_id, d))
        self.conn.commit()

    def get(self, id, url):
        """
        return the content for a given id and relative url
        """
        self.cursor.execute("SELECT content FROM recipes WHERE id=? and url=?",
            (id, url))
        row = self.cursor.fetchone()
        if row:
            return row[0]

    def get_urls(self, id):
        """
        return all the URLS within a id
        """
        self.cursor.execute("SELECT url FROM recipes WHERE id=?", (id,))
        # could use fetchone and yield but I want to release
        # my cursor after the call. I could have create a new cursor tho.
        # ...Oh well
        return [row[0] for row in self.cursor.fetchall()]