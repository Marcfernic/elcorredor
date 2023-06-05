def mix(a,b):
    mix=[]
    if len(a)==len(b):
        for n in range(0, len(a), 1):
            txt = [n+1,a[n],b[n]]
            mix.append(txt)
    elif len(a)>len(b):
        for n in range(0, len(b), 1):
            txt = [n+1,a[n],b[n]]
            mix.append(txt)
    elif len(a)<len(b):
        for n in range(0, len(a), 1):
            txt = [n+1,a[n],b[n]]
            mix.append(txt)
    else:
        mix = ""

    return mix

def sayCon(con, noc):
    num = len(con['consulta_dnp']['bico']['lcons']['cons'])
    lis = []
    if num > 1:
        for n in range(0,num,1):
            if noc == "Deportivo" or noc == "Residencial":
                lis.append(con['consulta_dnp']['bico']['lcons']['cons'][n]['lcd'])
            elif noc == "Espectaculos" or noc == "Religioso":
                lis.append(con['consulta_dnp']['bico']['lcons']['cons']['lcd'])
            else:
                print(noc)
    elif num == 1:
        lis.append(con['consulta_dnp']['bico']['lcons']['cons']['lcd'])
    else:
        lis = ""

    return lis

def revelSup(sup):
    num = len(sup['consulta_dnp']['bico']['bi']['debi'])
    lis = []
    if num > 1:
        for n in range(0,num,1):
            lis.append(sup['consulta_dnp']['bico']['bi']['debi']['sfc'])
    elif num == 1:
        lis.append(sup['consulta_dnp']['bico']['bi']['debi']['sfc'])
    else:
        a = sup['consulta_dnp']['bico']['bi']['dt']['loine']['cm']
        b = sup['consulta_dnp']['bico']['bi']['dt']['cmc']
        c = sup['consulta_dnp']['bico']['bi']['debi']['cpt']
        lis = lis.append(a + b + c)

    return lis


def revelSur(sur, rus):
    num = len(sur['consulta_dnp']['bico']['lspr']['spr'])
    lis = []
    print(rus)
    if num > 1:
        for n in range(0,num,1):
            if rus[n] == "AGRIOS REGADÍO" or rus[n] == "LABOR O LABRADÍO REGADÍO":
                lis.append(sur['consulta_dnp']['bico']['lspr']['spr']['dspr']['ssp'])
            else: 
                lis.append(sur['consulta_dnp']['bico']['lspr']['spr'][n]['dspr']['ssp'])
    elif num == 1:
        lis.append(sur['consulta_dnp']['bico']['lspr']['spr']['dspr']['ssp'])
    else:
        lis = ""

    return lis

def sayCul(cul, luc):
    num = len(cul['consulta_dnp']['bico']['lspr']['spr'])
    lis = []
    print(luc)
    if num > 1:
        for n in range(0,num,1):
            try:
                lis.append(cul['consulta_dnp']['bico']['lspr']['spr']['dspr']['dcc'])
            except: 
                lis.append(cul['consulta_dnp']['bico']['lspr']['spr'][n]['dspr']['dcc'])
            else:
                pass
    elif num == 1:
        lis.append(cul['consulta_dnp']['bico']['lspr']['spr']['dspr']['dcc'])
    else:
        lis = ""

    return lis


def sayCla(cla):
    try:
        letter = cla['consulta_dnp']['bico']['bi']['idbi']['cn']
    except:
        letter = "No tenemos acceso a este dato"
    else:
        if letter == 'UR': 
            letter = 'Urbano'
        elif letter == 'RU': 
            letter = 'Rústico'
        else:
            letter = 'De caracter especial'

    return letter


def sayUs(us):
    try:
        letter = us['consulta_dnp']['bico']['bi']['debi']['luso']
    except:
        letter = "No tenemos acceso a este dato"
    finally:
        pass

    return letter

def extractProv(street):
    a = street
    b = c = ""
    
    for x in reversed(a):
        if x == "(":
            break
        else:
            b = b + x
    
    for y in reversed(b):
        if y ==")":
            break
        else:
            c = c + y

    return c


def extractMun(street):
    a = street
    b = c = d = ""
    
    for x in a:
        if x == "(":
            break
        else:
            b=b+x

    for y in reversed(b):
        if y.isdigit() or y == ".":
            break
        else:
            c = c+y     
    
    for z in reversed(c):
        d = d + z
    
    return d.lstrip()


