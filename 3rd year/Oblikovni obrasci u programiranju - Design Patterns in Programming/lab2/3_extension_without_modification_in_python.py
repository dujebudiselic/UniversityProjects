def mymax(iterable, key=lambda x: x):
    max_x = max_key = None

    for x in iterable:
        current = key(x)
        if max_key is None or current > max_key:
            max_x = x
            max_key = current

    return max_x

maxlenstr = mymax(["Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"], key=lambda x: len(x))
print(maxlenstr)

maxint = mymax([1, 3, 5, 7, 4, 6, 9, 2, 0])
maxchar = mymax("Suncana strana ulice")
maxstring = mymax(["Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"])
print(maxint)
print(maxchar)
print(maxstring)

D = {'burek': 8, 'buhtla': 5}
maxD = mymax(D, key=D.get)
print(maxD)

maxnamelastname = mymax([("Duje", "Budiselic"), ("Ana", "Pet"), ("Marko", "Livaja"), ("Duje", "Brodic")])
print(maxnamelastname)

# zašto metodu možemo koristiti kao slobodnu funkciju:
# zato što se gleda kao objekt
