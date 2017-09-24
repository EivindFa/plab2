#rock, scissor, paper

import random
import matplotlib.pyplot as plt


# *************SUPERKLASSE SPILLER*************
class Spiller():

    #Lagrer info om motstanderne i dictionary
    # {spiller1:[trekk1,trekk2,..], spiller2:[trekk1,..],...}
    spiller_historikk = {}
    mulige_trekk = ["Stein", "Saks", "Papir"]

    def __init__(self, spillernavn):
        self.name = spillernavn
        Spiller.spiller_historikk[self] = []

    #velger aksjon som skal utføres
    def velg_aksjon(self):
        return

    #legger til resultatet i historikken
    # relevant for MestVanlig og Historikk
    def motta_resultat(self, spiller, trekk):
        self.spiller_historikk[spiller].append(trekk)

    def oppgi_navn(self):
        return self.name


# *************SPILLERKLASSE TILFELDIG*************
class Tilfeldig(Spiller):
    def __init__(self, name):
        Spiller.__init__(self, name)

    def velg_aksjon(self, motstander):
        return Aksjon(random.randint(0,2))

    def __str__(self):
        return "Tilfeldig"


# *************SPILLERKLASSE SEKVENSIELL*************
class Sekvensiell(Spiller):
    def __init__(self, name):
        Spiller.__init__(self, name)
        #starter med stein
        self.count = 1

    #velger sekvensielt
    def velg_aksjon(self, motstander):
        aksjon = Aksjon(self.count % 3)
        self.count += 1
        return aksjon

    def __str__(self):
        return "Sekvensiell"

# *************SPILLERKLASSE MEST VANLIG*************
class MestVanlig(Spiller):
    def __init__(self, name):
        Spiller.__init__(self, name)

    # finner mest vanlig trekk gjort av motstander.
    # hvis motstander ikke har gjort trekk, velges random
    def velg_aksjon(self, motstander):
        motstander_historikk = self.spiller_historikk[motstander]
        if (len(motstander_historikk)) == 0:
            return Aksjon(random.randint(0,2))
        stein = motstander_historikk.count(Aksjon(0))
        saks = motstander_historikk.count(Aksjon(1))
        papir = motstander_historikk.count(Aksjon(2))
        list = [stein, saks, papir]
        flest = list.index(max(list))
        return Aksjon((get_superior(flest)))

    def __str__(self):
        return "MestVanlig"


# *************SPILLERKLASSE HISTORIKER*************
class Historiker(Spiller):
    def __init__(self, name, husk):
        Spiller.__init__(self, name)
        self.husk = husk

    def velg_aksjon(self, motstander):
        motstander_historikk = self.spiller_historikk[motstander]
        sub_sekvens = motstander_historikk[-self.husk:]
        flest = [0,0,0] #teller mest vanlige trekk etter subsekvensen
        for i in range(len(motstander_historikk)-1-len(sub_sekvens),0,-1):
            if motstander_historikk[i] == sub_sekvens[-1]:
                # sjekker om det er nok elementer igjen i historikken til å matche subsekvensen
                if i - len(sub_sekvens) < 0:
                    break
                # sjekker om hele subsekvensen er riktig eller ikke
                if motstander_historikk[i - len(sub_sekvens) + 1:i + 1] == sub_sekvens:
                    flest[motstander_historikk[i + 1].get_value()] += 1
                # plusser på én i "flest" etter hva som ble spilt etter subsekvensen
                else:
                    break
        # returnerer det motsatte trekket av det som ble spilt flest ganger etter subsekvensen
        max_spilt = max(flest)
        if max_spilt == 0:
            return Aksjon(random.randint(0,2))
        return Aksjon(get_superior(flest.index(max(flest))))

    def __str__(self):
        return "Historiker(" + str(self.husk) + ")"


# *************SPILLERKLASSE SMART (ikke ferdig)*************
class Smart(Spiller):
    def __init__(self, name):
        Spiller.__init__(self, name)

    def velg_aksjon(self, motstander):
        antall_spilt = len(self.spiller_historikk[motstander])
        if antall_spilt < 1:
            return Aksjon(random.randint(0, 2))

        # sjekker om spilleren spiller sekvensielt
        isSekvensiell = True
        utsettelse = 0
        sekvens_start = False
        for i in range(antall_spilt):
            motstander_trekk = self.spiller_historikk[motstander][i]
            # må ta i betraktning at spilleren ikke nødvendigvis må starte med stein
            if motstander_trekk.get_value() == 0:
                sekvens_start = True
            if not sekvens_start:
                utsettelse += 1
            if sekvens_start:
                if motstander_trekk.get_value() != (i - utsettelse) % 3:
                    isSekvensiell = False
        print(isSekvensiell)
        if isSekvensiell:
            return Aksjon(get_superior((antall_spilt + (3 - utsettelse)) % 3))


        #sjekker om motstander er en MestVanlig-spiller
        flest = self.findFlestSpiltOpptilNå(self)
        if self.spiller_historikk[motstander][-1].get_value() == get_superior(flest):
            ny_flest  = self.findFlest(self)
            return Aksjon(get_superior(get_superior(ny_flest)))

        # ellers spilles det motsatte av det jeg pleier å spille etter en subsekvens på 2
        egen_historikk = self.spiller_historikk[self]
        sub_sekvens = egen_historikk[-2:]
        flest = [0, 0, 0]  # teller mest vanlige trekk etter subsekvensen
        for i in range(antall_spilt - 1 - len(sub_sekvens), 0, -1):
            if egen_historikk[i] == sub_sekvens[-1]:
                # sjekker om det er nok elementer igjen i historikken til å matche subsekvensen
                if i < len(sub_sekvens) < 0:
                    break
                # sjekker om hele subsekvensen er riktig eller ikke
                if egen_historikk[i - len(sub_sekvens) + 1:i + 1] != sub_sekvens:
                    break
                # plusser på én i "flest" etter hva som ble spilt etter subsekvensen
                flest[egen_historikk[i + 1].get_value()] += 1
        # returnerer det motsatte av det motsatte trekket av det som ble spilt flest ganger etter subsekvensen
        max_spilt = max(flest)
        if max_spilt == 0:
            return Aksjon(random.randint(0, 2))
        return Aksjon(get_superior(get_superior(flest.index(max(flest)))))


    def findFlestSpiltOpptilNå(self, spiller):
        stein = self.spiller_historikk[spiller].count(Aksjon(0))
        saks = self.spiller_historikk[spiller].count(Aksjon(1))
        papir = self.spiller_historikk[spiller].count(Aksjon(2))
        list = [stein, saks, papir]
        sist_spilt = self.spiller_historikk[spiller][-1]
        list[sist_spilt.get_value()] -= 1
        flest = list.index(max(list))
        return flest

    def findFlest(self, spiller):
        stein = self.spiller_historikk[spiller].count(Aksjon(0))
        saks = self.spiller_historikk[spiller].count(Aksjon(1))
        papir = self.spiller_historikk[spiller].count(Aksjon(2))
        list = [stein, saks, papir]
        flest = list.index(max(list))
        return flest

    def __str__(self):
        return "Smartspiller"


# *************AKSJON KLASSE*************
class Aksjon:
    def __init__(self, num):
        self.aksjon = num

    # sjekker om "self" sitt trekk og "other" sitt trekk er like
    def __eq__(self, other):
        return other.aksjon == self.aksjon

        # sjekker om "self" sitt trekk vinner over "others" trekk
        # 0: stein, 1: saks, 2: papir
    def __gt__(self, other):
        keyWinsOverValue = {0:1, 1:2, 2:0}
        return keyWinsOverValue[self.aksjon] == other.aksjon


    def get_value(self):
        return self.aksjon

    def __repr__(self):
        return Spiller.mulige_trekk[self.aksjon]

    def __str__(self):
        return Spiller.mulige_trekk[self.aksjon]


# *************ENKELTSPILL KLASSE*************
class Enkeltspill:
    def __init__(self, spiller1, spiller2):
        self.spiller1 = spiller1
        self.spiller2 = spiller2
        self.p1 = 0
        self.p2 = 0
        self.a1 = 0
        self.a2 = 0

    def gjennomfoer_spill(self):
        self.a1 = self.spiller1.velg_aksjon(self.spiller2)
        self.a2 = self.spiller2.velg_aksjon(self.spiller1)
        if self.a1 == self.a2:
            self.p1, self.p2 = 0.5, 0.5
        elif self.a1 > self.a2:
            self.p1, self.p2 = 1, 0
        else:
            self.p1, self.p2 = 0, 1

        self.spiller1.motta_resultat(self.spiller2,self.a2)
        self.spiller2.motta_resultat(self.spiller1, self.a1)

    def is_winner(self):
        if self.p1 == self.p2:
            return "Ingen"
        elif self.p1 > self.p2:
            return self.spiller1.oppgi_navn()
        else:
            return self.spiller2.oppgi_navn()


    def __str__(self):
        return self.spiller1.oppgi_navn() + " valgte " + str(self.a1) + " || " + self.spiller2.oppgi_navn() + \
               " valgte " + str(self.a2) + ".\n--> " + self.is_winner() + " vinner!" + "\n"


# *************MANGESPILL KLASSE*************
class Mangespill:
    def __init__(self, spiller1, spiller2, antall_spill):
        self.s1 = spiller1
        self.s2 = spiller2
        self.antall_spill = antall_spill
        self.totalp1 = 0
        self.totalp2 = 0

    def arranger_enkeltspill(self):
        return Enkeltspill(self.s1, self.s2)

    def arranger_turnering(self):
        poeng_sp1 = []
        x_akse = []
        #begynner turneringen
        for i in range(self.antall_spill):
            spill = self.arranger_enkeltspill()
            spill.gjennomfoer_spill()
            self.totalp1 += spill.p1
            self.totalp2 += spill.p2
            print(str(spill))
            #pyplot
            snitt_poeng = self.totalp1 / (i+1)
            poeng_sp1.append(snitt_poeng)
            x_akse.append(i+1)
        print("-----------------SAMMENLAGT SCORE-------------------------")
        print(self.get_score())
        print("Prosent seire for " + self.s1.oppgi_navn() + "(" + str(self.s1) + ") mot "
              + self.s2.oppgi_navn() + "(" + str(self.s2) + "):\n" + str(self.totalp1*100/self.antall_spill) + "%" )
        print("----------------------------------------------------------")

        #pyplot
        plt.plot(x_akse, poeng_sp1)
        plt.axis([0, self.antall_spill,0,1])
        plt.grid(True)
        plt.xlabel("Antall spill")
        plt.ylabel("Snittpoeng/runde")
        plt.axhline(y = 0.5, linewidth = 0.5, color = 'r').set_linestyle('dashed')
        plt.title("Snittpoeng per runde for " + self.s1.oppgi_navn() + "(" + str(self.s1) + ") mot " + self.s2.oppgi_navn() + "(" + str(self.s2) + ")" )
        plt.show()


    def get_winner(self):
        if self.totalp1 == self.totalp2:
            return "Ingen"
        elif self.totalp1 > self.totalp2:
            return self.s1.oppgi_navn()
        else:
            return self.s2.oppgi_navn()

    def get_score(self):
        return self.s1.oppgi_navn() + ": " + str(self.totalp1) + " poeng | " + self.s2.oppgi_navn() + ": "\
               + str(self.totalp2) + " poeng\n" + str(self.get_winner()) + " vinner!"



# *************HJELPEFUNKSJONER*************

def get_superior(num):
    k = {0:2, 1:0, 2:1}
    return k[num]

def main():
    s1 = MestVanlig("Axel")
    s2 = Sekvensiell("Martin")
    mangespill = Mangespill(s1, s2, 100)
    mangespill.arranger_turnering()

main()


