import sys

entry = sys.argv

path = entry[1]


with open(path, 'r', encoding='utf-8') as f:
    linije = f.readlines()


klijentska_podmreža_prenesenih_bajtova = {} 
for l in linije:
    dijelovi = l.split(' ')
    ip = dijelovi[0]
    broj_bajtova = dijelovi[9]
    broj_bajtova = broj_bajtova.replace('\n', '')
    ip_dijelovi = ip.split('.')
    
    ip_dijelovi[2] = '*'
    ip_dijelovi[3] = '*'
    
    ip = '.'.join(ip_dijelovi)
    
    if broj_bajtova != '-':
        if ip in klijentska_podmreža_prenesenih_bajtova:
            klijentska_podmreža_prenesenih_bajtova[ip] = klijentska_podmreža_prenesenih_bajtova[ip] + int(broj_bajtova)
        else:
            klijentska_podmreža_prenesenih_bajtova[ip] = int(broj_bajtova)
    
entorke = []
for k, v in klijentska_podmreža_prenesenih_bajtova.items():
    entorke.append((k, v))
sortirano = sorted(entorke, key=lambda t: t[1], reverse=True)
#print(sortirano)

print('--------------------------------')
print('  IP adrese   |  Br. pristupa   ')
print('--------------------------------')
for e in sortirano:
    k, v = e
    print(f"  {k:<14} {v:>6}")
print('--------------------------------')