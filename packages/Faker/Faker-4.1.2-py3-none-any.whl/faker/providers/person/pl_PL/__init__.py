from .. import Provider as PersonProvider


def checksum_identity_card_number(characters):
    """
    Calculates and returns a control digit for given list of characters basing on Identity Card Number standards.
    """
    weights_for_check_digit = [7, 3, 1, 0, 7, 3, 1, 7, 3]
    check_digit = 0

    for i in range(3):
        check_digit += weights_for_check_digit[i] * (ord(characters[i]) - 55)

    for i in range(4, 9):
        check_digit += weights_for_check_digit[i] * characters[i]

    check_digit %= 10

    return check_digit


class Provider(PersonProvider):
    formats = (
        '{{first_name}} {{last_name}}',
        '{{first_name}} {{last_name}}',
        '{{first_name}} {{last_name}}',
        '{{first_name}} {{last_name}}',
        '{{first_name}} {{last_name}}',
        '{{prefix_female}} {{first_name_female}} {{last_name_female}}',
        '{{first_name}} {{last_name}}',
        '{{prefix_male}} {{first_name_male}} {{last_name_male}}',
    )

    first_names_male = (
        'Jakub',
        'Jan',
        'Mateusz',
        'Bartek',
        'Kacper',
        'Michał',
        'Szymon',
        'Antoni',
        'Filip',
        'Piotr',
        'Maciej',
        'Aleksander',
        'Franciszek',
        'Mikołaj',
        'Adam',
        'Stanisław',
        'Wiktor',
        'Krzysztof',
        'Wojciech',
        'Igor',
        'Maksymilian',
        'Karol',
        'Dawid',
        'Tomasz',
        'Patryk',
        'Oskar',
        'Paweł',
        'Dominik',
        'Kamil',
        'Oliwier',
        'Ignacy',
        'Marcel',
        'Hubert',
        'Adrian',
        'Łukasz',
        'Sebastian',
        'Julian',
        'Tymon',
        'Krystian',
        'Marcin',
        'Damian',
        'Miłosz',
        'Leon',
        'Alan',
        'Tymoteusz',
        'Kajetan',
        'Grzegorz',
        'Daniel',
        'Rafał',
        'Eryk',
        'Konrad',
        'Ksawery',
        'Gabriel',
        'Nikodem',
        'Bruno',
        'Przemysław',
        'Borys',
        'Artur',
        'Olaf',
        'Jerzy',
        'Marek',
        'Tadeusz',
        'Andrzej',
        'Witold',
        'Iwo',
        'Juliusz',
        'Robert',
        'Błażej',
        'Cezary',
        'Jeremi',
        'Jacek',
        'Konstanty',
        'Ryszard',
        'Stefan',
        'Aleks',
        'Gustaw',
        'Radosław',
        'Emil',
        'Norbert',
        'Fabian',
        'Jędrzej',
        'Alex',
        'Kazimierz',
        'Arkadiusz',
        'Kornel',
        'Józef',
        'Natan',
        'Cyprian',
        'Mieszko',
        'Nataniel',
        'Maks',
        'Maurycy',
        'Olgierd',
        'Dariusz',
        'Leonard',
        'Mariusz',
        'Albert',
        'Fryderyk',
        'Ernest',
        'Tobiasz')

    first_names_female = (
        'Kamila',
        'Ewa',
        'Blanka',
        'Olga',
        'Kalina',
        'Klara',
        'Urszula',
        'Sandra',
        'Kaja',
        'Marianna',
        'Kornelia',
        'Justyna',
        'Monika',
        'Sara',
        'Adrianna',
        'Aniela',
        'Agnieszka',
        'Róża',
        'Marcelina',
        'Roksana',
        'Natasza',
        'Lidia',
        'Malwina',
        'Karina',
        'Ada',
        'Marika',
        'Anastazja',
        'Sonia',
        'Nela',
        'Dorota',
        'Apolonia',
        'Ida',
        'Eliza',
        'Angelika',
        'Anna Maria',
        'Liwia',
        'Ewelina',
        'Julita',
        'Rozalia',
        'Inga',
        'Krystyna',
        'Bianka',
        'Dagmara',
        'Melania',
        'Sylwia',
        'Nicole',
        'Anita',
        'Aurelia',
        'Elżbieta',
        'Janina',
        'Julianna',
        'Tola',
        'Gaja')

    unisex_last_names = (
        'Wandzel', 'Pajda', 'Dzienis', 'Borysewicz', 'Szlaga', 'Krzysiek', 'Iwańczyk', 'Cierpisz',
        'Borczyk', 'Szymula', 'Pietrasiak', 'Minkiewicz', 'Hojka', 'Goral', 'Staś', 'Smoter',
        'Bosek', 'Bitner', 'Kondej', 'Furgał', 'Durlik', 'Kusa', 'Pacewicz', 'Masiak', 'Kucz',
        'Cichowlas', 'Anders', 'Wawszczak', 'Słupek', 'Pych', 'Piszcz', 'Opoka', 'Lorenz',
        'Grochowina', 'Wicha', 'Pawliczek', 'Kus', 'Zysk', 'Sroga', 'Rychel', 'Patora', 'Maciocha',
        'Rozmiarek', 'Pesta', 'Działak', 'Godyń', 'Chmara', 'Jakubaszek', 'Bałazy', 'Rykała',
        'Wika', 'Kotala', 'Fikus', 'Sus', 'Kunc', 'Mateusiak', 'Kusyk', 'Romańczyk', 'Makieła',
        'Lejman', 'Kołaczek', 'Kurzak', 'Bondyra', 'Podkowa', 'Paśnik', 'Oleszko', 'Marcol',
        'Szybiak', 'Ruszczak', 'Zbroja', 'Stosik', 'Gruchot', 'Boś', 'Wożniak', 'Gniewek', 'Buława',
        'Wiatrak', 'Talaśka', 'Patalas', 'Kwoka', 'Krzempek', 'Danilczuk', 'Ważny', 'Sidorczuk',
        'Legutko', 'Kobos', 'Tylek', 'Szkoda', 'Przerwa', 'Linek', 'Galik', 'Dulewicz', 'Drozda',
        'Nowek', 'Matulewicz', 'Karpeta', 'Jurczuk', 'Buśko', 'Słomian', 'Drywa', 'Rybus', 'Langa',
        'Kluczek', 'Orkisz', 'Ziemkiewicz', 'Siara', 'Para', 'Kwasek', 'Januszko', 'Hejduk',
        'Łuszczak', 'Sprawka', 'Kiełek', 'Jop', 'Faryna', 'Zimoń', 'Utrata', 'Mirga', 'Kozaczuk',
        'Wojtyna', 'Rzońca', 'Madejczyk', 'Glapiak', 'Dziadkowiec', 'Ochnio', 'Sieja', 'Malewicz',
        'Bachanek', 'Mirocha', 'Domżał', 'Tworzydło', 'Płaneta', 'Feret', 'Witas', 'Figat', 'Muc',
        'Kuciel', 'Kielan', 'Hałat', 'Tecław', 'Loba', 'Klucznik', 'Bielas', 'Rajczyk', 'Myszak',
        'Muniak', 'Michalczak', 'Kochanowicz', 'Szołtysik', 'Rychert', 'Pyda', 'Janowiak', 'Janiga',
        'Grądziel', 'Wdowczyk', 'Pytlarz', 'Kuzia', 'Dziewa', 'Bernatowicz', 'Ostapiuk', 'Rejniak',
        'Kotlarek', 'Gajownik', 'Brach', 'Tatarek', 'Szyc', 'Masny', 'Drop', 'Saternus',
        'Podsiadła', 'Patyna', 'Kargol', 'Truchan', 'Pietrusiak', 'Kolbusz', 'Kalota', 'Hołubowicz',
        'Andrzejuk', 'Zdziech', 'Szymonik', 'Sych', 'Strojna', 'Seta', 'Orman', 'Hermanowicz',
        'Denkiewicz', 'Bulanda', 'Szwaja', 'Jankowicz', 'Pochopień', 'Kobza', 'Karwot', 'Kałek',
        'Laszuk', 'Aleksiejuk', 'Witaszek', 'Wawryniuk', 'Jacak', 'Bugla', 'Wejman', 'Jaroch',
        'Janiszek', 'Gorzelańczyk', 'Zieja', 'Krochmal', 'Filas', 'Wawrzynowicz', 'Szałas',
        'Machoń', 'Labus', 'Irzyk', 'Gomuła', 'Wesoły', 'Solarek', 'Kośka', 'Myszk', 'Moryc',
        'Lizoń', 'Lesisz', 'Kiełbowicz', 'Serwa', 'Piórek', 'Majdak', 'Bruzda', 'Bakun', 'Subocz',
        'Stypuła', 'Gołek', 'Fik', 'Wołczyk', 'Waniek', 'Parzyszek', 'Oszust', 'Burza', 'Żbik',
        'Misztela', 'Kurant', 'Drygas', 'Łaciak', 'Franczuk', 'Rycerz', 'Żok', 'Zeman', 'Mejer',
        'Kanarek', 'Jędruch', 'Saj', 'Nieroda', 'Juśkiewicz', 'Surdyk', 'Paliga', 'Makaruk',
        'Hamera', 'Łukowicz', 'Barcz', 'Witos', 'Strzelczak', 'Siedlaczek', 'Pakosz', 'Burchardt',
        'Nurek', 'Morys', 'Korbel', 'Kokosza', 'Kijanka', 'Bobak', 'Samson', 'Jarosiewicz',
        'Szelest', 'Stanisławek', 'Perka', 'Ciepłuch', 'Bryja', 'Świątkiewicz', 'Samul', 'Rohde',
        'Prucnal', 'Miszkiewicz', 'Kuropatwa', 'Gajdzik', 'Mućka', 'Misiaszek', 'Fornalik',
        'Wiszowaty', 'Thiel', 'Osiadacz', 'Miśko', 'Mielcarz', 'Drózd', 'Oleksiuk', 'Matyka',
        'Łyczak', 'Cabała', 'Ośka', 'Bereś', 'Armatys', 'Szmajda', 'Młyńczak', 'Kupidura', 'Kijas',
        'Chomiuk', 'Gowin', 'Dybka', 'Bródka', 'Wziątek', 'Ślęczka', 'Koj', 'Drabczyk', 'Buczko',
        'Sawko', 'Kłysz', 'Karpiel', 'Jarczyk', 'Flaga', 'Fiedorczuk', 'Tomalak', 'Nałęcz',
        'Choroś', 'Brańka', 'Rajchel', 'Kiedrowicz', 'Gąbka', 'Fiołek', 'Drozdowicz', 'Stypa',
        'Kawala', 'Mazanek', 'Kwinta', 'Koczy', 'Hyży', 'Grzejszczak', 'Wywiał', 'Sacharczuk',
        'Jaroszuk', 'Golon', 'Chachuła', 'Malarczyk', 'Kawula', 'Bohdanowicz', 'Bartocha', 'Lewko',
        'Igras', 'Damps', 'Tlałka', 'Niechciał', 'Łyskawa', 'Goś', 'Więckiewicz', 'Leśko', 'Konsek',
        'Juszczuk', 'Szczudło', 'Poniedziałek', 'Palus', 'Bodziony', 'Śmieszek', 'Rej', 'Pietryga',
        'Mieszała', 'Malcher', 'Kopij', 'Kaczan', 'Janasik', 'Watras', 'Stojak', 'Strzyż',
        'Siemieniec', 'Kośnik', 'Kasperczak', 'Woszczyna', 'Wiech', 'Stefanik', 'Miara', 'Łodyga',
        'Walo', 'Oleksiewicz', 'Mainka', 'Baka', 'Trybuś', 'Samol', 'Jamroży', 'Gruszczyk',
        'Deluga', 'Trzos', 'Sinkiewicz', 'Lesik', 'Kroczak', 'Klamka', 'Grzelczyk', 'Dycha',
        'Ciesielczyk', 'Armata', 'Wawrzyczek', 'Prokopczyk', 'Hampel', 'Grzech', 'Rzucidło', 'Rawa',
        'Kręcisz', 'Karyś', 'Rodzeń', 'Karalus', 'Mikosz', 'Kazimierczuk', 'Hajda', 'Berg', 'Teper',
        'Słabosz', 'Dziechciarz', 'Dmoch', 'Śleziak', 'Pietrek', 'Martyka', 'Wołk', 'Smętek',
        'Kroll', 'Grab', 'Dziedzina', 'Noszczyk', 'Kazek', 'Jędrusiak', 'Cebo', 'Tokarek', 'Małota',
        'Hanc', 'Uliasz', 'Pysz', 'Piłka', 'Błaszyk', 'Wyrobek', 'Trybus', 'Szlęk', 'Pindor', 'Łuc',
        'Baszak', 'Majak', 'Łój', 'Szczypek', 'Łuczkiewicz', 'Łaszcz', 'Froń', 'Dybaś', 'Budner',
        'Ostasz', 'Siekierka', 'Pilipczuk', 'Kandzia', 'Gieroń', 'Drost', 'Chwała', 'Malesza',
        'Fiedler', 'Suszko', 'Kurnik', 'Bereda', 'Nalewajko', 'Duczmal', 'Sieradzan', 'Pietrasz',
        'Cecot', 'Tomaszkiewicz', 'Rabiej', 'Staniaszek', 'Mikusek', 'Kuryłowicz', 'Herda',
        'Brzykcy', 'Początek', 'Ochal', 'Koral', 'Kaźmierczyk', 'Kandziora', 'Sycz', 'Reich',
        'Lindner', 'Fulara', 'Przybycień', 'Hermann', 'Forysiak', 'Strzępek', 'Sondej', 'Pyć',
        'Piaścik', 'Grygo', 'Wita', 'Szynkiewicz', 'Piesik', 'Nasiadka', 'Murach', 'Kostro',
        'Hinca', 'Engler', 'Tułacz', 'Przewoźny', 'Pizoń', 'Łapacz', 'Hajduga', 'Bulczak', 'Bubel',
        'Smutek', 'Samoraj', 'Plaskota', 'Fraś', 'Becker', 'Baranowicz', 'Trznadel', 'Topa',
        'Stanisławczyk', 'Lato', 'Kołton', 'Uryga', 'Tomaszczyk', 'Szymanik', 'Stochmal',
        'Kiszczak', 'Dylong', 'Chruszcz', 'Byra', 'Friedrich', 'Cyganik', 'Pacocha', 'Jonczyk',
        'Szymańczyk', 'Radko', 'Meler', 'Kuran', 'Koman', 'Błądek', 'Banachowicz', 'Babiuch',
        'Kruszka', 'Fijoł', 'Zatoń', 'Włodarz', 'Trepka', 'Świerszcz', 'Strzała', 'Opioła', 'Kursa',
        'Dyś', 'Broś', 'Tyka', 'Syroka', 'Grys', 'Szczepaniuk', 'Marcińczyk', 'Leks', 'Kubina',
        'Janke', 'Dąbrowicz', 'Hulbój', 'Cieciura', 'Chochół', 'Szpila', 'Samiec', 'Rduch',
        'Nabiałek', 'Margol', 'Kopa', 'Engel', 'Czerepak', 'Rosłon', 'Pusz', 'Matla', 'Wołoch',
        'Pazik', 'Nazimek', 'Kuśka', 'Karczmarz', 'Gajzler', 'Sławik', 'Lalak', 'Grabias', 'Gągała',
        'Chwedoruk', 'Wasil', 'Pachołek', 'Wichłacz', 'Walentynowicz', 'Tylus', 'Kosz', 'Iwanow',
        'Garczarek', 'Dorociak', 'Boguta', 'Betka', 'Widuch', 'Wawrzynek', 'Szymajda', 'Stanaszek',
        'Klama', 'Goj', 'Dzierżak', 'Walasik', 'Skwira', 'Luks', 'Kujawiak', 'Dworczak', 'Tofil',
        'Rurarz', 'Pachla', 'Lenarcik', 'Kusztal', 'Chaber', 'Skała', 'Radzewicz', 'Kramer',
        'Kochel', 'Dukat', 'Naglik', 'Szurek', 'Litwiniuk', 'Halama', 'Grzela', 'Wojaczek',
        'Popielarczyk', 'Krysik', 'Dawidczyk', 'Barteczko', 'Balik', 'Warych', 'Miodek', 'Madera',
        'Leszczyk', 'Kolanek', 'Fijak', 'Furgała', 'Faruga', 'Poleszak', 'Kusek', 'Herok', 'Golda',
        'Rymarz', 'Pociask', 'Kowalak', 'Czupryna', 'Trzcionka', 'Sulik', 'Matulka', 'Herbut',
        'Stosio', 'Kurtyka', 'Ciuk', 'Szczerbiak', 'Snoch', 'Budniak', 'Boruc', 'Tylka', 'Kwak',
        'Garncarz', 'Szuta', 'Miśkowiec', 'Sykut', 'Jarosik', 'Golus', 'Chmielak', 'Abramczuk',
        'Skrobek', 'Patrzałek', 'Linkiewicz', 'Jereczek', 'Jarema', 'Flasza', 'Fiedoruk',
        'Budkiewicz', 'Świgoń', 'Przewoźnik', 'Parada', 'Heller', 'Gierak', 'Ferdyn', 'Sumera',
        'Bik', 'Kamela', 'Ciereszko', 'Świtaj', 'Pastuszko', 'Łobacz', 'Kuba', 'Krzywonos',
        'Granat', 'Szóstak', 'Płoskonka', 'Kumorek', 'Komuda', 'Klinkosz', 'Falba', 'Szczechowicz',
        'Rozum', 'Moroń', 'Matynia', 'Greszta', 'Łuczka', 'Dziewit', 'Mueller', 'Kapral',
        'Hrynkiewicz', 'Gonsior', 'Forma', 'Ciesiółka', 'Bors', 'Siwa', 'Niemczuk', 'Nazar',
        'Liśkiewicz', 'Jarczak', 'Felisiak', 'Fedorczyk', 'Wilusz', 'Pastor', 'Gierek', 'Romaniak',
        'Oleszczak', 'Juras', 'Zachwieja', 'Szmurło', 'Smektała', 'Przewoźna', 'Nikel', 'Chlebek',
        'Balas', 'Latuszek', 'Ambrozik', 'Janczura', 'Aleksandrzak', 'Wojtalik', 'Rok', 'Nagórka',
        'Latoszek', 'Kubowicz', 'Domian', 'Ciemięga', 'Soliwoda', 'Komsta', 'Filus', 'Wierzchoń',
        'Skotarczak', 'Cader', 'Trzmiel', 'Jagieło', 'Wawszczyk', 'Troć', 'Swatek', 'Bączkiewicz',
        'Ulewicz', 'Tutka', 'Pałac', 'Mydlarz', 'Molka', 'Janiuk', 'Guziak', 'Frycz', 'Drzał',
        'Zacharek', 'Wiencek', 'Szłapka', 'Kurach', 'Bareja', 'Pawlukiewicz', 'Moździerz', 'Mich',
        'Lisik', 'Kałwa', 'Dadej', 'Matela', 'Lenda', 'Wolff', 'Wojnicz', 'Sendor', 'Mrózek',
        'Łągiewka', 'Kulisz', 'Kolarz', 'Walus', 'Mikoda', 'Kral', 'Darul', 'Warczak', 'Kunysz',
        'Kidoń', 'Ciuła', 'Chomiak', 'Rzeźniczak', 'Przeniosło', 'Chomik', 'Zimoląg', 'Wojtyś',
        'Mędrala', 'Hennig', 'Handzel', 'Twardzik', 'Śmieja', 'Solarczyk', 'Mendak', 'Lemieszek',
        'Kiryluk', 'Wrześniak', 'Kwarciak', 'Gasik', 'Borysiewicz', 'Sierota', 'Mysiak',
        'Kraszkiewicz', 'Hyjek', 'Polaszek', 'Pazera', 'Kubisz', 'Kościukiewicz', 'Kopczyk',
        'Kliber', 'Kaczmar', 'Kaczka', 'Bicz', 'Augustynek', 'Straszak', 'Sajewicz', 'Glanc',
        'Bzymek', 'Zieniewicz', 'Pagacz', 'Gortat', 'Bubak', 'Warwas', 'Skoneczna', 'Nestorowicz',
        'Dziopa', 'Danisz', 'Bazydło', 'Garncarek', 'Albin', 'Szeszko', 'Naczk', 'Łukowiak',
        'Kopciuch', 'Jakoniuk', 'Węgrzynowicz', 'Walencik', 'Turlej', 'Leonowicz', 'Kierepka',
        'Hendzel', 'Fronczek', 'Zarzeczna', 'Zagrodnik', 'Wałęsa', 'Trzepizur', 'Tereszkiewicz',
        'Szczubełek', 'Magier', 'Działo', 'Drygała', 'Czesak', 'Majorek', 'Wlizło', 'Skutnik',
        'Radke', 'Piątkiewicz', 'Oślizło', 'Kansy', 'Szela', 'Mol', 'Kuświk', 'Karpik', 'Janczarek',
        'Hajdukiewicz', 'Mzyk', 'Kostera', 'Leszkiewicz', 'Hutnik', 'Glaza', 'Fydrych', 'Piegza',
        'Matusewicz', 'Matus', 'Kluczyk', 'Drobnik', 'Połom', 'Okraska', 'Neska', 'Kozłowicz',
        'Wołos', 'Wacławczyk', 'Ochnik', 'Maruszczak', 'Lesner', 'Kuncewicz', 'Kieszek', 'Betlej',
        'Wałdoch', 'Szarejko', 'Smalec', 'Łosiewicz', 'Lisak', 'Walkusz', 'Owsiak', 'Kowaluk',
        'Simon', 'Rup', 'Neubauer', 'Muskała', 'Kucharzyk', 'Gabryel', 'Zimniak', 'Warmuz', 'Opas',
        'Michniak', 'Cieloch', 'Wójcikiewicz', 'Świech', 'Powierża', 'Olko', 'Miękus', 'Kutnik',
        'Kustosz', 'Kochman', 'Trąbka', 'Szyja', 'Młynarz', 'Wojtak', 'Dzierwa', 'Zyguła', 'Taciak',
        'Koziatek', 'Koss', 'Walenciak', 'Twardosz', 'Pakos', 'Mamcarz', 'Burzawa', 'Lenik',
        'Franc', 'Sadza', 'Mądrzak', 'Mak', 'Bobel', 'Szajna', 'Proch', 'Kosela', 'Guźniczak',
        'Radziewicz', 'Olchawa', 'Morcinek', 'Bastek', 'Ragan', 'Podeszwa', 'Mitek', 'Janoszka',
        'Słaba', 'Rusnak', 'Płócienniczak', 'Hanke', 'Gosek', 'Wujek', 'Warchał', 'Starzak',
        'Prochownik', 'Molak', 'Duszkiewicz', 'Sztaba', 'Piwek', 'Nowotnik', 'Kiljan', 'Dubel',
        'Brodowicz', 'Tylec', 'Pik', 'Pastucha', 'Księżak', 'Gumieniak', 'Ufnal', 'Stawinoga',
        'Słoń', 'Kolarczyk', 'John', 'Fleszar', 'Lemke', 'Kurc', 'Kamieniarz', 'Jaskóła', 'Jaremko',
        'Gogacz', 'Dudała', 'Chlipała', 'Szłapa', 'Seidel', 'Kopyt', 'Karłowicz', 'Gębura',
        'Frączkiewicz', 'Frankowicz', 'Dybiec', 'Drobny', 'Brózda', 'Boruń', 'Pelka', 'Macias',
        'Ruszel', 'Pabis', 'Krefta', 'Ćwierz', 'Bieleń', 'Szyca', 'Pronobis', 'Dreszer', 'Bryzek',
        'Ambrożewicz', 'Słobodzian', 'Mrozowicz', 'Wojak', 'Szklarek', 'Paw', 'Kościelak',
        'Kalarus', 'Wylegała', 'Powązka', 'Młot', 'Krekora', 'Bilewicz', 'Pyszka', 'Niedźwiadek',
        'Lubera', 'Chodak', 'Breguła', 'Synak', 'Supeł', 'Suda', 'Roczniak', 'Matuszyk', 'Helak',
        'Gubernat', 'Wojtera', 'Wiszowata', 'Świętoń', 'Deryło', 'Szałaj', 'Rzeszutko', 'Matejczuk',
        'Żołądź', 'Suchta', 'Pokrzywa', 'Piguła', 'Litwińczuk', 'Kik', 'Gula', 'Geisler', 'Micał',
        'Maszota', 'Kurzyna', 'Feliksiak', 'Cybul', 'Wiaderek', 'Śnieg', 'Linka', 'Fidler',
        'Fabiszak', 'Cibor', 'Ryczko', 'Rudolf', 'Jędrzejek', 'Bekus', 'Bek', 'Wolan', 'Radzio',
        'Kuliberda', 'Kolanko', 'Szykuła', 'Skowyra', 'Porwoł', 'Kosiak', 'Kasica', 'Jakiel',
        'Piejko', 'Owczarczak', 'Michnik', 'Linke', 'Kutera', 'Bobryk', 'Szabla', 'Powała',
        'Marciniszyn', 'Gorgol', 'Czerwionka', 'Ledzion', 'Dykas', 'Zygmuntowicz', 'Listwan',
        'Bobrowicz', 'Żurawik', 'Migała', 'Merchel', 'Bogumił', 'Wojsa', 'Sadura', 'Łyjak', 'Giers',
        'Gałat', 'Parafiniuk', 'Kryszkiewicz', 'Wyrostek', 'Wałek', 'Rembisz', 'Paściak', 'Maksym',
        'Kusio', 'Kostek', 'Kalisiak', 'Bździuch', 'Szlufik', 'Pogorzelec', 'Pielech', 'Kafel',
        'Gmur', 'Glazer', 'Borysiuk', 'Białk', 'Adamaszek', 'Wiesiołek', 'Wakuła', 'Rogula',
        'Leszczuk', 'Kapciak', 'Gul', 'Buszka', 'Sklorz', 'Parda', 'Miszkiel', 'Latek', 'Kurzydło',
        'Kucharz', 'Giec', 'Wajdzik', 'Mazik', 'Klimko', 'Kleina', 'Dorawa', 'Perczak', 'Lang',
        'Grunt', 'Cywka', 'Batóg', 'Widłak', 'Miszta', 'Kość', 'Kosidło', 'Aleksander',
        'Marchlewicz', 'Korkosz', 'Beśka', 'Bak', 'Stoch', 'Makles', 'Hudzik', 'Hornik', 'Bujko',
        'Ziętal', 'Zawal', 'Sochaj', 'Podpora', 'Małyszek', 'Maćków', 'Latacz', 'Kozdra', 'Kosno',
        'Gogół', 'Fit', 'Bienia', 'Wendt', 'Szyda', 'Suchoń', 'Sobel', 'Lesiewicz', 'Koleśnik',
        'Kinder', 'Kasper', 'Jaszczyszyn', 'Weremczuk', 'Steinke', 'Sądej', 'Puła', 'Nowrot',
        'Nowotny', 'Majorczyk', 'Kunert', 'Jerzyk', 'Capała', 'Bartoś', 'Wojciech', 'Stelmasiak',
        'Portka', 'Pietrak', 'Łuksza', 'Kulma', 'Jeske', 'Góraj', 'Fyda', 'Siemion', 'Rusiniak',
        'Flisiak', 'Cherek', 'Bryndza', 'Zioła', 'Zapaśnik', 'Raszkiewicz', 'Pszczółka', 'Pałgan',
        'Kozar', 'Gumienny', 'Fedak', 'Erdmann', 'Matura', 'Kapera', 'Golan', 'Szczesiak',
        'Szambelan', 'Półchłopek', 'Łuszczyk', 'Szymocha', 'Pielka', 'Macioł', 'Brudny', 'Babij',
        'Zacharczuk', 'Pilarek', 'Owsianka', 'Harasimiuk', 'Durlak', 'Długajczyk', 'Wijata',
        'Szyndler', 'Morka', 'Mendyka', 'Kubiaczyk', 'Kij', 'Gaudyn', 'Bok', 'Posłuszny', 'Plich',
        'Pacyga', 'Miętus', 'Ficner', 'Świerkosz', 'Krzywoń', 'Kojder', 'Kiepura', 'Godzisz',
        'Ciuba', 'Bukowiec', 'Wlaźlak', 'Teterycz', 'Ścibisz', 'Sobkiewicz', 'Raczkiewicz',
        'Konrad', 'Kohut', 'Gonet', 'Frydel', 'Dyka', 'Siemek', 'Ośko', 'Gospodarek', 'Stryjek',
        'Labudda', 'Kosiec', 'Indyk', 'Franik', 'Fiołka', 'Strycharz', 'Ostapczuk', 'Laszczyk',
        'Lament', 'Korzekwa', 'Kędziorek', 'Dziuban', 'Biegała', 'Witoń', 'Szpara', 'Padło',
        'Otremba', 'Mierzwiak', 'Kordus', 'Bojczuk', 'Szmelter', 'Rudzik', 'Madzia', 'Grabara',
        'Górkiewicz', 'Bartel', 'Śliz', 'Sura', 'Skrzecz', 'Puto', 'Pułka', 'Piotrowiak', 'Mazan',
        'Kobryń', 'Klatka', 'Januchta', 'Grubba', 'Zaucha', 'Sularz', 'Siergiej', 'Pianka',
        'Jędruszczak', 'Groth', 'Sobisz', 'Siejak', 'Rećko', 'Lorens', 'Cegła', 'Wochnik', 'Kuryś',
        'Gregorowicz', 'Filek', 'Salawa', 'Piekarek', 'Pabisiak', 'Glonek', 'Butrym', 'Przewoźniak',
        'Macek', 'Konstanty', 'Kolber', 'Jędrasiak', 'Wężyk', 'Szaj', 'Malara', 'Kłoczko',
        'Karsznia', 'Golenia', 'Zajko', 'Wudarczyk', 'Stanuch', 'Niklewicz', 'Matejczyk', 'Kopyto',
        'Grygorowicz', 'Szajda', 'Stachelek', 'Słyk', 'Loska', 'Job', 'Dziadura', 'Dworniczak',
        'Skubis', 'Obst', 'Kazimierczyk', 'Cymer', 'Ciak', 'Chudoba', 'Achtelik', 'Tytko', 'Skupin',
        'Skierka', 'Panuś', 'Pabiś', 'Folta', 'Bogaczyk', 'Basa', 'Trzpil', 'Morek', 'Kloska',
        'Kapustka', 'Gzyl', 'Gołoś', 'Danel', 'Borkiewicz', 'Araszkiewicz', 'Miotke', 'Rezler',
        'Potyrała', 'Pacholak', 'Herba', 'Grzenia', 'Giezek', 'Gajowiak', 'Filak', 'Fechner',
        'Droździk', 'Cyman', 'Wieczerzak', 'Stróż', 'Staciwa', 'Ruchała', 'Rogal', 'Reszke',
        'Kurpisz', 'Gryga', 'Stempniak', 'Matraszek', 'Kózka', 'Elsner', 'Boba', 'Barłóg',
        'Kiliszek', 'Jessa', 'Ignatiuk', 'Gogola', 'Drobek', 'Lica', 'Larysz', 'Kalka', 'Dziczek',
        'Czupryn', 'Żołna', 'Pytko', 'Misiarz', 'Majnusz', 'Kaszkowiak', 'Jonak', 'Basista',
        'Potęga', 'Natanek', 'Matyszczak', 'Majerczyk', 'Łapaj', 'Korzonek', 'Jaśko', 'Futyma',
        'Duszczyk', 'Antończak', 'Wysota', 'Dela', 'Stawowczyk', 'Milczarczyk', 'Malisz',
        'Andrearczyk', 'Żynda', 'Swaczyna', 'Ryndak', 'Moskalik', 'Mitoraj', 'Łyś', 'Łepek',
        'Knieć', 'Janisz', 'Gorol', 'Ciężka', 'Żyrek', 'Zmarzły', 'Wojtaszczyk', 'Szyguła',
        'Szalast', 'Rząd', 'Nicewicz', 'Danieluk', 'Bulak', 'Wojtasiewicz', 'Pleskot', 'Materek',
        'Kurczak', 'Dytko', 'Świstek', 'Szafarz', 'Litwa', 'Kreczmer', 'Idec', 'Grabczak',
        'Goliszek', 'Flieger', 'Filiks', 'Dyszy', 'Błażejczak', 'Maksimowicz', 'Komisarczyk',
        'Jewuła', 'Hallmann', 'Gabara', 'Budzyń', 'Andruszko', 'Pałyga', 'Moj', 'Koterba', 'Gruza',
        'Gamoń', 'Pasierbek', 'Kuchciak', 'Kanik', 'Cis', 'Zegar', 'Sadlik', 'Paprotny', 'Nalazek',
        'Mikita', 'Kucab', 'Kranc', 'Godzik', 'Sip', 'Powałka', 'Penkala', 'Pachuta', 'Nagel',
        'Litwinowicz', 'Kukuczka', 'Knysak', 'Fojt', 'Brejnak', 'Tasarz', 'Zielke', 'Zaraś',
        'Zaranek', 'Waleczek', 'Rubaj', 'Bazylewicz', 'Banyś', 'Balawender', 'Zmuda', 'Wojcik',
        'Łabno', 'Gęsiarz', 'Frost', 'Bany', 'Żero', 'Rudowicz', 'Nyk', 'Milcarz', 'Lipowicz',
        'Kycia', 'Kościołek', 'Korda', 'Berus', 'Wiese', 'Olkowicz', 'Dzieża', 'Doroszkiewicz',
        'Cetera', 'Pazdan', 'Pacia', 'Kempka', 'Dydak', 'Ścibior', 'Szyjka', 'Pyziak', 'Pleśniak',
        'Maszczyk', 'Ludwiniak', 'Zadora', 'Strug', 'Mokwa', 'Łasak', 'Kulczak', 'Kruszona',
        'Zacharewicz', 'Miękina', 'Klaus', 'Glegoła', 'Wyderka', 'Maleszka', 'Malcherek', 'Lew',
        'Kulis', 'Bodzak', 'Błaziak', 'Bartłomiejczyk', 'Toś', 'Kubasiak', 'Dorobisz', 'Cukier',
        'Ciećko', 'Zapadka', 'Kłosowicz', 'Kasak', 'Czubaszek', 'Baumgart', 'Szemraj', 'Nogieć',
        'Burczak', 'Pietraś', 'Ostafin', 'Noculak', 'Kukieła', 'Fogel', 'Duczek', 'Cylwik',
        'Biernacik', 'Wydrych', 'Szajek', 'Siwczak', 'Majewicz', 'Łosiak', 'Karkut', 'Durys',
        'Chwalisz', 'Bembenek', 'Bartkowicz', 'Piskor', 'Mikus', 'Księżyk', 'Goss', 'Drewniok',
        'Bąkiewicz', 'Wódka', 'Wota', 'Prażmo', 'Kiwior', 'Bogdał', 'Rubacha', 'Hanus', 'Wasiewicz',
        'Trochimiuk', 'Szwiec', 'Suszka', 'Palak', 'Ziemann', 'Maćczak', 'Kruzel', 'Kołaczyk',
        'Kapka', 'Jodko', 'Jeszke', 'Gros', 'Gendek', 'Dubik', 'Ważna', 'Pierchała', 'Nieszporek',
        'Kandora', 'Janasz', 'Gryszkiewicz', 'Drobik', 'Ciołczyk', 'Wołkowicz', 'Tylman', 'Pituła',
        'Pioch', 'Pilich', 'Marach', 'Malon', 'Lepa', 'Kaliciak', 'Joszko', 'Hejna', 'Gryta',
        'Frelich', 'Bełz', 'Bakalarczyk', 'Nóżka', 'Holewa', 'Fierek', 'Żuchowicz', 'Wojtunik',
        'Trzop', 'Masłoń', 'Linda', 'Kurp', 'Gryka', 'Draus', 'Rezmer', 'Mizak', 'Makurat',
        'Kościk', 'Helman', 'Gendera', 'Dydo', 'Bondaruk', 'Bodek', 'Wujec', 'Sady', 'Przekwas',
        'Postawa', 'Polasik', 'Plebanek', 'Lejk', 'Kacperek', 'Gołofit', 'Tomys', 'Świadek',
        'Mizgała', 'Kubrak', 'Ernst', 'Wielgos', 'Martynowicz', 'Drela', 'Ziarnik', 'Stasica',
        'Semik', 'Mytych', 'Melka', 'Marat', 'Dąbrówka', 'Wyroba', 'Siudek', 'Senator',
        'Ryszkiewicz', 'Podsiedlik', 'Małys', 'Lepianka', 'Giersz', 'Zugaj', 'Procek', 'Makosz',
        'Kunda', 'Ziółko', 'Trzyna', 'Stroka', 'Rzeszut', 'Pyza', 'Krężołek', 'Kazior', 'Fidos',
        'Sołek', 'Gordon', 'Dubis', 'Ciochoń', 'Bieszke', 'Żołnierczyk', 'Sobstyl', 'Skalik',
        'Namysło', 'Litewka', 'Krzysztofek', 'Grycz', 'Feluś', 'Downar', 'Szram', 'Oleksik',
        'Milej', 'Kudela', 'Klaja', 'Giedrojć', 'Getka', 'Durma', 'Dudko', 'Dębosz', 'Browarczyk',
        'Sąsiadek', 'Picheta', 'Peciak', 'Niećko', 'Midura', 'Maciejko', 'Gregorek', 'Wąsiewicz',
        'Twardy', 'Szachniewicz', 'Sypek', 'Sojda', 'Saran', 'Mosiołek', 'Guściora', 'Golak',
        'Ellwart', 'Drewicz', 'Barszczak', 'Wójt', 'Strawa', 'Sereda', 'Rejmer', 'Prostak', 'Kołak',
        'Klekot', 'Gerlach', 'Ciepła', 'Barankiewicz', 'Welc', 'Skotarek', 'Sadłocha',
        'Roszkiewicz', 'Połetek', 'Ofiara', 'Kiełbus', 'Kałwak', 'Jas', 'Jarkiewicz', 'Jambor',
        'Hartman', 'Graś', 'Raźniak', 'Janc', 'Doroz', 'Baster', 'Banak', 'Spólnik', 'Poreda',
        'Orwat', 'Matyjas', 'Laskus', 'Bajak', 'Witko', 'Ślimak', 'Sapeta', 'Sadownik', 'Roszko',
        'Nazarewicz', 'Mrotek', 'Gnyp', 'Dziarmaga', 'Zaniewicz', 'Walusiak', 'Toborek', 'Szulim',
        'Pawliczak', 'Nikołajuk', 'Myszor', 'Mila', 'Liedtke', 'Korpal', 'Jaźwiec', 'Groborz',
        'Świerkot', 'Sabała', 'Kluj', 'Żach', 'Wawrzyńczyk', 'Szumiło', 'Sulich', 'Stępak',
        'Rutowicz', 'Krzyszczak', 'Kiełbik', 'Gogol', 'Buszkiewicz', 'Basaj', 'Bartuś', 'Samulak',
        'Ryfa', 'Potoczna', 'Panicz', 'Leśny', 'Lada', 'Kuska', 'Gleba', 'Folga', 'Barczuk',
        'Ślebioda', 'Olma', 'Kuśnierek', 'Krzan', 'Hubert', 'Grzebyk', 'Fras', 'Durlej', 'Pielach',
        'Klin', 'Jędrak', 'Frelek', 'Brząkała', 'Borysiak', 'Zagozda', 'Śliż', 'Szkopek', 'Raźny',
        'Olearczyk', 'Mirończuk', 'Chyb', 'Żybura', 'Żelazo', 'Kunka', 'Kosałka', 'Gosz', 'Dulas',
        'Żelazek', 'Terka', 'Sośniak', 'Pikor', 'Pezda', 'Hadam', 'Groń', 'Fal', 'Chalimoniuk',
        'Karnas', 'Uziębło', 'Grochola', 'Gawliczek', 'Freitag', 'Ćmiel', 'Wacław', 'Symonowicz',
        'Strzoda', 'Sterna', 'Spadło', 'Rajtar', 'Krzykała', 'Holc', 'Gronostaj', 'Barej',
        'Wasilewicz', 'Podgórny', 'Łapot', 'Lepak', 'Hojda', 'Dziuda', 'Klupś', 'Brzeźniak',
        'Bojarczuk', 'Tryka', 'Nalewajek', 'Kudłacik', 'Kubasiewicz', 'Bazyluk', 'Bartoszak',
        'Zbylut', 'Tołoczko', 'Szaruga', 'Obuchowicz', 'Gryska', 'Bociek', 'Wowra', 'Szramka',
        'Spychaj', 'Roj', 'Musiolik', 'Franas', 'Dłubak', 'Cholewka', 'Bobko', 'Białous', 'Osial',
        'Nieborak', 'Minta', 'Kozica', 'Kowara', 'Gwara', 'Tekieli', 'Pancerz', 'Mleczak', 'Celuch',
        'Zapiór', 'Graboś', 'Fidura', 'Cyrek', 'Bracha', 'Gradek', 'Noras', 'Mulawa', 'Moniuszko',
        'Kapcia', 'Gumienna', 'Graj', 'Gilewicz', 'Żółtek', 'Wojtalewicz', 'Szumny', 'Opyrchał',
        'Macha', 'Łuczyk', 'Hus', 'Czak', 'Borzym', 'Wojtczuk', 'Winnik', 'Kuk', 'Kubanek',
        'Dziełak', 'Dudziec', 'Cimoch', 'Ciapa', 'Buchalik', 'Zbróg', 'Węgrzyniak', 'Wawrzkiewicz',
        'Teodorowicz', 'Szkoła', 'Sutor', 'Kapuścik', 'Hajdas', 'Fołta', 'Burkiewicz', 'Aleksa',
        'Wajer', 'Siembab', 'Kozon', 'Wojewódka', 'Wenda', 'Majos', 'Huczek', 'Domoń', 'Zubel',
        'Szymaniuk', 'Salomon', 'Mikiciuk', 'Grodek', 'Wielądek', 'Szymańczak', 'Sommer', 'Saczuk',
        'Pastuszek', 'Mroczko', 'Łokaj', 'Deptuch', 'Wawak', 'Szczepaniec', 'Romejko', 'Rogacz',
        'Poczta', 'Nowotka', 'Jaszcz', 'Jany', 'Hewelt', 'Stachów', 'Smykla', 'Sędek', 'Niemira',
        'Młodzik', 'Łyczek', 'Kleban', 'Fura', 'Fudalej', 'Cyroń', 'Zagożdżon', 'Kenig',
        'Górnisiewicz', 'Wołoszyk', 'Szatanik', 'Sajda', 'Pyrkosz', 'Misiejuk', 'Mikołajewicz',
        'Kołsut', 'Glenc', 'Eckert', 'Dziadowicz', 'Waszczyk', 'Szyba', 'Steckiewicz', 'Kloch',
        'Kabala', 'Zamora', 'Tabiś', 'Sobków', 'Pupek', 'Neugebauer', 'Kołtuniak', 'Galek', 'Stój',
        'Rajda', 'Pruchnik', 'Kuza', 'Karaśkiewicz', 'Judek', 'Jędryczka', 'Grzegorzak', 'Drobniak',
        'Chowaniak', 'Wąsek', 'Smagacz', 'Pędzik', 'Klinger', 'Klęczar', 'Wochna', 'Rejek',
        'Krakowczyk', 'Kobak', 'Kawiak', 'Grosz', 'Czubaj', 'Chorążewicz', 'Zadka', 'Wietecha',
        'Sass', 'Męcik', 'Gustaw', 'Furga', 'Frącz', 'Dawiec', 'Wypchło', 'Tarasek', 'Szmaj',
        'Ornat', 'Huszcza', 'Dudczak', 'Ułanowicz', 'Rubin', 'Pich', 'Makoś', 'Krępa', 'Korek',
        'Jonik', 'Andrejczuk', 'Wiertel', 'Soroko', 'Składanek', 'Mortka', 'Małocha', 'Majsterek',
        'Lemanowicz', 'Lelito', 'Krystkowiak', 'Krasa', 'Kierat', 'Jędraszczyk', 'Handke',
        'Dymarczyk', 'Doruch', 'Beker', 'Peszko', 'Osik', 'Łyp', 'Karmelita', 'Herdzik', 'Brzęk',
        'Białczyk', 'Uss', 'Pitura', 'Łusiak', 'Knapek', 'Gumuła', 'Darłak', 'Znojek', 'Wilkos',
        'Rut', 'Przekop', 'Kręcichwost', 'Korab', 'Józwik', 'Jagiełka', 'Chylak', 'Zbiciak',
        'Wasążnik', 'Tłuczek', 'Syldatk', 'Parkitny', 'Juroszek', 'Wisz', 'Wiciak', 'Palonek',
        'Kusik', 'Kocurek', 'Kacperczyk', 'Bluszcz', 'Wydmuch', 'Wereda', 'Trybała', 'Sito',
        'Pietraszkiewicz', 'Nojek', 'Madziar', 'Kazana', 'Szulczyk', 'Rosołek', 'Roskosz', 'Proć',
        'Mazek', 'Koniecko', 'Horbacz', 'Zastawny', 'Orszulik', 'Mesjasz', 'Margas', 'Koźlak',
        'Dzidek', 'Damek', 'Zinkiewicz', 'Sznura', 'Sapała', 'Piaseczna', 'Osada', 'Koziarz',
        'Korta', 'Kłosiewicz', 'Klyszcz', 'Janoszek', 'Deszcz', 'Okła', 'Matacz', 'Hankiewicz',
        'Front', 'Daraż', 'Czura', 'Bylina', 'Bugiel', 'Anioła', 'Amanowicz', 'Zach', 'Starościak',
        'Kliszcz', 'Hadała', 'Czopik', 'Bytner', 'Wośko', 'Wawrzyn', 'Świt', 'Sanetra', 'Pyszczek',
        'Potaczek', 'Osman', 'Materka', 'Madura', 'Kniaź', 'Gryciuk', 'Fidor', 'Dunal', 'Dobroń',
        'Chlebda', 'Słupik', 'Osica', 'Oleksak', 'Maraszek', 'Kręgiel', 'Kopytko', 'Gomoła',
        'Droździel', 'Szott', 'Szkup', 'Posmyk', 'Młotek', 'Klejna', 'Jałowiec', 'Heinrich',
        'Haraburda', 'Grupa', 'Dziadkiewicz', 'Zaczyk', 'Rapa', 'Łodej', 'Lempart', 'Lamch',
        'Głuszko', 'Cudzich', 'Brojek', 'Ziemak', 'Tusk', 'Kieloch', 'Dziduch', 'Dudkowiak',
        'Czerner', 'Sommerfeld', 'Migoń', 'Macheta', 'Dusik', 'Ćwirko', 'Bilik', 'Sydor', 'Swiątek',
        'Sporek', 'Olesiejuk', 'Kutek', 'Jaszczur', 'Jarmuż', 'Gronkiewicz', 'Witan', 'Staniczek',
        'Rząca', 'Roter', 'Pracz', 'Hnat', 'Cydzik', 'Szatko', 'Styrna', 'Podleśna', 'Oleksa',
        'Nieścior', 'Matyjaszek', 'Łasica', 'Kwapień', 'Koronkiewicz', 'Hołota', 'Elert',
        'Czochara', 'Toczko', 'Święs', 'Słysz', 'Salach', 'Leśna', 'Głownia', 'Galica', 'Cieniuch',
        'Szulist', 'Pedrycz', 'Królczyk', 'Zyzik', 'Zaborek', 'Skałka', 'Sankiewicz', 'Pleban',
        'Martin', 'Lewek', 'Jędrys', 'Guzdek', 'Dumała', 'Wszoła', 'Rębiś', 'Pośnik', 'Porzucek',
        'Hawro', 'Dziób', 'Zwara', 'Wiraszka', 'Romankiewicz', 'Roch', 'Paleń', 'Ogonek', 'Makar',
        'Majdan', 'Kozdrój', 'Kozdroń', 'Jachna', 'Duniec', 'Dułak', 'Wojtanowicz', 'Waloch',
        'Ubysz', 'Stożek', 'Małycha', 'Kmak', 'Hass', 'Frydrychowicz', 'Domka', 'Żugaj', 'Zubowicz',
        'Wyrwał', 'Mordal', 'Kordys', 'Gozdur', 'Gabrych', 'Zbrożek', 'Zbroszczyk', 'Wojtoń',
        'Tórz', 'Torbus', 'Letkiewicz', 'Lampart', 'Superson', 'Sopata', 'Sobiło', 'Sapa', 'Salwin',
        'Pera', 'Organiściak', 'Matwiejczyk', 'Matejuk', 'Mały', 'Krüger', 'Dyszkiewicz', 'Basak',
        'Ankiewicz', 'Adamiuk', 'Sykała', 'Skonieczka', 'Pawełko', 'Nojman', 'Iskierka', 'Zięcik',
        'Trojanek', 'Sadlak', 'Nieradko', 'Behrendt', 'Wojewodzic', 'Polewka', 'Zasępa', 'Szczerek',
        'Szałata', 'Sot', 'Mleczek', 'Kukawka', 'Kaczmarkiewicz', 'Dorobek', 'Burchard', 'Blaut',
        'Witka', 'Sasak', 'Pasiak', 'Panasiewicz', 'Motak', 'Lizurej', 'Kuboń', 'Jędraszek',
        'Dylik', 'Cal', 'Buszko', 'Burnat', 'Wyskiel', 'Winek', 'Wiertelak', 'Wiak', 'Roś',
        'Orzeszek', 'Ochota', 'Mijas', 'Maculewicz', 'Kaja', 'Ciesielka', 'Bejm', 'Szmuc', 'Sygut',
        'Siarkiewicz', 'Ryznar', 'Patoka', 'Miszkurka', 'Kudełka', 'Krzyśko', 'Galon', 'Buczma',
        'Ziegler', 'Uroda', 'Turczyk', 'Tolak', 'Sypuła', 'Sadowy', 'Rasała', 'Kazubek', 'Han',
        'Wasiuk', 'Stempin', 'Stawczyk', 'Prokopiak', 'Pospiech', 'Polakiewicz', 'Olas',
        'Maruszczyk', 'Kapinos', 'Kabza', 'Szwałek', 'Smagała', 'Musiała', 'Miksza', 'Lampa',
        'Kulon', 'Koczara', 'Drynda', 'Szczypiór', 'Pawełkiewicz', 'Myk', 'Kuczak', 'Kołata',
        'Żywica', 'Tondera', 'Szmalec', 'Szczap', 'Sypień', 'Sołtysek', 'Mosur', 'Kościesza',
        'Kosowicz', 'Kolendo', 'Huber', 'Giel', 'Gałęza', 'Dyja', 'Cacko', 'Apanowicz', 'Wandas',
        'Siebert', 'Moneta', 'Ziajka', 'Sieg', 'Paluszak', 'Lichoń', 'Kastelik', 'Gwizdek', 'Drewa',
        'Andrys', 'Zbrzeźniak', 'Wlazły', 'Wittbrodt', 'Niksa', 'Habdas', 'Fryś', 'Doktór', 'Detka',
        'Cieplucha', 'Ciarka', 'Witkowicz', 'Wardzała', 'Stąpór', 'Pniak', 'Pierzak', 'Kryk',
        'Kożuszek', 'Kohnke', 'Kapałka', 'Domino', 'Czuj', 'Boksa', 'Wocial', 'Stuglik', 'Steciuk',
        'Smela', 'Plona', 'Piwowarek', 'Pernak', 'Minkina', 'Klos', 'Halik', 'Dzika', 'Dargacz',
        'Damian', 'Adrian', 'Węgrzynek', 'Tomal', 'Świerad', 'Szkatuła', 'Sajnóg', 'Kudlak',
        'Golczyk', 'Fronczyk', 'Czapiga', 'Błażejak', 'Bejma', 'Bartela', 'Tadeusiak', 'Nędzi',
        'Kurcz', 'Jasionek', 'Heleniak', 'Ziarek', 'Zera', 'Sarniak', 'Różak', 'Ligas', 'Kuzior',
        'Kuder', 'Korzeniak', 'Fac', 'Domowicz', 'Dębniak', 'Cieciora', 'Chaberek', 'Bogusiewicz',
        'Block', 'Wardziak', 'Prawdzik', 'Niebudek', 'Jeszka', 'Szpyrka', 'Szkaradek', 'Starek',
        'Pasich', 'Lademann', 'Jantos', 'Grzelec', 'Zapora', 'Wnuczek', 'Wąsala', 'Pompa', 'Małas',
        'Janka', 'Gałaj', 'Dybał', 'Chromy', 'Szpyt', 'Senger', 'Prygiel', 'Pawela', 'Łakota',
        'Jama', 'Graban', 'Fogt', 'Cebulak', 'Boryczko', 'Bojdo', 'Biesek', 'Arendarczyk',
        'Schubert', 'Namysł', 'Milewczyk', 'Hetmańczyk', 'Dyczko', 'Dankiewicz', 'Czerniec',
        'Staśko', 'Rochowiak', 'Misiuk', 'Markiel', 'Ksel', 'Krzyżostaniak', 'Elwart', 'Delekta',
        'Zębik', 'Siatka', 'Niewiara', 'Miozga', 'Mętel', 'Korgul', 'Karwan', 'Franków', 'Domek',
        'Ciepluch', 'Chojna', 'Surmiak', 'Strama', 'Stein', 'Siewiera', 'Robaszkiewicz', 'Piksa',
        'Kociemba', 'Klyta', 'Gromala', 'Gill', 'Broszkiewicz', 'Zontek', 'Stiller', 'Rosada',
        'Mieloch', 'Kornak', 'Goworek', 'Gadzała', 'Fitas', 'Uzar', 'Siedlarz', 'Rorat', 'Oskroba',
        'Mitera', 'Grygorcewicz', 'Gmurczyk', 'Dylak', 'Zybura', 'Wojtaszak', 'Wisła', 'Wasyluk',
        'Szałkiewicz', 'Krzysztoszek', 'Kościuszko', 'Kasiak', 'Wyrwich', 'Wołoszczuk', 'Śledzik',
        'Smorąg', 'Satora', 'Pochroń', 'Melaniuk', 'Jajko', 'Czajor', 'Bajko', 'Wojsław', 'Szumiec',
        'Nehring', 'Naumiuk', 'Luberda', 'Kęsek', 'Jaśkowiec', 'Foit', 'Fita', 'Fedyk', 'Działa',
        'Cygal', 'Zdancewicz', 'Walocha', 'Toma', 'Soczewka', 'Monkiewicz', 'Majtyka', 'Hynek',
        'Dynia', 'Czuryło', 'Bernatek', 'Apostel', 'Zawiasa', 'Piersa', 'Megger', 'Kukier', 'Jarka',
        'Glazik', 'Dyjas', 'Buś', 'Bona', 'Bandyk', 'Zięciak', 'Krajniak', 'Koperek', 'Kazberuk',
        'Dziewior', 'Chachaj', 'Sołoducha', 'Słomiany', 'Skolik', 'Pęksa', 'Mularz', 'Kosman',
        'Kolonko', 'Januszewicz', 'Gramza', 'Foremniak', 'Fijałek', 'Cierpka', 'Polnik', 'Drwięga',
        'Semenowicz', 'Pieszak', 'Narożna', 'Ładniak', 'Kontny', 'Klemens', 'Jancewicz', 'Fąferek',
        'Bisaga', 'Złotnik', 'Wosiek', 'Supernak', 'Kala', 'Giża', 'Bielat', 'Żyto', 'Rompa',
        'Kurpanik', 'Kołpak', 'Gołas', 'Długozima', 'Bacia', 'Wincenciak', 'Styn', 'Moczko',
        'Langier', 'Szrama', 'Szok', 'Suchenek', 'Pieczarka', 'Parus', 'Machul', 'Latko',
        'Krzyśków', 'Galos', 'Ekert', 'Dawidek', 'Czerkies', 'Bujas', 'Andryszczyk', 'Zuziak',
        'Węgrzyk', 'Stąpor', 'Pinda', 'Muzyk', 'Maligłówka', 'Łukasiuk', 'Kinal', 'Dobosiewicz',
        'Waraksa', 'Szywała', 'Nastały', 'Mordak', 'Ligenza', 'Leszczak', 'Krauz', 'Kopała',
        'Byzdra', 'Bartman', 'Wojtach', 'Wałaszek', 'Szara', 'Hapka', 'Wielgat', 'Węgier', 'Pokusa',
        'Małż', 'Kononowicz', 'Hawrylak', 'Grund', 'Druszcz', 'Dacko', 'Sprycha', 'Pryszcz',
        'Łachut', 'Dobrosz', 'Brygoła', 'Ryguła', 'Posłuszna', 'Mydlak', 'Bernard', 'Woroch',
        'Uliczka', 'Tomaszuk', 'Pastuła', 'Pachnik', 'Kudra', 'Kretek', 'Keler', 'Heczko', 'Beck',
        'Tekiela', 'Plizga', 'Piekacz', 'Ochab', 'Maziarczyk', 'Krzosek', 'Gabryelczyk', 'Stępka',
        'Rajch', 'Owsiany', 'Kossak', 'Kocaj', 'Gierach', 'Buza', 'Berendt', 'Tabak', 'Przewłoka',
        'Nytko', 'Kuban', 'Gebauer', 'Gajcy', 'Franaszek', 'Chwedczuk', 'Bochnak', 'Stachewicz',
        'Sosnówka', 'Słowiak', 'Mądro', 'Malcharek', 'Łukasz', 'Kornek', 'Hanusiak',
        'Furmankiewicz', 'Dzikiewicz', 'Duży', 'Delikat', 'Chojak', 'Zyga', 'Pyrz', 'Pietrusiewicz',
        'Olszyna', 'Olszowa', 'Ograbek', 'Molga', 'Maron', 'Jasica', 'Frymus', 'Buszta', 'Woszczak',
        'Woronko', 'Trawka', 'Rychcik', 'Przystupa', 'Oczko', 'Migda', 'Klebba', 'Jaje', 'Grabas',
        'Bugno', 'Bortkiewicz', 'Wesoła', 'Sudak', 'Puc', 'Przeklasa', 'Kocoł', 'Goik',
        'Błażejewicz', 'Tuzimek', 'Petrus', 'Pawlaczek', 'Pacholczak', 'Maciejewicz', 'Jakóbik',
        'Frania', 'Duszczak', 'Domurad', 'Bednarowicz', 'Thomas', 'Rakus', 'Przybyś', 'Pasiut',
        'Małyszka', 'Kurz', 'Kuczaj', 'Doktor', 'Tadla', 'Praczyk', 'Milka', 'Leszcz', 'Kryza',
        'Kryszczuk', 'Juraszczyk', 'Durczok', 'Boduch', 'Szeja', 'Pryk', 'Pitala', 'Molek',
        'Duchnik', 'Brachaczek', 'Wieja', 'Waloszek', 'Nawrotek', 'Nawój', 'Mironiuk', 'Matyjasek',
        'Łachacz', 'Kubów', 'Kidawa', 'Jaremek', 'Hasiak', 'Gierat', 'Gawłowicz', 'Wichary',
        'Sornat', 'Solich', 'Kurczab', 'Jasnoch', 'Famuła', 'Budrewicz', 'Pawliszyn', 'Kułach',
        'Kuffel', 'Konieczek', 'Koćwin', 'Imiołczyk', 'Dyda', 'Zander', 'Stochel', 'Osojca',
        'Mysior', 'Kuciak', 'Kłósek', 'Buchholz', 'Zegadło', 'Wiewiórka', 'Stochaj', 'Smolka',
        'Piotrak', 'Misior', 'Leoniak', 'Karwala', 'Jasina', 'Cięciwa', 'Ciastek', 'Chadaj',
        'Białach', 'Tabisz', 'Such', 'Sromek', 'Rysz', 'Puch', 'Plak', 'Palej', 'Och', 'Niedbał',
        'Mytnik', 'Morgała', 'Lukas', 'Lisoń', 'Królikiewicz', 'Kamieniak', 'Jachimczyk',
        'Grzywnowicz', 'Frukacz', 'Feliniak', 'Dzienisz', 'Drążyk', 'Żelasko', 'Waloszczyk',
        'Strójwąs', 'Smoczyk', 'Klorek', 'Kajdan', 'Kajak', 'Gral', 'Zawodnik', 'Ulfik',
        'Sobieszczyk', 'Skrobot', 'Ochał', 'Leżoń', 'Krywult', 'Iciek', 'Gasek', 'Czenczek',
        'Budzeń', 'Botor', 'Wikło', 'Tymczyszyn', 'Szpyra', 'Słonka', 'Prasek', 'Majczyna', 'Lula',
        'Jakubiuk', 'Hanzel', 'Głowiak', 'Calik', 'Zagrajek', 'Stefankiewicz', 'Serzysko',
        'Piechna', 'Myga', 'Maślankiewicz', 'Kuziora', 'Korniak', 'Indyka', 'Gałach', 'Gadzina',
        'Cyba', 'Bystrek', 'Bazela', 'Wabik', 'Ragus', 'Pitek', 'Mizia', 'Łaskawiec', 'Holeksa',
        'Hajdasz', 'Fugiel', 'Białasik', 'Woźniczko', 'Wilma', 'Rode', 'Preś', 'Komander', 'Klus',
        'Sarosiek', 'Sadoch', 'Osipowicz', 'Lelonek', 'Korbut', 'Jarmużek', 'Włodyka', 'Józefczak',
        'Jędra', 'Hamerla', 'Gęgotek', 'Domińczak', 'Wypiór', 'Sudnik', 'Słoboda', 'Pela', 'Kupś',
        'Kostorz', 'Kosak', 'Kopyść', 'Jarmuła', 'Daniec', 'Blank', 'Balcewicz', 'Starostka',
        'Siemieńczuk', 'Reiter', 'Mycek', 'Miętka', 'Łupina', 'Lipok', 'Knych', 'Drobisz', 'Cuch',
        'Wojtarowicz', 'Wojniak', 'Piechura', 'Meissner', 'Lemiesz', 'Klęk', 'Jargieło', 'Jamroz',
        'Huczko', 'Ceynowa', 'Trochim', 'Kremer', 'Janic', 'Gal', 'Cyrulik', 'Bejger', 'Bawoł',
        'Szczepan', 'Plewnia', 'Pędrak', 'Niedośpiał', 'Maras', 'Klepka', 'Kawulok', 'Katana',
        'Bronka', 'Bender', 'Bałdys', 'Wawrzonek', 'Taranek', 'Tadych', 'Szymała', 'Stebel', 'Skup',
        'Skubała', 'Pasieczna', 'Karkocha', 'Hak', 'Gąszczak', 'Pyś', 'Prażuch', 'Politowicz',
        'Piestrzeniewicz', 'Pajek', 'Nitek', 'Kozok', 'Kowala', 'Kalinka', 'Galuba', 'Buk', 'Breś',
        'Bodych', 'Bittner', 'Bakiera', 'Rembacz', 'Podgórna', 'Myrcik', 'Mojsa', 'Karpiak',
        'Kajdas', 'Gregorczuk', 'Dziurla', 'Dzienniak', 'Dyrek', 'Żołądkiewicz', 'Szumacher',
        'Sado', 'Pyszny', 'Narożny', 'Kuszyk', 'Jakimiak', 'Dynak', 'Dejneka', 'Wiekiera',
        'Tatarczuk', 'Rudyk', 'Nieścioruk', 'Laszkiewicz', 'Gołota', 'Golisz', 'Bąbel', 'Taczała',
        'Świć', 'Siciarz', 'Ropiak', 'Pacura', 'Makulec', 'Krauza', 'Grzesiek', 'Gemza', 'Dering',
        'Banek', 'Andziak', 'Wiza', 'Trojanowicz', 'Parkitna', 'Pacholik', 'Majtczak', 'Krenc',
        'Koniec', 'Wawrzeńczyk', 'Stupak', 'Roda', 'Maciejczuk', 'Irla', 'Husak', 'Fuławka',
        'Fabiańczyk', 'Bryda', 'Zackiewicz', 'Szoka', 'Melcer', 'Kempny', 'Dulemba', 'Duc',
        'Ziniewicz', 'Truchel', 'Szajner', 'Petryk', 'Peda', 'Obarzanek', 'Maszkiewicz', 'Łabaj',
        'Cymbała', 'Biesaga', 'Zdobylak', 'Wojtiuk', 'Ulrych', 'Szymków', 'Sporysz', 'Smardz',
        'Mandrysz', 'Kulus', 'Duras', 'Dumin', 'Borejko', 'Wyłupek', 'Ufniarz', 'Stypka',
        'Młyńczyk', 'Miros', 'Maciuk', 'Hrabia', 'Burzec', 'Buksa', 'Wygoda', 'Tomzik', 'Pindral',
        'Nijak', 'Mszyca', 'Maciejuk', 'Kudłacz', 'Dziwak', 'Chaba', 'Borkowicz', 'Berek',
        'Żakiewicz', 'Wykręt', 'Sztuba', 'Smykała', 'Pyc', 'Pęciak', 'Parzonka', 'Kyc', 'Klemczak',
        'Gąsienica', 'Gabryszak', 'Częścik', 'Cisoń', 'Zmyślony', 'Komisarek', 'Ficoń', 'Citko',
        'Bidas', 'Bas', 'Żabierek', 'Wyciszkiewicz', 'Tarach', 'Staniewicz', 'Reichel',
        'Panasewicz', 'Kucewicz', 'Kilar', 'Hein', 'Fronia', 'Derek', 'Bruś', 'Antoń', 'Pawlos',
        'Ochwat', 'Kurbiel', 'Gosik', 'Gierasimiuk', 'Doroba', 'Chłąd', 'Wrochna', 'Protasiuk',
        'Opalach', 'Mućko', 'Martyn', 'Drgas', 'Ceran', 'Bryczek', 'Ziarno', 'Wołodźko', 'Wac',
        'Szpala', 'Szlachcic', 'Rurka', 'Oczkowicz', 'Mik', 'Małysiak', 'Kubek', 'Imiela', 'Graboń',
        'Garbacik', 'Dolega', 'Broncel', 'Baum', 'Bancerz', 'Siedlik', 'Miąsko', 'Lenc', 'Konat',
        'Kaletka', 'Jenek', 'Honkisz', 'Droś', 'Suchojad', 'Ratka', 'Raba', 'Lulek', 'Komperda',
        'Kołodziejak', 'Koloch', 'Kolka', 'Joniak', 'Jezior', 'Faltyn', 'Dyjach', 'Czulak', 'Cop',
        'Wyroślak', 'Woda', 'Stranc', 'Solis', 'Skomra', 'Sierpień', 'Rzeźniczek', 'Pajdak',
        'Mostek', 'Machowiak', 'Janduła', 'Fitrzyk', 'Welenc', 'Tyczka', 'Skiepko', 'Potok',
        'Olewniczak', 'Nitkiewicz', 'Myrcha', 'Krata', 'Kara', 'Hołysz', 'Hałka', 'Florian',
        'Dziurdzia', 'Dryka', 'Sysło', 'Rolek', 'Młocek', 'Idzi', 'Haponiuk', 'Grębowiec', 'Gęca',
        'Bochnia', 'Ślipek', 'Sieczko', 'Pierz', 'Nyc', 'Łacina', 'Ludwisiak', 'Kujda', 'Hutyra',
        'Dziugieł', 'Białka', 'Zemanek', 'Zawartka', 'Smyl', 'Smolec', 'Słoka', 'Putek',
        'Pietrewicz', 'Lepka', 'Krzeszowiec', 'Kowalówka', 'Jośko', 'Hamrol', 'Gapys', 'Antoszczyk',
        'Turoń', 'Teter', 'Surdel', 'Pieczyrak', 'Mudlaff', 'Manista', 'Kolek', 'Kadela', 'Jeka',
        'Jamrożek', 'Goliasz', 'Dywan', 'Drewnik', 'Dąbroś', 'Ciaś', 'Obiała', 'Nocek', 'Marko',
        'Ładziak', 'Hadaś', 'Dulik', 'Dorynek', 'Wolańczyk', 'Stoltmann', 'Rozumek', 'Łudzik',
        'Łaś', 'Leoniuk', 'Krzyk', 'Karol', 'Kamyszek', 'Filusz', 'Czermak', 'Budych', 'Żółkiewicz',
        'Tatarczyk', 'Pietrus', 'Pachowicz', 'Niesporek', 'Kultys', 'Kornet', 'Kajstura',
        'Grześków', 'Dub', 'Drobot', 'Urynowicz', 'Swacha', 'Prokopczuk', 'Michnowicz', 'Malka',
        'Labocha', 'Capiga', 'Zawalich', 'Wizner', 'Startek', 'Smolorz', 'Rozynek', 'Pal',
        'Madajczyk', 'Ławniczek', 'Haremza', 'Bejnarowicz', 'Żuberek', 'Windak', 'Sobolak',
        'Sibiga', 'Rajczak', 'Pudełek', 'Michalkiewicz', 'Fularczyk', 'Broniarek', 'Żabka',
        'Towarek', 'Sugier', 'Pikula', 'Pawlonka', 'Marosz', 'Kut', 'Grymuza', 'Dąbkiewicz',
        'Ciechowicz', 'Brodawka', 'Borzych', 'Bela', 'Zaguła', 'Tyniec', 'Trepczyk', 'Stwora',
        'Paczos', 'Olbrych', 'Ogrodowicz', 'Michel', 'Mazepa', 'Lazarek', 'Krzystek', 'Jażdżyk',
        'Goska', 'Fraszczyk', 'Drożdżal', 'Cofała', 'Chołody', 'Wawrzyk', 'Prokurat', 'Policht',
        'Płodzień', 'Pasztaleniec', 'Osipiuk', 'Mateńko', 'Kiciak', 'Grotek', 'Członka', 'Żal',
        'Zimmer', 'Wosiak', 'Srokosz', 'Paździora', 'Patoła', 'Pałęga', 'Orawiec', 'Nastaj',
        'Mirgos', 'Merda', 'Machniak', 'Łokietek', 'Fogiel', 'Elias', 'Świergiel', 'Stempel',
        'Skocz', 'Potoczek', 'Penar', 'Miecznik', 'Kwapis', 'Jakóbiak', 'Gietka', 'Flisek',
        'Dudzicz', 'Cich', 'Broniek', 'Wiercigroch', 'Usarek', 'Tryc', 'Szylar', 'Szczot', 'Ptok',
        'Prystupa', 'Preuss', 'Piekara', 'Łaszczyk', 'Kurzaj', 'Kopiczko', 'Jachimczak', 'Hirsch',
        'Dytrych', 'Dorna', 'Bystroń', 'Worach', 'Tokaj', 'Szmagaj', 'Solnica', 'Rejmak', 'Reimann',
        'Pazoła', 'Nieradzik', 'Miechowicz', 'Langiewicz', 'Kruś', 'Kozień', 'Kielczyk', 'Jargiło',
        'Dąbal', 'Cichos', 'Sorbian', 'Ruman', 'Piotrkowicz', 'Oziębło', 'Henke', 'Czosnyka',
        'Choina', 'Chabior', 'Warzybok', 'Seweryniak', 'Pyzel', 'Niewola', 'Nesterowicz', 'Liss',
        'Kiepas', 'Kalista', 'Demiańczuk', 'Cłapa', 'Błasik', 'Berdzik', 'Bełza', 'Złotek',
        'Tonder', 'Szwaj', 'Szarzec', 'Suchora', 'Sarota', 'Palica', 'Matula', 'Malecha', 'Magryta',
        'Łuckiewicz', 'Kuster', 'Stoltman', 'Siewert', 'Serwach', 'Schwarz', 'Kuźnia', 'Kuśmider',
        'Kurzac', 'Klisz', 'Gwardiak', 'Gotfryd', 'Deneka', 'Ciuruś', 'Żmija', 'Tałaj', 'Sobuś',
        'Rajman', 'Perlik', 'Kurda', 'Kosznik', 'Kaluga', 'Jaracz', 'Hanas', 'Dzwonnik', 'Ziegert',
        'Szyma', 'Różewicz', 'Paszkowiak', 'Maślach', 'Lewicz', 'Heba', 'Godzwon', 'Drej', 'Borak',
        'Adamów', 'Tywoniuk', 'Ścieszka', 'Smal', 'Łabuś', 'Kominiak', 'Dietrich', 'Cąkała',
        'Budzich', 'Bąbol', 'Zgoła', 'Sładek', 'Sierżant', 'Misiurek', 'Miąsik', 'Mądrzyk',
        'Kretowicz', 'Kasznia', 'Jeżyna', 'Humeniuk', 'Fiutak', 'Czerniakiewicz', 'Bork', 'Żymełka',
        'Tomalik', 'Szarpak', 'Sołtan', 'Maciuszek', 'Krysta', 'Grzeszkowiak', 'Brachman', 'Zys',
        'Westfal', 'Waluk', 'Wacławiak', 'Sałuda', 'Sabak', 'Niedojadło', 'Nazarko', 'Murat',
        'Majzner', 'Ludwin', 'Kubaczyk', 'Kielich', 'Doliwa', 'Dej', 'Chuchla', 'Boguś', 'Bobik',
        'Zadworny', 'Wójs', 'Tyma', 'Sztuczka', 'Strządała', 'Sowała', 'Omiotek', 'Oleśkiewicz',
        'Morawiak', 'Kwapisiewicz', 'Krokosz', 'Hajder', 'Garczyk', 'Burdach', 'Związek', 'Wojczuk',
        'Stanclik', 'Piekart', 'Mielke', 'Machowicz', 'Kozieja', 'Kaziród', 'Gaś', 'Garbaciak',
        'Chatys', 'Bzdęga', 'Bartoszczyk', 'Zdonek', 'Więcławek', 'Wielgo', 'Steuer', 'Staręga',
        'Sakwa', 'Orpel', 'Kobel', 'Golonko', 'Stark', 'Soczówka', 'Nickel', 'Kupaj', 'Kolman',
        'Kieca', 'Kamyk', 'Jeżyk', 'Glica', 'Gasz', 'Gamrat', 'Franiak', 'Bacik', 'Andrukiewicz',
        'Troka', 'Siwka', 'Odrzywołek', 'Nurkiewicz', 'Kozubal', 'Kott', 'Głowienka', 'Doroszuk',
        'Cogiel', 'Cheba', 'Baś', 'Andreasik', 'Wenzel', 'Szumna', 'Rosłoń', 'Ogłaza',
        'Mikłaszewicz', 'Kubieniec', 'Jędral', 'Bieniak', 'Wons', 'Władyka', 'Rolak', 'Prejs',
        'Płocharczyk', 'Ostręga', 'Łęgowik', 'Ludwik', 'Kopik', 'Kleinschmidt', 'Karczmarek',
        'Gładka', 'Czylok', 'Wawrzynkiewicz',
    )
    male_last_names = (
        'Kowalski', 'Wiśniewski', 'Dąbrowski', 'Lewandowski', 'Wójcik', 'Kamiński', 'Kowalczyk',
        'Zieliński', 'Szymański', 'Woźniak', 'Kozłowski', 'Jankowski', 'Wojciechowski',
        'Kwiatkowski', 'Kaczmarek', 'Mazur', 'Krawczyk', 'Piotrowski', 'Grabowski', 'Nowakowski',
        'Pawłowski', 'Michalski', 'Nowicki', 'Adamczyk', 'Dudek', 'Zając', 'Wieczorek', 'Jabłoński',
        'Król', 'Majewski', 'Olszewski', 'Jaworski', 'Wróbel', 'Malinowski', 'Pawlak', 'Witkowski',
        'Walczak', 'Stępień', 'Górski', 'Rutkowski', 'Michalak', 'Sikora', 'Ostrowski', 'Baran',
        'Duda', 'Szewczyk', 'Tomaszewski', 'Pietrzak', 'Marciniak', 'Wróblewski', 'Zalewski',
        'Jakubowski', 'Jasiński', 'Zawadzki', 'Sadowski', 'Bąk', 'Chmielewski', 'Włodarczyk',
        'Borkowski', 'Czarnecki', 'Sawicki', 'Sokołowski', 'Urbański', 'Kubiak', 'Maciejewski',
        'Szczepański', 'Kucharski', 'Wilk', 'Kalinowski', 'Lis', 'Mazurek', 'Wysocki', 'Adamski',
        'Kaźmierczak', 'Wasilewski', 'Sobczak', 'Czerwiński', 'Andrzejewski', 'Cieślak', 'Głowacki',
        'Zakrzewski', 'Kołodziej', 'Sikorski', 'Krajewski', 'Gajewski', 'Szymczak', 'Szulc',
        'Baranowski', 'Laskowski', 'Brzeziński', 'Makowski', 'Ziółkowski', 'Przybylski', 'Domański',
        'Nowacki', 'Borowski', 'Błaszczyk', 'Chojnacki', 'Ciesielski', 'Mróz', 'Szczepaniak',
        'Wesołowski', 'Górecki', 'Krupa', 'Kaczmarczyk', 'Leszczyński', 'Lipiński', 'Kowalewski',
        'Urbaniak', 'Kozak', 'Kania', 'Mikołajczyk', 'Czajkowski', 'Mucha', 'Tomczak', 'Kozioł',
        'Markowski', 'Kowalik', 'Nawrocki', 'Brzozowski', 'Janik', 'Musiał', 'Wawrzyniak',
        'Markiewicz', 'Orłowski', 'Tomczyk', 'Jarosz', 'Kołodziejczyk', 'Kurek', 'Kopeć', 'Żak',
        'Wolski', 'Łuczak', 'Dziedzic', 'Kot', 'Stasiak', 'Stankiewicz', 'Piątek', 'Jóźwiak',
        'Urban', 'Dobrowolski', 'Pawlik', 'Kruk', 'Domagała', 'Piasecki', 'Wierzbicki', 'Karpiński',
        'Jastrzębski', 'Polak', 'Zięba', 'Janicki', 'Wójtowicz', 'Stefański', 'Sosnowski',
        'Bednarek', 'Majchrzak', 'Bielecki', 'Małecki', 'Maj', 'Sowa', 'Milewski', 'Gajda',
        'Klimek', 'Olejniczak', 'Ratajczak', 'Romanowski', 'Matuszewski', 'Śliwiński', 'Madej',
        'Kasprzak', 'Wilczyński', 'Grzelak', 'Socha', 'Czajka', 'Marek', 'Kowal', 'Bednarczyk',
        'Skiba', 'Wrona', 'Owczarek', 'Marcinkowski', 'Matusiak', 'Orzechowski', 'Sobolewski',
        'Kędzierski', 'Kurowski', 'Rogowski', 'Olejnik', 'Dębski', 'Barański', 'Skowroński',
        'Mazurkiewicz', 'Pająk', 'Czech', 'Janiszewski', 'Bednarski', 'Łukasik', 'Chrzanowski',
        'Bukowski', 'Leśniak',
    )

    prefixes_male = ('pan',)
    prefixes_female = ('pani',)

    first_names = first_names_male + first_names_female

    def last_name(self):
        return self.random_element(self.unisex_last_names)

    def identity_card_number(self):
        """
        Returns 9 character Polish Identity Card Number,
        Polish: Numer Dowodu Osobistego.

        The card number consists of 3 letters followed by 6 digits (for example, ABA300000),
        of which the first digit (at position 3) is the check digit.

        https://en.wikipedia.org/wiki/Polish_identity_card
        """
        identity = []

        for _ in range(3):
            identity.append(self.random_letter().upper())

        # it will be overwritten by a checksum
        identity.append(0)

        for _ in range(5):
            identity.append(self.random_digit())

        identity[3] = checksum_identity_card_number(identity)

        return ''.join(str(character) for character in identity)

    @staticmethod
    def pesel_compute_check_digit(pesel):
        checksum_values = [9, 7, 3, 1, 9, 7, 3, 1, 9, 7]
        return sum(int(a) * b for a, b in zip(pesel, checksum_values)) % 10

    def pesel(self, date_of_birth=None, sex=None):
        """
        Returns 11 characters of Universal Electronic System for Registration of the Population.
        Polish: Powszechny Elektroniczny System Ewidencji Ludności.

        PESEL has 11 digits which identifies just one person.
        pesel_date: if person was born in 1900-2000, december is 12. If person was born > 2000, we have to add 20 to
        month, so december is 32.
        pesel_sex: last digit identifies person's sex. Even for females, odd for males.

        https://en.wikipedia.org/wiki/PESEL
        """
        if date_of_birth is None:
            date_of_birth = self.generator.date_of_birth()

        pesel_date = '{year}{month:02d}{day:02d}'.format(
            year=date_of_birth.year, day=date_of_birth.day,
            month=date_of_birth.month if date_of_birth.year < 2000 else date_of_birth.month + 20)
        pesel_date = pesel_date[2:]

        pesel_core = ''.join(map(str, (self.random_digit() for _ in range(3))))
        pesel_sex = self.random_digit()

        if (sex == 'M' and pesel_sex % 2 == 0) or (sex == 'F' and pesel_sex % 2 == 1):
            pesel_sex = (pesel_sex + 1) % 10

        pesel = '{date}{core}{sex}'.format(date=pesel_date, core=pesel_core, sex=pesel_sex)
        pesel += str(self.pesel_compute_check_digit(pesel))

        return pesel

    @staticmethod
    def pwz_doctor_compute_check_digit(x):
        return sum((i + 1) * d for i, d in enumerate(x)) % 11

    def pwz_doctor(self):
        """
        Function generates an identification number for medical doctors
        Polish: Prawo Wykonywania Zawodu (PWZ)

        https://www.nil.org.pl/rejestry/centralny-rejestr-lekarzy/zasady-weryfikowania-nr-prawa-wykonywania-zawodu
        """
        core = [self.random_digit() for _ in range(6)]
        check_digit = self.pwz_doctor_compute_check_digit(core)

        if check_digit == 0:
            core[-1] = (core[-1] + 1) % 10
            check_digit = self.pwz_doctor_compute_check_digit(core)

        return '{}{}'.format(check_digit, ''.join(map(str, core)))

    def pwz_nurse(self, kind='nurse'):
        """
        Function generates an identification number for nurses and midwives
        Polish: Prawo Wykonywania Zawodu (PWZ)

        http://arch.nipip.pl/index.php/prawo/uchwaly/naczelnych-rad/w-roku-2015/posiedzenie-15-17-grudnia/3664-uchwala-
        nr-381-vi-2015-w-sprawie-trybu-postepowania-dotyczacego-stwierdzania-i-przyznawania-prawa-wykonywania-zawodu-pi
        elegniarki-i-zawodu-poloznej-oraz-sposobu-prowadzenia-rejestru-pielegniarek-i-rejestru-poloznych-przez-okregowe
        -rady-pielegniarek-i-polo
        """
        region = self.random_int(1, 45)
        core = [self.random_digit() for _ in range(5)]
        kind_char = 'A' if kind == 'midwife' else 'P'

        return '{:02d}{}{}'.format(region, ''.join(map(str, core)), kind_char)

    tax_office_codes = (
        '101', '102', '103', '104', '105', '106', '107', '108', '109', '111', '112', '113', '114', '115', '116', '117',
        '118', '119', '121', '122', '123', '124', '125', '126', '127', '128', '129', '131', '132', '133', '134', '135',
        '136', '137', '138', '139', '141', '142', '143', '144', '145', '146', '147', '148', '149', '151', '152', '153',
        '154', '155', '156', '157', '158', '159', '161', '162', '163', '164', '165', '166', '167', '168', '169', '171',
        '172', '173', '174', '175', '176', '177', '178', '179', '181', '182', '183', '184', '185', '186', '187', '188',
        '189', '191', '192', '193', '194', '195', '196', '197', '198', '199', '201', '202', '203', '204', '205', '206',
        '207', '208', '209', '211', '212', '213', '214', '215', '216', '217', '218', '219', '221', '222', '223', '224',
        '225', '226', '227', '228', '229', '231', '232', '233', '234', '235', '236', '237', '238', '239', '241', '242',
        '243', '244', '245', '246', '247', '248', '249', '251', '252', '253', '254', '255', '256', '257', '258', '259',
        '261', '262', '263', '264', '265', '266', '267', '268', '269', '271', '272', '273', '274', '275', '276', '277',
        '278', '279', '281', '282', '283', '284', '285', '286', '287', '288', '289', '291', '292', '293', '294', '295',
        '296', '297', '298', '301', '302', '311', '312', '313', '314', '315', '316', '317', '318', '319', '321', '322',
        '323', '324', '325', '326', '327', '328', '329', '331', '332', '333', '334', '335', '336', '337', '338', '339',
        '341', '342', '343', '344', '345', '346', '347', '348', '349', '351', '352', '353', '354', '355', '356', '357',
        '358', '359', '361', '362', '363', '364', '365', '366', '367', '368', '369', '371', '372', '373', '374', '375',
        '376', '377', '378', '379', '381', '382', '383', '384', '385', '386', '387', '388', '389', '391', '392', '393',
        '394', '395', '396', '397', '398', '399', '411', '412', '413', '414', '415', '416', '417', '418', '419', '421',
        '422', '423', '424', '425', '426', '427', '428', '429', '431', '432', '433', '434', '435', '436', '437', '438',
        '439', '441', '442', '443', '444', '445', '446', '447', '448', '449', '451', '452', '453', '454', '455', '456',
        '457', '458', '459', '461', '462', '463', '464', '465', '466', '467', '468', '469', '471', '472', '473', '474',
        '475', '476', '477', '478', '479', '481', '482', '483', '484', '485', '486', '487', '488', '489', '491', '492',
        '493', '494', '495', '496', '497', '498', '499', '501', '502', '503', '504', '505', '506', '507', '508', '509',
        '511', '512', '513', '514', '516', '519', '521', '522', '523', '524', '525', '526', '527', '528', '529', '531',
        '532', '533', '534', '535', '536', '537', '538', '539', '541', '542', '543', '544', '545', '546', '547', '548',
        '549', '551', '552', '553', '554', '555', '556', '557', '558', '559', '561', '562', '563', '564', '565', '566',
        '567', '568', '569', '571', '572', '573', '574', '575', '576', '577', '578', '579', '581', '582', '583', '584',
        '585', '586', '587', '588', '589', '591', '592', '593', '594', '595', '596', '597', '598', '599', '601', '602',
        '603', '604', '605', '606', '607', '608', '609', '611', '612', '613', '614', '615', '616', '617', '618', '619',
        '621', '622', '623', '624', '625', '626', '627', '628', '629', '631', '632', '633', '634', '635', '636', '637',
        '638', '639', '641', '642', '643', '644', '645', '646', '647', '648', '649', '651', '652', '653', '654', '655',
        '656', '657', '658', '659', '661', '662', '663', '664', '665', '666', '667', '668', '669', '671', '672', '673',
        '674', '675', '676', '677', '678', '679', '681', '682', '683', '684', '685', '686', '687', '688', '689', '691',
        '692', '693', '694', '695', '696', '697', '698', '699', '701', '711', '712', '713', '714', '715', '716', '717',
        '718', '719', '721', '722', '723', '724', '725', '726', '727', '728', '729', '731', '732', '733', '734', '735',
        '736', '737', '738', '739', '741', '742', '743', '744', '745', '746', '747', '748', '749', '751', '752', '753',
        '754', '755', '756', '757', '758', '759', '761', '762', '763', '764', '765', '766', '767', '768', '769', '771',
        '772', '773', '774', '775', '776', '777', '778', '779', '781', '782', '783', '784', '785', '786', '787', '788',
        '789', '791', '792', '793', '794', '795', '796', '797', '798', '799', '811', '812', '813', '814', '815', '816',
        '817', '818', '819', '821', '822', '823', '824', '825', '826', '827', '828', '829', '831', '832', '833', '834',
        '835', '836', '837', '838', '839', '841', '842', '843', '844', '845', '846', '847', '848', '849', '851', '852',
        '853', '854', '855', '856', '857', '858', '859', '861', '862', '863', '864', '865', '866', '867', '868', '869',
        '871', '872', '873', '874', '875', '876', '877', '878', '879', '881', '882', '883', '884', '885', '886', '887',
        '888', '889', '891', '892', '893', '894', '895', '896', '897', '898', '899', '911', '912', '913', '914', '915',
        '916', '917', '918', '919', '921', '922', '923', '924', '925', '926', '927', '928', '929', '931', '932', '933',
        '934', '935', '936', '937', '938', '939', '941', '942', '943', '944', '945', '946', '947', '948', '949', '951',
        '952', '953', '954', '955', '956', '957', '958', '959', '961', '962', '963', '964', '965', '966', '967', '968',
        '969', '971', '972', '973', '974', '975', '976', '977', '978', '979', '981', '982', '983', '984', '985', '986',
        '987', '988', '989', '991', '992', '993', '994', '995', '996', '997', '998',
    )

    def nip(self):
        """
        Returns 10 digit of Number of tax identification.
        Polish: Numer identyfikacji podatkowej (NIP).

        https://pl.wikipedia.org/wiki/NIP
        list of codes
        http://www.algorytm.org/numery-identyfikacyjne/nip.html

        """

        nip = [int(i) for i in self.random_element(self.tax_office_codes)]
        for _ in range(6):
            nip.append(self.random_digit())

        weights = (6, 5, 7, 2, 3, 4, 5, 6, 7)
        check_sum = sum(d * w for d, w in zip(nip, weights)) % 11

        if check_sum % 11 == 10:
            position = self.random_int(3, 8)
            if nip[position] < 9:
                nip[position] = (nip[position] + 1) % 10
                nip.append((check_sum + weights[position]) % 11)
            else:
                nip[position] = (nip[position] - 1) % 10
                nip.append((check_sum - weights[position]) % 11)

        else:
            nip.append(check_sum % 11)

        return ''.join(str(character) for character in nip)
