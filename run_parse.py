from htmlparser import HTMLParser

offset = 0
increment = 100
total = 232596
parsing = True

while parsing:
    if offset > total:
        offset = total
    print ('Parsing records ' + str(offset) + ' to ' + str(offset + increment))
    toparse = HTMLParser('crawler.db', offset, increment)
    toparse.parse_data()
    if offset == total:
        parsing = False
    offset = offset + increment
    

#toparse.len_of_data()