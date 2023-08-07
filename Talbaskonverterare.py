import string
import math

"""
Carl Viggo Nilsson Gravenhorst-Lövenstierne ProCivitas, NA2b, 16/05/2023 

Detta program kan användas för att: 
1. Konvertera mellan talbaser inom intervallet 2 - 62 
2. Utföra räkneoperationer på tal med olika talbaser inom samma intervall

(Pröva gärna extrema tal, ex: -AxyB78.98hj i talbas 60 till ex talbas 17 eller liknande)
(Pröva gärna att medvetet slå in felaktiga tal, Ex: ABC i bas 10 (finns ej) eller Ex: ABC i bas 100 (finns ej), 
eller Ex: abcdefghijklmnop i talbas 60 --> talbas 2 (blir för långt), för att se felmeddelanden)

Regler: 

#Talbaskonverteraren fungerar för negativa tal och decimaltal. Stora bokstäver (A,B,C,D...) används 
för att representera siffror med värden från 10-35. Små bokstäver (a,b,c,d...) används för att 
representera siffror med värdeen från 36-62. Ex. B --> 11 (tio), b --> 37 (tio) 

#Räkneoperationsalgoritmen fungerar för decimaltal, dock ej för negativa tal. Då användaren förhoppningsvis 
är varse om regler för addition, subtraktion, division och multiplikation begränsar detta inte programmet allt för mycket

#Programmet bygger på att användarens angivna tal först omvandlas till talbas tio (tal --> 10) för att därpå omvandlas till 
önskad talbas (10 --> önskad talbas)

"""

"""
Noteringar till Petter: 

1. Programmet bygger på att talet som ska omvandlas först omvandlas till talbas 10 (DEL1). Talet i talbas 10 returneras av funktionen lower_to_decimal()
Härifrån utförs antingen beräkningar, eller så fortsätter programmet, genom att talet i talbas 10 omvandlas till önskad talbas (DEL2). 

2. Funktionen konvertera() innehåller flera funktioner som tillsammans utför beräkningar. 
Dessa funktioner tillkallas hela tiden nedifrån i en lång "kedja". Den slutgiltiga funktionen add_comma() 
som finns längst ned sammanställer resulatet från ovanstående funktioner. 

3. Moment som kan uppfattas som otydliga är förtydligade med text som denna.  

4. Följande felmeddelanden finns inbyggda: 
    a. Om användaren anger en bas under 2 eller över 62 
    b. Om användaren anger ett tal som ej finns i den angivna talbasen. 
    c. Om längden på det slutgiltiga talet överstiger 55 siffror. 
    d. Om användaren angett , istället för . 
    e. Om resultatet från talbasoperatorn understiger 0.0000000001 
    f. Om användaren anger en bas som är inte är heltal. 
    g. Om användaren anger en annan räkneoperatör än **, *, /, - eller +
    h. Om användaren inte svarar A eller B 

5.  Klassen Above_decimal hanterar de problem som kan uppkomma vid talbasberäkningar. 
"""

"""
Planering: 

Prio --> Få konverteraren att fungera. Därpå kn resulterande funktionalitet läggas till. 
What to do next: 
    # PÅSKLOV Raise exception if the insert number doesn't belong to the base CHECK
    # PÅSKLOV Raise exception if base is higher than 62 or is below 2 CHECK
    # V17 Make the function work for negative numbers CHECK 
    # V19 Make the program add, subtract, multiply and divide CHECK
    # PÅSKLOV Transfer to desired base CHECK 
    # Make "number" a global number and also the length of the number CHECK 
    # V18 Add support for decimals CHECK 
    # Add great comments 
    # Add user experience 
    # V18 Add correct number of decimals CHECK 
"""

#Klassen Above_decimal utgörs av "metoder"/"methods" som hanterar de problem som kan uppkomma vid talbasberäkningar. 
class Above_decimal:
    #Skapar en lista med tuples (x,y) där x motsvarar siffran i den specifika talbasen, medan y är det korresponderande värdet i talbas 10. Ex: (B,11)
    def __init__(self): 
        #Skapar nya symboler för högre talbaser, (små och stora bokstäver.)  
        self.alphabetA = list(string.ascii_uppercase)
        self.alphabetB = list(string.ascii_lowercase)
        self.new_nums = []
 
        #Siffror tillskrivs värden, Ex: (7,7) innebär att 7 har värdet 7 i talbas 10. Tuplen läggs till i listan new_nums
        for k in range(0,10): 
            self.new_nums.append((str(k),k))
        
        #Bokstäver tillskrivs värden, Ex: (B,10). Tuplen läggs till i listan new_nums
        for i in range(len(self.alphabetA)):
            self.new_nums.append((self.alphabetA[i], i+10))
        
        for i in range(len(self.alphabetB)):
            self.new_nums.append((self.alphabetB[i], i+35))

    #ConverterA returnerar det korresponderande värdet i talbas 10 för stora och små bokstäver. 
    #Ex: om letter = B, så hittar algoritmen tuplen (B,7) och returnerar värdet 7
    def converterA(self, letter): 
        for j in range(len(self.new_nums)): 
            if self.new_nums[j][0] == letter: 
                return self.new_nums[j][1]

    #ConverterB gör motsatsen till ConverterA och returnerar den korresponderande bokstaven för ett värde i talbas 10. 
    def converterB(self, number):
        for j in range(len(self.new_nums)): 
            if self.new_nums[j][1] == number: 
                return self.new_nums[j][0]
    
    #Raise_error "raises an error" om den siffran användaren vill omvandla (number) inte finns i inputtalbasen.
    #Ex: Nummret ABC finns ej i talbas 10 --> raises an error
    def raise_error(self, number, inbase): 
        no_comma = number.replace(".", "")
        num_len = len(str(no_comma))
        false_number_lst = []
        false_numbers_str = ""
        #Skapar en lista av de siffror i den siffran användaren vill omvandla(number) som inte finns i den givna basen. 
        #Detta för att ge ett instruktivt meddelande vid "raise exception"
        for i in range(num_len):
            if int(object.converterA(no_comma[i])) > inbase - 1: 
                false_number_lst.append(no_comma[i] + ",")
    
        for i in range(len(false_number_lst)): 
            false_numbers_str += false_number_lst[i]

        for i in range(num_len): 
            #Undersöker om (number) finns i den givna talbasen. 
            #Detta måste gå via converter_A då Ex: A behöver omvandlas till 10 för att undersöka om A finns i den angivna talbasen(inbase). 
            #Ett unikt felmeddelande visas för användaren om nummret ej uppfyller kvalifikationen ovan. 
            check = self.converterA(no_comma[i])
            try: 
                if int(check) > inbase - 1  :
                    raise ValueError
            except ValueError: 
                print("Programmet avslutades då siffrorna {} ej existerar i ".format(false_numbers_str) + "talbas: {}".format(inbase))
                print()
                exit()
    
    #"raises an exception" om inputtalbasen överstiger 62 eller understiger 2
    def raise_error2(self, too_base):
        try: 
            if too_base > 62: 
                raise ValueError
        except ValueError: 
            print("Programmet avslutades då bas {} > 62 (maximum)".format(too_base))
            exit()
        try:
            if too_base < 2:
                raise ValueError
        except ValueError: 
            print("Programmet avslutades då bas {} < 2 (minimum)".format(too_base))
            exit()
    # "raises an exception" om användarens inputtal innehåller kommatecken (fungerar enbart med punkt)
    def raise_error3(self, numberF):
        try: 
            if "," in numberF: 
             raise ValueError
        except ValueError: 
            print()
            print("Ersätt kommatecknet med punkt")
            print()
            exit()
    # "raises an exception" om talet understiger 0.0000000001 
    def raise_error4(self, tal): 
        try: 
            if float(tal) < 0.0000000001: 
                raise ValueError
        except ValueError: 
            print()
            print("Talet blir för litet. Pröva igen")
            print()
            exit()
    # "raises an exception" om räkneoperatorn ej är kompatibel
    def raise_error5(self, operator): 
        kompatibel = ["-", "+", "**", "*", "/"]
        try: 
            if operator not in kompatibel:
                raise ValueError
        except ValueError: 
            print()
            print("Räkneoperatorn {operator} är ej kompatibel. Välj antingen +,-,*,/ eller **".format(operator=operator))
            print()
            exit()
    #Ser till att användarinputen är kompatibel med programmet 
    def raise_error6(self, user_input): 
        ok_input = ["a", "A", "B", "b"]
        if user_input not in ok_input: 
            print()
            print("{svar} är inte ett giltigt svar".format(svar=user_input))
            exit()
            print()

#Klassen Above_decimal initieras 
object = Above_decimal()

#Funktionen konvertera kör programmet 
def konvertera():  
    print()
    print("---------------------------------------------------")
    print()
    #Användaren får välja mellan tabaskonverteraren eller talbasoperatorn
    user_input = input("Konvertera (A) eller utför räkneoperationer (B): ")
    #Tillkallar metoden "raise_error6" i klassen Above_Decimal för att se till att svaret är kompatibelt med programmet 
    object.raise_error6(user_input)
    print()
    print("---------------------------------------------------")
    print()

    #Definierar startvariabler för konverteraren
    if user_input.lower() == "a": 
        inbase = int(input("Talbas att konvertera från: "))
        number = input("Nummer att konvertera     : ")
        too_base = int(input("Talbas att konvertera till: "))
    
    #Definierar startvariebler för talbasoperatorn 
    if user_input.lower() == "b": 
        try: 
            bas1 = int(input("Talbas Nummer 1        : "))
            number1 = input("Nummer 1               : ")
            operator = input("Räkneoperatör (+,-,*,/): ")
            bas2 = int(input("Talbas Nummer 2        : "))
            number2 = input("Nummer 2               : ")
            too_base = int(input("Önskad talbas          : "))
        except ValueError: 
            print()
            print("Ange en talbas som tillhör de positiva heltalen")
            print()
            exit()

    ######### DEL 1: Användarangivet nummer --> talbas 10 

    """
    Funktionen "bases" returnerar en lista, positions, med tuplar (x,y) där x är antal gånger som siffran med basen y förekommer. 
    Ex: Tal: 123 talbas 8 --> lista = [(1,8**2), (2,8**1), (3,8**0)]
    """
    def bases(numberF,inbaseF):   
        
        string = str(numberF)
        commaidx = 0
        positions = []

        #Aningen invecklad algoritm neda, finns säkert en bättre lösning: 
        """
        Om talet (number F) är 1234.5678 så kommer string_left = 1234 & string_right = 5678
        Detta för att hantera problemet med kommatecknet som annars skulle räknas som en plats. String_right och string_left 
        kommer att behandlas både enskilt och tillsammans genom hela programmet. Om numberF inte är ett decimaltal så är enbart string_left relevant och string_right = None
        """
        for i in range(len(string)): 
            if string[i] == ".": 
                commaidx = i
                string_left = string[:commaidx]
                string_right = string[commaidx+1:]
                break
            else: 
                string_left = numberF
                string_right = None     
        
        #Om string_right == None så är numberF (talet som användaren anger) ett heltal --> Går direkt till loopen nedan som hanterar heltal .
        if string_right == None: 
            pass
        else:  
            #Förklaring nedan 
            """
            Här hanteras string_right, dvs, eventuella decimaltal. 
            Ex: string_right = "ABCD" i talbas 16. 
            base_base används för att spara siffrornas värde i positionssystemet, Ex: A i ABCD --> 16 ** 3 osv...
            Samtliga siffror itereras igenom och konverteras till korresponderande värde i talbas 10 genom metoden converterA i klassen Above_decimal
            I slutändan fylls listan positions på med tuplar i enlighet med beskrivningen ovan
            """
            for i in range(len(string_right)): 
                length = str(len(string_right))
                class_input = string_right[len(string_right)-1-i]
                base_base = -1 * (len(string_right) - i)
                occurrence = object.converterA(class_input)
                positions.append((occurrence, inbaseF **  base_base))

        #Denna for-loop tillämpar samma algoritm som ovanstående loop, men på heltalsdelen av användarens inputtal, dvs, string_left, av numberF.  
        for i in range(len(string_left)): 
            class_input = string_left[len(string_left)-1-i]
            occurrence = object.converterA(class_input)
            positions.append((occurrence, inbaseF ** i))
        
        #Ex: numberF = 123.567 talbas 10 --> positions = [(6, 0.001), (5, 0.01), (4, 0.1), (3, 1), (2, 10), (1, 100)]
        #Dvs (Förekomst, bas ** positionsvärde) 
        return positions

    #Funktionen lower_to_decimal använder listan med tuplar (x,y) (positions), för att omvandla inputtalet-
    #till korresponderande tal i talbas 10. 
    def lower_to_decimal(numberF, inbaseF): 
        #Tillkallar metoden raise_error3 i klassen Above_decimal för att eliminera risken att numberF innehåller kommatecken
        object.raise_error3(numberF)
        
        #pairs är listan "positions" med tuplar (x,y) där x är förekomst och y är positionsvärde 
        pairs = bases(numberF, inbaseF)
        #tillkallar metoden raise_error2 i klassen Above_decimal som undersöker om värdet på inputbasen är för högt eller för lågt. 
        object.raise_error2(inbaseF)
        decimal = 0
        no_comma = numberF.replace(".","")
        num_len = len(str(no_comma))
        #tillkallar metoden raise_error i klassen Above_decimal som undersöker om siffrorna i inputnumret existerar i den angivna basen. 
        object.raise_error(numberF,inbaseF)
        """
        Här genereras det korresponderande talet till numberF (inputtalet) i talbas 10.
        Talet är en summa av elementen i listan pairs (positions) med tuplar. 
        Ex: i = (7, 10**2) -->  7 * 10**2 adderas till variebeln decimal.
        """
        for i in range(num_len):
            decimal += pairs[i][0] * pairs[i][1]
        
        #decimal är användarens inputnummer (numberF) omvandlat till talbas 10
        return decimal

    ######### DEL 2: talbas 10 --> Önskad talbas 
    
    """
    Funktionen create_base_list returnerar en lista med korrekt antal bas ** exponent som senare används i funktionen to_new_base
    Ex: 1234 (tio) utgörs av 10**3, 10**2, 10 **1  & 10**0 som förkommer x antal gånger på varje plats.
    """ 
    def create_base_list(Number_in_base_ten, inbaseF):
        #Undersöker om numret i talbas 10 = 0 för att undvika ZeroDivisionError vid division
        if Number_in_base_ten == 0: 
            baselst = []
        else: 
            length = len(str(Number_in_base_ten))
            baselst = []
            
            """
            Följande kodrad: length = int(math.log(Number_in_base_ten) / math.log(too_base)) är mycket viktig. 
            Koden löser ut variebeln "length" i följande ekvation nummer = bas ** length och rundar svaret nedåt till närmaste heltal. 
            Variebeln "length" avgör sedan hur många Ex: 10**3, 10**2, 10 **1, 10**0, 10**-1 osv som ska sparas i baselst. Detta är en förutsättning för att algoritmen 
            i funktionen to_new_base ska fungera.
            """
            
            length = int(math.log(Number_in_base_ten) / math.log(too_base))
            
            #Här skapas de negativa exponenterna i sekvensen (10**-1, 10**-2 osv) i minskande ordning. 10 decimaler --> Max 10 decimalers noggranhet. 
            for i in range(10, 0, -1): 
                baselst.append(inbaseF ** -i)
            
            #Här används variabeln length för att avgöra hur många element: bas ** x som ska läggas till baselst. 
            for i in range(length+1):
                baselst.append(inbaseF ** i)
            
            #Byter från ökande till minskande ordning. 
            baselst.reverse()
        
        #I slutändan kommer baselst exempelvis se ut såhär: [1000, 100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 1e-05, 1e-06, 1e-07, 1e-08, 1e-09, 1e-10]
        return baselst

    #Funktionen to_new_base använder sig av baselst för att omvandla från nummret i talbas 10 till önskad talbas (too_base)
    def to_new_base(Number_in_base_ten, too_base): 
        #tillkallar metoden raise_error2 i klassen Above_decimal som undersöker om värdet på inputbasen är för högt eller för lågt
        object.raise_error2(too_base)
        #tillkallar ovanstående funktion som returnerar en lista med följande struktur: Ex:[1000, 100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 1e-05, 1e-06, 1e-07, 1e-08, 1e-09, 1e-10]
        new_baselst = create_base_list(Number_in_base_ten, too_base)
        baselst_len = len(new_baselst) 
        new_base = []
        counter = Number_in_base_ten
        new_number = ""
        
        """
        De två For-looparna nedan har följande funktioner: 
        1. num_times står för "antal gånger ett element i baselst får plats i nummret i base tio". Elementen i baselst läses av från stort till minskande värde. 
        2. Om ex 1000 går 14 gånger i ett tal, ex E000 bas 15, så behöver 14 konverteras till motsvarande symbol i bas 15 --> E. Därför tillkallas metoden converterB i klassen
        Above_decimal som omvandlar en siffra i talbas 10 till korresponderande symbol i önskad talbas. 
        3. Denna siffra, ex "E" läggs till i en separat lista. 
        4. counter (ursprungligen nummret i talbas 10) minskas med antalet gånger som elementet i baselst fick plats i numret i talbas 10. 
        5. Summerar elementen i listan new_base (siffror i string format)
        """

        for i in range(baselst_len):
            # 1
            num_times = float(counter // new_baselst[i]) 
            # 2
            converted_num_times = object.converterB(num_times) 
            # 3
            new_base.append(str(converted_num_times)) 
            # 4
            counter -= num_times * new_baselst[i] 

        for j in range(len(new_base)): 
            # 5
            new_number += new_base[j]
        
        #new_number är siffran i talbas 10 konverterad till önskad talbas, men!, fortfarande finns eventuella komma eller minustecken med.
        return new_number

    """
    Samtliga ovanstående funktioner tillkallas inom funktionen add_comma, där det slutgiltiga resultatet sammanställs. 
    add_comma har följande uppgifter: 

    - Se till att kommatecknet placeras på rätt plats. Att få till detta rätt var en ganska stor utmaning! 
    - Se till att eventuella minustecken läggs till. 
    - Se till att talet formateras på ett snyggt sätt genom att ta bort onösigt många nollor på slutet av talet
    - Returnerar det slutgiltiga talet i önskad talbas. 
    """

    def add_comma(numberF, inbaseF, too_base): 
    
        #Tillkallar metoden raise_error3 i klassen Above_decimal för att eliminera risken att numberF innehåller kommatecken
        object.raise_error3(numberF)
        #Tillkallar metoden raise_error4 i klassen Above_decimal för att elimnera risken att inbaseF eller too_base inte är ett heltal
        object.raise_error4(inbaseF)
        object.raise_error4(too_base)
        ############

        #Sektionen mellan ########## avlägsnar temporärt eventuella minustecken. 
        global number_original 
        
        number_original = None
        #Sparar det ursprungliga nummret i number_original. Nummret utan minustecken benämns number F. 
        if numberF[0] == "-":
            numberF = str(numberF[1:])
            number_original = numberF

        #############

        #Funktionen lower_to_decimal tillkallas och returnerar användarens inputnummer konverterat till talbas 10 
        decimal = lower_to_decimal(numberF, inbaseF)
        
        #Tar temporärt bort decimaler från decimal 
        rounded_dec = int(decimal)

        #Omvandlar det avrundade talet i talbas 10 till önskad talbas. 
        rounded_to_new_base = to_new_base(rounded_dec, too_base)
        
        #Eftersom det fortfarande inte finns något kommatecken behöver överblivna nollor tas bort (10 st pga 10 siffrors noggrannhet i funktionen create_base_lst)
        rounded_num = rounded_to_new_base.replace("0000000000", "")
        length_rounded = len(str(rounded_num))

        #Omvandlar det egentliga talet i talbas 10 till önskad talbas (kom ihåg, fortfarande inget kommatecken!) 
        no_comma = to_new_base(decimal, too_base)

        """
        Här läggs ett kommatecken till i det slutgiltiga talet. Hur hamnar det på rätt plats? 
        Låt anta att decimal = 1234.5678 --> rounded_dec = 1234 
        Talen ska omvandlas till talbas 12 -->  
        no_comma = 86A.6991A986BA, rounded_num = 86A 
        Kommatecknets plats måste alltså hamna precis efter "86A", dvs, på index len(rounded_num) Därmed final_number = no_comma[:length_rounded] + "." + no_comma[length_rounded:]
        Finns säkert ett bättre sätt att lösa detta på som jag inte insett än! 
        """

        final_number = no_comma[:length_rounded] + "." + no_comma[length_rounded:]

        str_final_number = str(final_number)
        
        #Avlägsnar överflödiga nollor
        str_final_number = str_final_number.rstrip("0")  
        
        #Om "decimal" är ett heltal kommer talet i nuläget se ut på följande vis, Ex: 1234. På innan ovanstående steg (rad 392) --> 1234.0000000000
        #Den överflödiga punkten 1234(.) behöver avlägsnas så länge talet faktiskt inte ska ha ett kommatecken (om float)
        if type(numberF) != float: 
            str_final_number = str_final_number.rstrip(".") 
        
        #number_original är inte None om det ursprungliga talet är negativt. Minustecknet behöver då läggas till. 
        if number_original != None: 
            str_final_number = "-" + str(str_final_number)
        
        ############# 

        #Denna kodrad korrigerar ett misstag som uppkommer vid division då kvoten < 0. (listan baselst blir då tom vilket gör att det slutgiltiga talet blir .0 istället för 0. )
        if rounded_dec == 0: 
            str_final_number = str_final_number.replace(".0","0.")

        ############
        
        #Undersöker om det slutgiltiga talet är längre än 55 siffror, det kan då ej visas i terminalen
        try: 
            if len(str_final_number) > 55: 
                raise ValueError 
        except ValueError: 
            print("Talets längd = {length} siffror,  {length} överstiger maxglängden på 55 siffror".format(length=len(str_final_number)))
            print()
            exit()

        #str_final_number är den slutgiltiga siffran, dvs, användarinput --> talbas 10 --> siffra i önskad talbas
        return str_final_number
    

    #OBS! Funktionerna ovan har fortfarande inte tillkallats än, det första datorn läser efter att ha besvarat frågan A eller B högst upp i programmet är denna rad: 
    #Detta stycke tillkallar konverterarfunktionen och därmed samtliga ovanstående funktioner. 
    if user_input.lower() == "a": 
        print()
        print("---------------------------------------------------")
        print()
        print("\t\t", add_comma(number, inbase, too_base))
        print()
        print("---------------------------------------------------")
        print()
    
    """
    I nedanstående stycke aktiveras räkneoperationsfunktionen 
    Stycket bygger på att användarens inputtal först omvandlas till talbas 10, 
    därpå utförs räkneoperationer, sedan konverteras resultatet till önskad talbas, 
    dvs, input --> talbas 10 --> Räkneoperationer --> Önskad talbas 
    """
    #Räkneoperationsfunktionen tillkallas
    #Detta stycke bygger på att användarens inputtal först omvandlas till talbas 10, därpå utförs räkneoperationer, sedan konverteras resultatet till önskad talbas
    if user_input.lower() == "b":
        #funktionen lower_to_decimal omvandlar ett tal i valfri talbas till talbas 10. decimal_1 & decimal_2 är alltså två tal i talbas 10. 
        decimal_1 = lower_to_decimal(number1, bas1)
        decimal_2 = lower_to_decimal(number2, bas2)
        
        #Metoden raise_error5 i klassen Above_Decimal tillkallas för att säkerställar att räkneoperatorn är kompatibel
        object.raise_error5(operator)
        #operator_result är resultatet efter att räkneoperator tillämpats på de två talen i talbas 10
        if operator == "+": 
            """ 
            Att inse att {:.10f}".format(....) skulle användas tog verkligen en stund... Programmet fungerade bra förutom vid mycket stora tal. 
            Tydligen konverterar Python automatiskt alla tal mindre än 10**-4 eller större än 10**15 till grundpotensform, vilket inte är kompatibelt 
            med algoritmerna ovan. Kodraden ovan ser till att enbart 10 decimaler sparas. 
            """
            operator_result = "{:.10f}".format(decimal_1 + decimal_2)
        elif operator == "-": 
            operator_result = "{:.10f}".format(decimal_1 - decimal_2)
        elif operator == "*": 
            operator_result = "{:.10f}".format(decimal_1 * decimal_2)
        elif operator == "**": 
            try: 
                operator_result = "{:.10f}".format(decimal_1 ** decimal_2)
            #Vid potensberäkningar tenderar talen att bli alldeles för stora
            except OverflowError: 
                print("Talet blir för stort")
                exit()
        #Vid division behövs "exception handling" för att inte orsaka ZeroDivisionError
        elif operator == "/": 
            try:
                operator_result = "{:.10f}".format(decimal_1 / decimal_2)
            except ZeroDivisionError: 
                print("Kan ej dela med 0")

        #Om operator_result understiger 0.0000000001 kommer inget värde att sparas då dess maximala noggrannhet är 10 decimaler.
        #Därmed tillkallas metoden raise_erro4 i klassen Above_Decimal 
        object.raise_error4(operator_result)
        
        print()
        print("----------------------------------------------")
        print() 
        #Eftersom operator_result redan står i talbas 10 kan 10 ställas in som förvald bas/parameter (inbase) för funktionen add_comma. 
        #Operator_result konverteras då till önskad talbas (too_base)
        print("\t\t", add_comma(str(operator_result), 10, too_base))
        print()
        print("----------------------------------------------")
        print()



#Programmet initieras 
konvertera()





    

    



