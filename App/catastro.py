def mix(a,b):
    mix=[]
    if b == "":
        for n in range(0, len(a), 1):
                txt = [n+1,a[n],"-"]
                mix.append(txt)
    else:
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
            mix = [["-","-", "-"]]

    return mix


def proFloor(floor, ex):
    num = 0
    options = ""
    if ex == "No tenemos acceso a este dato":
        lis = ""
    else:
        try:
            num = len(floor['consulta_dnp']['bico']['bi']['debi'])
            options = "a"
        except:
            num = len(floor['consulta_dnp']['bico']['lspr']['spr'])
            options = "b"
        finally:
            lis = []
            if num > 1:
                for n in range(0,num,1):
                    if options == "a":
                        lis.append(floor['consulta_dnp']['bico']['bi']['debi']['sfc'])  
                    if options == "b":
                        try:
                            lis.append(floor['consulta_dnp']['bico']['lspr']['spr']['dspr']['ssp'])
                        except: 
                            lis.append(floor['consulta_dnp']['bico']['lspr']['spr'][n]['dspr']['ssp']) 
            elif num == 1:
                if options == "a":
                    try:
                        lis.append(floor['consulta_dnp']['bico']['bi']['debi']['sfc'])
                    except:
                        lis.append(floor['consulta_dnp']['bico']['lspr']['spr']['dspr']['ssp'])
                if options == "b":
                    lis.append(floor['consulta_dnp']['bico']['lspr']['spr']['dspr']['ssp'])
            else:
                if options == "a":
                    a = floor['consulta_dnp']['bico']['bi']['dt']['loine']['cm']
                    b = floor['consulta_dnp']['bico']['bi']['dt']['cmc']
                    c = floor['consulta_dnp']['bico']['bi']['debi']['cpt']
                    lis = lis.append(a + b + c)
                else:
                    lis = ""

    return lis


def proTyp(typ, ex):
    options = ""
    num = 0
    if ex == "No tenemos acceso a este dato":
        lis = []
        try:
            num = len(typ['consulta_dnp']['lrcdnp']['rcdnp'])
            if num > 1:
                for n in range(0,num,1):
                    try:
                        lis.append(typ['consulta_dnp']['lrcdnp']['rcdnp'][n]['dt']['locs']['lous']['lourb']['dir']['nv'])
                    except:
                        lis.append(typ['consulta_dnp']['lrcdnp']['rcdnp']['dt']['locs']['lous']['lourb']['dir']['nv'])
            elif num == 1:
                lis.append(typ['consulta_dnp']['lrcdnp']['rcdnp']['dt']['locs']['lous']['lourb']['dir']['nv'])
            else:
                lis = ""
        except:
            lis = ""
    else:
        try:
            num = len(typ['consulta_dnp']['bico']['lcons']['cons'])
            options = "a"
        except: 
            num = len(typ['consulta_dnp']['bico']['lspr']['spr'])
            options = "b"      
        finally:
            lis = []
            if num > 1:
                for n in range(0,num,1):
                    if options == "a":
                        try:
                            lis.append(typ['consulta_dnp']['bico']['lcons']['cons'][n]['lcd'])
                        except:
                            lis.append(typ['consulta_dnp']['bico']['lcons']['cons']['lcd'])
                    if options == "b":
                        try:
                            lis.append(typ['consulta_dnp']['bico']['lspr']['spr']['dspr']['dcc'])
                        except: 
                            lis.append(typ['consulta_dnp']['bico']['lspr']['spr'][n]['dspr']['dcc'])
            elif num == 1:
                if options == "a":
                    lis.append(typ['consulta_dnp']['bico']['lcons']['cons']['lcd'])
                if options == "b":
                    lis.append(typ['consulta_dnp']['bico']['lspr']['spr']['dspr']['dcc'])
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


