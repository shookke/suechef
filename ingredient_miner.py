from db import Database

class Ingredient_Miner(object):
    
    def __init__(self, db_file):
        self.db = Database(db_file)
        self.test_data = self.db.getRecipe(33025)
        self.units = ['tablespoon', 'tbsp', 'teaspoon', 'tspn', 'cup', 'head', 'sprig']
    
    def printRecipe(self):
        print ('URL: ' + self.test_data[0][1] + '\n' +
                'Title: ' + self.test_data[0][3] + '\n' +
                'Author: ' + self.test_data[0][2] + '\n' +
                'Prep-time: ' + self.test_data[0][5] + '\n' +
                'Cook-time: ' + self.test_data[0][6] + '\n' +
                'Servings: ' + self.test_data[0][7] + '\n')
        for i in range(0,len(self.test_data[1])):
            print (self.test_data[1][i][0])
        for i in range(0,len(self.test_data[2])):
            print (self.test_data[2][i][0] + '\n')

test = Ingredient_Miner('parsed.db')
test.printRecipe()