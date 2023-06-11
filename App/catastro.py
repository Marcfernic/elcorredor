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
            for n in range(0, len(a), 1):
                try:
                    txt = [n+1,a[n],b[n]]
                except:
                    txt = [n+1,a[n],"-"]
                finally:
                    mix.append(txt)
            
        elif len(a)<len(b):
            for n in range(0, len(b), 1):
                try:
                    txt = [n+1,a[n],b[n]]
                except:
                    txt = [n+1,"-",b[n]]
                finally:
                    mix.append(txt)
        else:
            mix = [["-","-", "-"]]

    return mix


def proFloor(floor, ex):
    num = 0
    options = ""
    if ex == "No tenemos acceso a este dato":
        lis = []
    else:
        try:
            a = len(floor['consulta_dnp']['bico']['lcons']['cons'])
            b = len(floor['consulta_dnp']['bico']['lcons'])
            if a < b:
                num = b
            elif a > b:
                num = a
            else:
                num = b
            options = "a"
        except:
            num = len(floor['consulta_dnp']['bico']['lspr'])
            options = "b"
        finally:
            lis = []
            if num > 1:
                for n in range(0,num,1):
                    try:
                        try:
                            lis.append(floor['consulta_dnp']['bico']['lcons']['cons'][n]['dfcons']['stl'])
                        except:
                            lis.append(floor['consulta_dnp']['bico']['lspr']['spr'][n]['dspr']['ssp'])
                    except:
                        try:
                            lis.append(floor['consulta_dnp']['bico']['lcons']['cons']['dfcons']['stl'])
                        except:
                            lis.append(floor['consulta_dnp']['bico']['lspr']['spr']['dspr']['ssp'])
            elif num == 1:
                try:
                    try:
                        lis.append(floor['consulta_dnp']['bico']['lcons']['cons']['dfcons']['stl'])
                    except:
                        lis.append(floor['consulta_dnp']['bico']['lspr']['spr']['dspr']['ssp'])
                except:
                    try:
                        lis.append(floor['consulta_dnp']['bico']['lcons']['cons'][0]['dfcons']['stl'])
                    except:
                        lis.append(floor['consulta_dnp']['bico']['lspr']['spr'][0]['dspr']['ssp'])
            else:                    
                try:
                    a = floor['consulta_dnp']['bico']['bi']['dt']['loine']['cm']
                    b = floor['consulta_dnp']['bico']['bi']['dt']['cmc']
                    c = floor['consulta_dnp']['bico']['bi']['debi']['cpt']
                    float(a)
                    float(b)
                    float(c)
                    print(a+b+c)
                    lis = lis.append(a + b + c)
                except:
                    print("ALGO PASA")
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
        except:
            pass
    else:
        try:
            a = len(typ['consulta_dnp']['bico']['lcons']['cons'])
            b = len(typ['consulta_dnp']['bico']['lcons'])
            if a < b:
                num = b
            elif a > b:
                num = a
            else:
                num = b
            options = "a"
        except: 
            num = len(typ['consulta_dnp']['bico']['lspr'])
            options = "b"      
        finally:
            lis = []
            if num > 1:
                for n in range(0,num,1):
                    try: 
                        try:
                            lis.append(typ['consulta_dnp']['bico']['lcons']['cons'][n]['lcd'])
                        except:
                            lis.append(typ['consulta_dnp']['bico']['lspr']['spr'][n]['dspr']['dcc'])
                    except:
                        try:
                            lis.append(typ['consulta_dnp']['bico']['lcons']['cons']['lcd'])
                        except:
                            lis.append(typ['consulta_dnp']['bico']['lspr']['spr']['dspr']['dcc'])
            elif num == 1:
                try: 
                    try:
                        lis.append(typ['consulta_dnp']['bico']['lcons']['cons'][0]['lcd'])
                    except:
                        lis.append(typ['consulta_dnp']['bico']['lspr']['spr'][0]['dspr']['dcc'])
                except:
                    try:
                        lis.append(typ['consulta_dnp']['bico']['lcons']['cons']['lcd'])
                    except:
                        lis.append(typ['consulta_dnp']['bico']['lspr']['spr']['dspr']['dcc'])
            else:
                if options == "a":
                    try:
                        lis.append(typ['consulta_dnp']['bico']['lcons']['cons']['lcd'])
                    except:
                        lis.append(typ['consulta_dnp']['bico']['lcons']['cons'][0]['lcd'])
                elif options == "b":
                    lis.append(typ['consulta_dnp']['bico']['lspr']['spr']['dspr']['dcc'])

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
    
    try:
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
    except:
        pass

    return c


def extractMun(street):
    a = street
    b = c = d = ""
    
    try:
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
    except:
        pass
    
    return d.lstrip()