fprm_prompt = '''
Your task is to fill in the missing values in the target entry from the `california_schools` database.
Return a single row and with no explanation.

The columns are: `School Name`,`District Name`,`Educational Option Type`,`Charter School (1/0)`,`Charter Funding Type`.

The possible cell values for `Educational Option Type` are: ```
['Traditional', 'Juvenile Court School', 'County Community School', 'State Special School', 'Alternative School of Choice', 'Continuation School', 'Special Education School', 'Community Day School', 'Home and Hospital', 'Opportunity School', 'Youth Authority School', 'District Special Education Consortia School']
```

/*Five examples are provided before the target data entry*/
Example Entry:'FAME Public Charter','Alameda County Office of Education',?,?,?
Example Answer:'FAME Public Charter','Alameda County Office of Education','Traditional',1,'Directly funded'

Example Entry:'Charter Community School Home Study Academy','El Dorado County Office of Education',?,?,?
Example Answer:'Charter Community School Home Study Academy','El Dorado County Office of Education','County Community School',1,'Locally funded'

Example Entry:'Alameda County Juvenile Hall/Court','Alameda County Office of Education',?,?,?
Example Answer:'Alameda County Juvenile Hall/Court','Alameda County Office of Education','Juvenile Court School',0,NULL

Example Entry:'Yu Ming Charter','Alameda County Office of Education',?,?,?
Example Answer:'Yu Ming Charter','Alameda County Office of Education','Traditional',1,'Directly funded'

Example Entry:'California School for the Deaf-Fremont','California School for the Deaf-Fremont (State Special Schl)',?,?,?
Example Answer:'California School for the Deaf-Fremont','California School for the Deaf-Fremont (State Special Schl)','State Special School',0,NULL

Target Entry:'{school_name}','{district_name}',?,?,?
Answer:
'''

schools_prompt = '''
Your task is to fill in the missing values in the target entry from the `california_schools` database.
Return a single row and with no explanation.

The columns are: `Street`, `School`, `City`, `County`, `Magnet`, `Website`, `ExclusivelyVirtual (Y/N)`

/*Five examples are provided before the target data entry*/
Example Entry:'1515 Webster Street','Envision Academy for Arts & Technology',?,?,?,?,?
Example Answer:'1515 Webster Street','Envision Academy for Arts & Technology','Oakland','Alameda',0,'www.envisionacademy.org/','N'

Example Entry:'2125 Jefferson Avenue','Aspire California College Preparatory Academy',?,?,?,?,?
Example Answer:'2125 Jefferson Avenue','Aspire California College Preparatory Academy','Berkeley','Alameda',0,'www.aspirepublicschools.org','N'

Example Entry:'39500 Dunlap Road','Dunlap Leadership Academy',?,?,?,?,?
Example Answer:'39500 Dunlap Road','Dunlap Leadership Academy','Dunlap','Fresno',0,'www.kcusd.com','Y'

Example Entry:'5328 Brann Street','Urban Montessori Charter',?,?,?,?,?
Example Answer:'5328 Brann Street','Urban Montessori Charter','Oakland',0,'www.urbanmontessori.org','N','Alameda'

Example Entry:'755 Oak Grove Road','Ygnacio Valley High',?,?,?,?,?
Example Answer:'755 Oak Grove Road','Ygnacio Valley High','Concord',1,'www.mdusd.org','N','Contra Costa'

Target Entry:'{street_name}','{school_name}',?,?,?,?,?
Answer:
'''


superhero_prompt = '''
Your task is to fill in the missing values in the target entry from the `superhero` database.
Return a single row and with no explanation.

The columns are: `superhero_name`,`full_name`,`eye_color`,`hair_color`,`skin_color`,`publisher_name`,`race`,`gender`,`moral_alignment`,`powers`


The possible cell values for different colors are: ```
['No Colour', 'Amber', 'Auburn', 'Black', 'Black/Blue', 'Blond', 'Blue', 'Blue/White', 'Brown', 'Brown/Black', 'Brown/White', 'Gold', 'Grey', 'Green', 'Green/Blue', 'Hazel', 'Indigo', 'Magenta', 'Orange', 'Orange/White', 'Pink', 'Purple', 'Red', 'Red/Black', 'Red/Grey', 'Red/Orange', 'Red/White', 'Silver', 'Strawberry Blond', 'Violet', 'White', 'White/Red', 'Yellow', 'Yellow/Blue', 'Yellow/Red']
```

The possible cell values for ·publisher_name` are:```
['', 'ABC Studios', 'Dark Horse Comics', 'DC Comics', 'George Lucas', 'Hanna-Barbera', 'HarperCollins', 'Icon Comics', 'IDW Publishing', 'Image Comics', 'J. K. Rowling', 'J. R. R. Tolkien', 'Marvel Comics', 'Microsoft', 'NBC - Heroes', 'Rebellion', 'Shueisha', 'Sony Pictures', 'South Park', 'Star Trek', 'SyFy', 'Team Epic TV', 'Titan Books', 'Universal Studios', 'Wildstorm']
```

The possible cell values for `race` are: ```
['-', 'Alien', 'Alpha', 'Amazon', 'Android', 'Animal', 'Asgardian', 'Atlantean', 'Bizarro', 'Bolovaxian', 'Clone', 'Cosmic Entity', 'Cyborg', 'Czarnian', 'Dathomirian Zabrak', 'Demi-God', 'Demon', 'Eternal', 'Flora Colossus', 'Frost Giant', 'God / Eternal', 'Gorilla', 'Gungan', 'Human', 'Human / Altered', 'Human / Clone', 'Human / Cosmic', 'Human / Radiation', 'Human-Kree', 'Human-Spartoi', 'Human-Vulcan', 'Human-Vuldarian', 'Icthyo Sapien', 'Inhuman', 'Kakarantharaian', 'Korugaran', 'Kryptonian', 'Luphomoid', 'Maiar', 'Martian', 'Metahuman', 'Mutant', 'Mutant / Clone', 'New God', 'Neyaphem', 'Parademon', 'Planet', 'Rodian', 'Saiyan', 'Spartoi', 'Strontian', 'Symbiote', 'Talokite', 'Tamaranean', 'Ungaran', 'Vampire', 'Xenomorph XX121', 'Yautja', "Yoda's species", 'Zen-Whoberian', 'Zombie']
```

The possible power names are:```
['Agility', 'Accelerated Healing', 'Lantern Power Ring', 'Dimensional Awareness', 'Cold Resistance', 'Durability', 'Stealth', 'Energy Absorption', 'Flight', 'Danger Sense', 'Underwater breathing', 'Marksmanship', 'Weapons Master', 'Power Augmentation', 'Animal Attributes', 'Longevity', 'Intelligence', 'Super Strength', 'Cryokinesis', 'Telepathy', 'Energy Armor', 'Energy Blasts', 'Duplication', 'Size Changing', 'Density Control', 'Stamina', 'Astral Travel', 'Audio Control', 'Dexterity', 'Omnitrix', 'Super Speed', 'Possession', 'Animal Oriented Powers', 'Weapon-based Powers', 'Electrokinesis', 'Darkforce Manipulation', 'Death Touch', 'Teleportation', 'Enhanced Senses', 'Telekinesis', 'Energy Beams', 'Magic', 'Hyperkinesis', 'Jump', 'Clairvoyance', 'Dimensional Travel', 'Power Sense', 'Shapeshifting', 'Peak Human Condition', 'Immortality', 'Camouflage', 'Element Control', 'Phasing', 'Astral Projection', 'Electrical Transport', 'Fire Control', 'Projection', 'Summoning', 'Enhanced Memory', 'Reflexes', 'Invulnerability', 'Energy Constructs', 'Force Fields', 'Self-Sustenance', 'Anti-Gravity', 'Empathy', 'Power Nullifier', 'Radiation Control', 'Psionic Powers', 'Elasticity', 'Substance Secretion', 'Elemental Transmogrification', 'Technopath/Cyberpath', 'Photographic Reflexes', 'Seismic Power', 'Animation', 'Precognition', 'Mind Control', 'Fire Resistance', 'Power Absorption', 'Enhanced Hearing', 'Nova Force', 'Insanity', 'Hypnokinesis', 'Animal Control', 'Natural Armor', 'Intangibility', 'Enhanced Sight', 'Molecular Manipulation', 'Heat Generation', 'Adaptation', 'Gliding', 'Power Suit', 'Mind Blast', 'Probability Manipulation', 'Gravity Control', 'Regeneration', 'Light Control', 'Echolocation', 'Levitation', 'Toxin and Disease Control', 'Banish', 'Energy Manipulation', 'Heat Resistance', 'Natural Weapons', 'Time Travel', 'Enhanced Smell', 'Illusions', 'Thirstokinesis', 'Hair Manipulation', 'Illumination', 'Omnipotent', 'Cloaking', 'Changing Armor', 'Power Cosmic', 'Biokinesis', 'Water Control', 'Radiation Immunity', 'Vision - Telescopic', 'Toxin and Disease Resistance', 'Spatial Awareness', 'Energy Resistance', 'Telepathy Resistance', 'Molecular Combustion', 'Omnilingualism', 'Portal Creation', 'Magnetism', 'Mind Control Resistance', 'Plant Control', 'Sonar', 'Sonic Scream', 'Time Manipulation', 'Enhanced Touch', 'Magic Resistance', 'Invisibility', 'Sub-Mariner', 'Radiation Absorption', 'Intuitive aptitude', 'Vision - Microscopic', 'Melting', 'Wind Control', 'Super Breath', 'Wallcrawling', 'Vision - Night', 'Vision - Infrared', 'Grim Reaping', 'Matter Absorption', 'The Force', 'Resurrection', 'Terrakinesis', 'Vision - Heat', 'Vitakinesis', 'Radar Sense', 'Qwardian Power Ring', 'Weather Control', 'Vision - X-Ray', 'Vision - Thermal', 'Web Creation', 'Reality Warping', 'Odin Force', 'Symbiote Costume', 'Speed Force', 'Phoenix Force', 'Molecular Dissipation', 'Vision - Cryo', 'Omnipresent', 'Omniscient']
```


/*Five examples are provided before the target data entry*/
Example Entry:'3-D Man','Charles Chandler',?,?,?,?,?,?,?,?
Example Answer:'3-D Man','Charles Chandler','Brown','Grey','No Colour','Marvel Comics','-','Male','Good','Agility,Super Strength,Stamina,Super Speed'

Example Entry:'Lucifer Morningstar','-',?,?,?,?,?,?,?,?
Example Answer:'Lucifer Morningstar','-','Amber','Blond','No Colour','DC Comics','God / Eternal','Male','Neutral',NULL

Example Entry:'Abe Sapien','Abraham Sapien',?,?,?,?,?,?,?,?
Example Answer:'Abe Sapien','Abraham Sapien','Blue','No Colour','Blue','Dark Horse Comics','Icthyo Sapien','Male','Good','Agility,Accelerated Healing,Cold Resistance,Durability,Underwater breathing,Marksmanship,Weapons Master,Longevity,Intelligence,Super Strength,Telepathy,Stamina,Immortality,Reflexes,Enhanced Sight,Sub-Mariner'

Example Entry:'Abomination','Emil Blonsky',?,?,?,?,?,?,?,?
Example Answer:'Abomination','Emil Blonsky','Green','No Colour','No Colour','Marvel Comics','Human / Radiation','Male','Bad','Accelerated Healing,Intelligence,Super Strength,Stamina,Super Speed,Invulnerability,Animation,Super Breath'

Example Entry:'Lucifer Morningstar','-',?,?,?,?,?,?,?,?
Example Answer:'Abin Sur','-','Blue','No Colour','Red','DC Comics','Ungaran','Male','Good','Lantern Power Ring'

Target Entry:'{superhero_name}','{full_name}',?,?,?,?,?,?,?,?
Answer:
'''

llm_circuits_prompt = '''
Your task is to fill in the missing values in the target entry from the `formula_1` database.
Return a single row and with no explanation.

The columns are:`circuit_location`,`circuit_name`,`country`,`url`,`latitude`,`longitude`

/*Five examples are provided before the target data entry*/
Example Entry:'Kuala Lumpur','Sepang International Circuit',?,?,?,?
Example Answer:'Kuala Lumpur','Sepang International Circuit','Malaysia','http://en.wikipedia.org/wiki/Sepang_International_Circuit',2.76083,101.738

Example Entry:'Sakhir','Bahrain International Circuit',?,?,?,?
Example Answer:'Sakhir','Bahrain International Circuit','Bahrain','http://en.wikipedia.org/wiki/Bahrain_International_Circuit',26.0325,50.5106

Example Entry:'Montmeló','Circuit de Barcelona-Catalunya',?,?,?,?
Example Answer:'Montmeló','Circuit de Barcelona-Catalunya','Spain','http://en.wikipedia.org/wiki/Circuit_de_Barcelona-Catalunya',41.57,2.26111

Example Entry:'Istanbul','Istanbul Park',?,?,?,?
Example Answer:'Istanbul','Istanbul Park','Turkey','http://en.wikipedia.org/wiki/Istanbul_Park',40.9517,29.405

Example Entry:'Monte-Carlo','Circuit de Monaco',?,?,?,?
Example Answer:'Monte-Carlo','Circuit de Monaco','Monaco','http://en.wikipedia.org/wiki/Circuit_de_Monaco',43.7347,7.42056

Target Entry:'{location}','{name}',?,?,?,?
Answer:
'''

llm_people_prompt = '''
Your task is to fill in the missing values in the target entry from the `formula_1` database.
Return a single row and with no explanation.

The columns are:`name`,`dob`,`driver_code`,`nationality`,`person_url`

/*Five examples are provided before the target data entry*/
Example Entry:'AFM',NULL,NULL,?,?
Example Answer:'AFM',NULL,NULL,'German','http://en.wikipedia.org/wiki/Alex_von_Falkenhausen_Motorenbau'

Example Entry:'BMW Sauber',NULL,NULL,?,?
Example Answer'BMW Sauber',NULL,NULL,'German','http://en.wikipedia.org/wiki/BMW_Sauber'

Example Entry:'LewisHamilton',?,?,?,?
Example Answer:'LewisHamilton','1985-01-07','HAM','British','http://en.wikipedia.org/wiki/Lewis_Hamilton'

Example Entry:'NickHeidfeld',?,?,?,?
Example Answer:'NickHeidfeld','1977-05-10','HEI','German','http://en.wikipedia.org/wiki/Nick_Heidfeld'

Example Entry:'NicoRosberg',?,?,?,?
Example Answer:'NicoRosberg','1985-06-27','ROS','German','http://en.wikipedia.org/wiki/Nico_Rosberg',

Target Entry:'{name}',{dob},{code},?,?
Answer:
'''


llm_race_prompt = '''
Your task is to fill in the missing values in the target entry from the `formula_1` database.
Return a single row and with no explanation.

The columns are:`race_name`,`race_year`,`race_date`,`season_url`

/*Five examples are provided before the target data entry*/
Example Entry:'Australian Grand Prix',2009,?,?
Example Answer:'Australian Grand Prix',2009,'2009-03-29','http://en.wikipedia.org/wiki/2009_Formula_One_season'

Example Entry:'Bahrain Grand Prix',2008,?,?
Example Answer:'Bahrain Grand Prix',2008,'2008-04-06','http://en.wikipedia.org/wiki/2008_Formula_One_season'

Example Entry:'Malaysian Grand Prix',2007,?,?
Example Answer:'Malaysian Grand Prix',2007,'2007-04-08','http://en.wikipedia.org/wiki/2007_Formula_One_season'

Example Entry:'Bahrain Grand Prix',2009,?,?
Example Answer:'Bahrain Grand Prix',2009,'2009-04-26','http://en.wikipedia.org/wiki/2009_Formula_One_season'

Example Entry:'Spanish Grand Prix',2009,?,?
Example Answer:'Spanish Grand Prix',2009,'2009-05-10','http://en.wikipedia.org/wiki/2009_Formula_One_season'

Target Entry:'{race}',{year},?,?
Answer:
'''




llm_match_prompt = '''
Your task is to fill in the missing values in the target entry from the `european_football` database.
Return a single row and with no explanation.

The columns are:`home_team`,`away_team`,`date`,`league_name`,`home_team_goal`,`away_team_goal`,`country_name`

/*Five examples are provided before the target data entry*/
Example Entry:'KRC Genk','Beerschot AC','2008-08-17 00:00:00',?,?,?,?
Example Answer:'KRC Genk','Beerschot AC','2008-08-17 00:00:00','Belgium Jupiler League',1,1,'Belgium'

Example Entry:'SV Zulte-Waregem','Sporting Lokeren','2008-08-16 00:00:00',?,?,?,?
Example Answer:'SV Zulte-Waregem','Sporting Lokeren','2008-08-16 00:00:00','Belgium Jupiler League',0,0,'Belgium'

Example Entry:'KSV Cercle Brugge','RSC Anderlecht','2008-08-16 00:00:00',?,?,?,?
Example Answer:'KSV Cercle Brugge','RSC Anderlecht','2008-08-16 00:00:00','Belgium Jupiler League',0,3,'Belgium'

Example Entry:''FCV Dender EH','Standard de Liège','2008-08-16 00:00:00',?,?,?,?
Example Answer:'FCV Dender EH','Standard de Liège','2008-08-16 00:00:00','Belgium Jupiler League',1,3,'Belgium'

Example Entry:'Manchester United','Newcastle United','2008-08-17 00:00:00',?,?,?,?
Example Answer:'Manchester United','Newcastle United','2008-08-17 00:00:00','England Premier League',1,1,'England'

Target Entry:'{home_team}','{away_team}','{date}',?,?,?,?
Answer:
'''

llm_team_prompt = '''
Your task is to fill in the missing values in the target entry from the `european_football` database.
Return a single row and with no explanation.

The columns are:`team_long_name`,`team_short_name`

/*Five examples are provided before the target data entry*/
Example Entry:'KRC Genk',?
Example Answer:'KRC Genk','GEN'

Example Entry:'Beerschot AC',?
Example Answer:'Beerschot AC','BAC'

Example Entry:'SV Zulte-Waregem',?
Example Answer:'SV Zulte-Waregem','ZUL'

Example Entry:'Sporting Lokeren',?
Example Answer:'Sporting Lokeren','LOK'

Example Entry:'KSV Cercle Brugge',?
Example Answer:'KSV Cercle Brugge','CEB'

Target Entry:'{team_long_name}',?
Answer:
'''


llm_player_prompt = '''
Your task is to fill in the missing values in the target entry from the `european_football` database.
Return a single row and with no explanation.

The columns are:`player_name`,`weight`,`birthday`,`preferred_foot`,`height`

/*Five examples are provided before the target data entry*/
Example Entry:'Aaron Appindangoye',187,?,?,?
Example Answer:'Aaron Appindangoye',187,'1992-02-29 00:00:00','right',182.88

Example Entry:'Aaron Doran',163,?,?,?
Example Answer:'Aaron Doran',163,'1991-05-13 00:00:00','right',170.18

Example Entry:'Aaron Galindo',198,?,?,?
Example Answer:'Aaron Galindo',198,'1982-05-08 00:00:00','right',182.88

Example Entry:'Aaron Hughes',154,?,?,?
Example Answer:'Aaron Hughes',154,'1979-11-08 00:00:00','right',182.88

Example Entry:'Aaron Hunt',161,?,?,?
Example Answer:'Aaron Hunt',161,'1986-09-04 00:00:00','left',182.88

Target Entry:'{player_name}',{weight},?,?,?
Answer:
'''