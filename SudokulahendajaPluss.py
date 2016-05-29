__author__ = 'Diana'
#Sudokulahendaja, mis lahendab standardseid ja erikujuliste regioonidega sudokusid. Valmis: 04.12.14. Diana Algma

import copy

#Arvutab ruudu numbri rea ja veeru järgi
def annaRuuduNr(rida, veerg):
    if rida<4:
        if veerg<4: return 1
        elif veerg<7: return 2
        else: return 3
    elif rida<7:
        if veerg<4: return 4
        elif veerg<7: return 5
        else: return 6
    else:
        if veerg<4: return 7
        elif veerg<7: return 8
        else: return 9

#Numbri klass, mis esindab sisulselt sudoku ühte numbrit, mille väärtus on number selles kastis või "-", kui kast on
#tühi, asukoht rea, veeru ja ruudu kaudu ning sobivad, mis sisaldab kõiki väärtusi, mis sinna ruutu sobiksid.
class Number():
    def __init__(self, väärtus, rida, veerg, sobivad):
        self.väärtus = väärtus
        self.rida = rida
        self.veerg = veerg
        self.ruut = annaRuuduNr(rida, veerg)
        self.sobivad = sobivad
    def toString(self):
        return self.väärtus, self.rida, self.veerg, self.ruut, self.sobivad

#klass regiooni väljade jaoks
class RegiooniVäli():
    def __init__(self, väärtus, rida, veerg):
        self.väärtus = väärtus
        self.rida = rida
        self.veerg = veerg

#prindib järjendina antud sudoku välja
def prindiSudoku(numbrid):
    for i in range(9):
        for nr in numbrid:
            if nr.rida==i+1:
                if nr.veerg != 9:
                    print(nr.väärtus, end = " ")
                else: print(nr.väärtus)

#loeb antud failist sudoku ja tagastab selle sudoku väljade järjendi ning prindib välja sisestatud Sudoku
def loeSisse(fail):
    s = open(fail)
    numbrid = []
    rnr = 0
    for rida in s:
        vnr = 0
        for väärtus in rida:
            if väärtus not in [" ", "\n"]:
                if väärtus == "-":
                    numbrid.append(Number(väärtus, rnr+1, vnr+1, ["1","2","3","4","5","6","7","8","9"]))
                else:
                    numbrid.append(Number(väärtus, rnr+1, vnr+1, [väärtus]))
                vnr +=1
        rnr+=1
    print("\nSisend: " + fail)
    prindiSudoku(numbrid)
    return numbrid

#loeb regiooni failist väljad ja tagastab väljade järjendi
def loeRegioonid(fail):
    s = open(fail)
    väljad = []
    rnr = 0
    for rida in s:
        vnr = 0
        for väärtus in rida:
            if väärtus not in [" ", "\n"]:
                väljad.append(RegiooniVäli(väärtus, rnr+1, vnr+1))
                vnr +=1
        rnr+=1
    print("Regioonid: " + fail)
    return väljad

#kui tegemist erikujulise sudokuga, siis annab väljadele ruudu väärtuseks õige regiooni. (Koodi sees nimetatakse neid
#regioone siiski ruutudeks
def annaRegiooniRuudud(numbrid, regioonid):
    for number in numbrid:
        for väli in regioonid:
            if number.rida == väli.rida and number.veerg == väli.veerg:
                number.ruut = väli.väärtus

#Kontrollib, et igas reas, veerus ja ruudus pole ühte numbrit rohkem kui üks kord
def kontrolli(numbrid):
    for number in numbrid:
        if len(number.sobivad) == 0:
            return False
    for väärtus in ["1","2","3","4","5","6","7","8","9"]:
        for asukoht in [1,2,3,4,5,6,7,8,9]:
            ruudus = []
            reas = []
            veerus = []
            for nmb in numbrid:
                if nmb.ruut == asukoht:
                    ruudus.append(nmb)
                if nmb.rida == asukoht:
                    reas.append(nmb)
                if nmb.veerg == asukoht:
                    veerus.append(nmb)
            i = 0
            for number in ruudus:
                if number.väärtus == väärtus:
                    i += 1
            if i > 1: return False
    return True

#Sudoku lahendamine
def lahendamine(numbrid):
    lahendatud = False
    seis = "käsil"
    proovitud = 0
    #proovitudEeldused on numbrite ajalugu, millele on antud mittekindel väärtus
    proovitudEeldused = []
    #vanemadSeisud on numbrite järjendite ajalugu, mis salvestatakse iga kord, kui numbrile antakse mittekindel väärtus
    vanemadSeisud = []
    #kontrollib, kas midagi tehti, et vältida üleliigsete mõttetute tsüklite läbimist
    tegimidagi = False
    #meetod, mis eemaldab väljade sobivatest väärtustest mittesobivad ja ainult ühe* sobiva korral omistab väärtuse
    #*kui i > 1, siis hakatakse omistama mittekindlaid väärtusi
    def kontrolliSobivaid(tegimidagi, i = 1):
        seis = "korras"
        for number in numbrid:
            if number.väärtus == "-":
                #eemaldab sobivatest kõik mittesobivad väärtused
                for nr in numbrid:
                    if nr.väärtus != "-":
                        if nr.rida == number.rida or nr.veerg == number.veerg or nr.ruut == number.ruut:
                            if nr.väärtus in number.sobivad and nr.väärtus != number.väärtus:
                                (number.sobivad).remove(nr.väärtus)
                                tegimidagi = True
                #kui vaid üks sobiv, omistab numbrile selle väärtuse:
                if len(number.sobivad) == i:
                    if i > 1:
                        #kuna hakatakse omistama mittekindlat väärtust, salvestatakse antud number ja järjendi
                        #hetkeseis
                        proovitudEeldused.append(number)
                        vanemadSeisud.append(copy.deepcopy(numbrid))
                    number.väärtus = number.sobivad[0]
                    tegimidagi = True
                    if i > 1:
                        #kui tegeleti mittekindla väärtusega, lõpetatakse tsükli läbimine, et mitte omistada mitut
                        #ebakindlat väärtust
                        return (tegimidagi, seis)
                #kui pole sobivaid, tagastab veateate
                elif len(number.sobivad) == 0:
                    seis = "vigane"
        #tagastab, kas tsükli käigus tehti midagi ja mis seisuga tsükkel lõpetas
        return (tegimidagi, seis)

    #meetod, mis üritab leida väärtusi, mis sobivad mingisse ruutu/ritta/veergu ainult ühte kohta
    def otsiVõimalusi(tegimidagi):
        for väärtus in ["1","2","3","4","5","6","7","8","9"]:
            for asukoht in [1,2,3,4,5,6,7,8,9]:
                ruudus = []
                reas = []
                veerus = []
                #grupeerib numbrid rea, veeru ja ruudu järgi
                for nmb in numbrid:
                    if nmb.ruut == asukoht:
                        ruudus.append(nmb)
                    if nmb.rida == asukoht:
                        reas.append(nmb)
                    if nmb.veerg == asukoht:
                        veerus.append(nmb)
                #üritab leida igale väärtusele oma kohta igas ruudus
                leidubruudus = False
                for number in ruudus:
                    if number.väärtus == väärtus:
                        leidubruudus = True
                if not leidubruudus:
                    võimalused = []
                    for number in ruudus:
                        if väärtus in number.sobivad:
                            võimalused.append(number)
                    if len(võimalused) == 1:
                        võimalused[0].väärtus = väärtus
                        võimalused[0].sobivad = [väärtus]
                        tegimidagi = True
                        tegimidagi = kontrolliSobivaid(tegimidagi)[0]

                #üritab leida igale väärtusele oma kohta igas reas
                leidubreas = False
                for number in reas:
                    if number.väärtus == väärtus:
                        leidubreas = True
                if not leidubreas:
                    võimalused = []
                    for number in reas:
                        if väärtus in number.sobivad:
                            võimalused.append(number)
                    if len(võimalused) == 1:
                        võimalused[0].väärtus = väärtus
                        võimalused[0].sobivad = [väärtus]
                        tegimidagi = True
                        tegimidagi = kontrolliSobivaid(tegimidagi)[0]

                #üritab leida igale väärtusele oma kohta igas veerus
                leidubveerus = False
                for number in veerus:
                    if number.väärtus == väärtus:
                        leidubveerus = True
                if not leidubveerus:
                    võimalused = []
                    for number in veerus:
                        if väärtus in number.sobivad:
                            võimalused.append(number)
                    if len(võimalused) == 1:
                        võimalused[0].väärtus = väärtus
                        võimalused[0].sobivad = [väärtus]
                        tegimidagi = True
                        tegimidagi = kontrolliSobivaid(tegimidagi)[0]
        return tegimidagi

    #kui sudoku on alguses juba vigane:
    if not kontrolli(numbrid):
        print("\nSeda sudokut ei saa lahendada.")
        return tegimidagi
    #hakkab reaalselt lahendust otsima, otsib, kuni leiab vastuse või jõuab veani, mida parandada ei anna
    while not lahendatud and seis != "vigane":
        tegimidagi = False
        #kontrollib, üritab algselt ka lahendada
        tegimidagi = kontrolliSobivaid(tegimidagi)[0]
        otsiVõimalusi(tegimidagi)
        #kontrollib, kas äkki on lahendatud
        lahendatud = True
        for number in numbrid:
            if number.väärtus=="-":
                lahendatud = False
        #kui lahendatud ja ei ole vigane, siis prindib lahenduse
        if lahendatud and kontrolli(numbrid):
            seis = "lahendatud"
            print("\nLahendus:")
            prindiSudoku(numbrid)
        #kui vigane, annab veateate ja lõpetab lahendamise
        elif seis == "vigane":
            print("\nSeda sudokut ei saa lahendada.")
        #kui ei teinud viimasel tsükli läbimisel midagi, hakkab proovima (mittekindlaid väärtusi omistama)
        elif not tegimidagi:
            #kui sudoku pole vigane:
            if kontrolli(numbrid):
                i=1
                #kui vaja, et sobivaid oleks rohkem kui 9, siis
                while i < 9:
                    #kui viimati tehti midagi (omistati väärtus või muudeti midagi muud), siis hakatakse otsima jälle
                    #kindlaid väärtusi
                    if tegimidagi:
                        seis = kontrolliSobivaid(tegimidagi)[1]
                        #kui sudoku on muutunud vigaseks, võetakse viimane mittekindel omistamine tagasi, kui saab, kui
                        #ei saa, lõpetatakse otsimine
                        if seis == "vigane" or not kontrolli(numbrid):
                            if len(proovitudEeldused) > 0 and len(vanemadSeisud) > 0:
                                muudetudNumber = proovitudEeldused.pop()
                                numbrid = vanemadSeisud.pop()
                                #numbrilt, mille esimene sobiv väärtus oli tegelikult mittesobiv, võetakse see väärtus
                                #sobivatest ära
                                for number in numbrid:
                                    if number.rida == muudetudNumber.rida and number.veerg == muudetudNumber.veerg:
                                        number.sobivad.remove(number.sobivad[0])
                            else:
                                break
                        tegimidagi = False
                        otsiVõimalusi(tegimidagi)
                    #kui viimati ei saanud midagi teha, siis suurendab i-d ühe võrra, ehk omistab esimese sobiva
                    #väärtuse numbrile, millel on i sobivat
                    else:
                        i += 1
                        (a, b) = kontrolliSobivaid(tegimidagi, i)
                        tegimidagi = a
                        seis = b
                        #kui sudoku on vigane, võetakse jälle viimane mittekindel omistamine tagasi, kui saab, kui
                        #ei saa, lõpetatakse otsimine
                        if seis == "vigane" or not kontrolli(numbrid):
                            if len(proovitudEeldused) > 0 and len(vanemadSeisud) > 0:
                                muudetudNumber = proovitudEeldused.pop()
                                numbrid = vanemadSeisud.pop()
                                tegimidagi = True
                                for number in numbrid:
                                    if number.rida == muudetudNumber.rida and number.veerg == muudetudNumber.veerg:
                                        number.sobivad.remove(number.sobivad[0])
                            else:
                                break
                        otsiVõimalusi(tegimidagi)
                        if tegimidagi:
                            i=1
                #kontrollib, kas sai lahendatud, kui jah, siis väljastab lahenduse
                lahendatud = True
                for number in numbrid:
                    if number.väärtus=="-":
                        lahendatud = False
                if lahendatud and kontrolli(numbrid):
                    seis = "lahendatud"
                    print("\nLahendus:")
                    prindiSudoku(numbrid)
                #kui sudoku jäi vigaseks, siis ei saa seda lahendada, väljastab selle teate
                elif not kontrolli(numbrid):
                    print("\nSeda sudokut ei saa lahendada :(")
                    break
                #kui sudoku sai lahendatud, aga see ei läbi kontrolli ega anna enne veateadet, siis on midagi valesti
                else:
                    print()
                    prindiSudoku(numbrid)
                    print("\nMidagi on valesti.")
                    break
            #kui sudoku on peale algset lahendamist juba vigane
            else:
                print("\nVigane sudoku.")
                break

#Näitelahendused olemasolevate sudokudele
def näitelahendused():
    while True:
        a = input("Kas soovid näha näitelahendusi? (jah/ei) ")
        if a.lower() == "jah":
            try:
                numbrid2 = loeSisse('SudokuSisend.txt')
                lahendamine(numbrid2)
                numbrid = loeSisse('SudokuSisend2.txt')
                lahendamine(numbrid)
                vähene = loeSisse('VäheneSisend.txt')
                lahendamine(vähene)
                tühi = loeSisse('TühiSisend.txt')
                lahendamine(tühi)
                vigane = loeSisse('ViganeSisend.txt')
                lahendamine(vigane)
                eriline = loeSisse('ErilineSisend.txt')
                regioonid = loeRegioonid('Regioonid.txt')
                annaRegiooniRuudud(eriline, regioonid)
                lahendamine(eriline)
            except:
                print("Ei leidnud (rohkem) näidislahendusi.")
            break
        elif a.lower() == 'ei':
            break
        else:
            print("Ma ei saanud aru.")

#Lahendused kasutaja käest küsitud sudokudele:
def lahendused():
    while True:
        tavaline = input("\nKas soovid lahendada tavalist sudokut? (jah/ei) ")
        if tavaline == '':
            return
        #tavalise sudoku lahendamine:
        if tavaline.lower() == 'jah':
            while True:
                try:
                    fail = input("Anna algseisuga tekstifail: ")
                    if  fail == '':
                        return
                    numbrid = loeSisse(fail)
                    lahendamine(numbrid)
                    break
                except:
                    print("Ei suutnud faili lugeda, proovime uuesti.")
        #erikujulise sudoku lahendamine:
        elif tavaline.lower() == 'ei':
            print("Sudoku peab siiski olema 9x9 ruudustikus.")
            while True:
                try:
                    sisendfail = input("Anna algseisuga tekstifail: ")
                    if  sisendfail == '':
                        return
                    regioonifail = input("Anna regioonide kujuga lähtefail: ")
                    if  regioonifail == '':
                        return
                    numbrid = loeSisse(sisendfail)
                    regioonid = loeRegioonid(regioonifail)
                    annaRegiooniRuudud(numbrid, regioonid)
                    lahendamine(numbrid)
                    break
                except:
                    print("Ei suutnud faile lugeda, proovime uuesti.")
        else:
            print("Ma ei saanud aru.")

#alguses pakub näitelahendusi, siis küsib kasutaja käest sudokusid ja lahendab neid.
näitelahendused()
print("\nKui soovid lõpetada, vajuta lihtsalt ENTER.")
lahendused()
