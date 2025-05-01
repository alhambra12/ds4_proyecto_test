path = 'c:/Users/astra/UNISON/desarrollo4/ds4_proyecto/scrapper/../datos/json/scrap_test.json'

def fix_path(path):
    path = path.split('/')
    while '..' in path:
        i = path.index('..')
        if i > 0:
            del path[i - 1:i + 1]
        else:
            del path[i]
    return '/'.join(path)


path = fix_path(path)

print(path)
