fprm_prompt = '''
Your task is to fill in the missing values in the target entry from the `california_schools` database.
Return a single row and with no explanation.

The columns are: `School Name`,`District Name`,`Educational Option Type`,`Charter School (1/0)`,`Charter Funding Type`.

The possible cell values for `Educational Option Type` are: ```
['Traditional', 'Juvenile Court School', 'County Community School', 'State Special School', 'Alternative School of Choice', 'Continuation School', 'Special Education School', 'Community Day School', 'Home and Hospital', 'Opportunity School', 'Youth Authority School', 'District Special Education Consortia School']
```

/*One example is provided before the target data entry*/
Example Entry:'FAME Public Charter','Alameda County Office of Education',?,?,?
Example Answer:'FAME Public Charter','Alameda County Office of Education','Traditional',1,'Directly funded'


Target Entry:'{school_name}','{district_name}',?,?,?
Answer:
'''
schools_prompt = '''
Your task is to fill in the missing values in the target entry from the `california_schools` database.
Return a single row and with no explanation.

The columns are: `Street`, `School`, `City`, `County`, `Magnet`, `Website`, `ExclusivelyVirtual (Y/N)`

/*One example is provided before the target data entry*/
Example Entry:'1515 Webster Street','Envision Academy for Arts & Technology',?,?,?,?,?
Example Answer:'1515 Webster Street','Envision Academy for Arts & Technology','Oakland','Alameda',0,'www.envisionacademy.org/','N'


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

/*One example is provided before the target data entry*/
Example Entry:'3-D Man','Charles Chandler',?,?,?,?,?,?,?,?
Example Answer:'3-D Man','Charles Chandler','Brown','Grey','No Colour','Marvel Comics','-','Male','Good','Agility,Super Strength,Stamina,Super Speed'

Target Entry:'{superhero_name}','{full_name}',?,?,?,?,?,?,?,?
Answer:
'''

llm_circuits_prompt = '''
Your task is to fill in the missing values in the target entry from the `formula_1` database.
Return a single row and with no explanation.

The columns are:`circuit_location`,`circuit_name`,`country`,`url`,`latitude`,`longitude`

/*One example is provided before the target data entry*/
Example Entry:'Kuala Lumpur','Sepang International Circuit',?,?,?,?
Example Answer:'Kuala Lumpur','Sepang International Circuit','Malaysia','http://en.wikipedia.org/wiki/Sepang_International_Circuit',2.76083,101.738

Target Entry:'{location}','{name}',?,?,?,?
Answer:
'''

llm_people_prompt = '''
Your task is to fill in the missing values in the target entry from the `formula_1` database.
Return a single row and with no explanation.

The columns are:`name`,`dob`,`driver_code`,`nationality`,`person_url`

/*One example is provided before the target data entry*/
Example Entry:'AFM',NULL,NULL,?,?
Example Answer:'AFM',NULL,NULL,'German','http://en.wikipedia.org/wiki/Alex_von_Falkenhausen_Motorenbau'

Target Entry:'{name}',{dob},{code},?,?
Answer:
'''


llm_race_prompt = '''
Your task is to fill in the missing values in the target entry from the `formula_1` database.
Return a single row and with no explanation.

The columns are:`race_name`,`race_year`,`race_date`,`season_url`

/*One example is provided before the target data entry*/
Example Entry:'Australian Grand Prix',2009,?,?
Example Answer:'Australian Grand Prix',2009,'2009-03-29','http://en.wikipedia.org/wiki/2009_Formula_One_season'


Target Entry:'{race}',{year},?,?
Answer:
'''

llm_match_prompt = '''
Your task is to fill in the missing values in the target entry from the `european_football` database.
Return a single row and with no explanation.

The columns are:`home_team`,`away_team`,`date`,`league_name`,`home_team_goal`,`away_team_goal`,`country_name`

/*One example is provided before the target data entry*/
Example Entry:'KRC Genk','Beerschot AC','2008-08-17 00:00:00',?,?,?,?
Example Answer:'KRC Genk','Beerschot AC','2008-08-17 00:00:00','Belgium Jupiler League',1,1,'Belgium'

Target Entry:'{home_team}','{away_team}','{date}',?,?,?,?
Answer:
'''

llm_team_prompt = '''
Your task is to fill in the missing values in the target entry from the `european_football` database.
Return a single row and with no explanation.

The columns are:`team_long_name`,`team_short_name`

/*One example is provided before the target data entry*/
Example Entry:'KRC Genk',?
Example Answer:'KRC Genk','GEN'

Target Entry:'{team_long_name}',?
Answer:
'''


llm_player_prompt = '''
Your task is to fill in the missing values in the target entry from the `european_football` database.
Return a single row and with no explanation.

The columns are:`player_name`,`weight`,`birthday`,`preferred_foot`,`height`

/*One example is provided before the target data entry*/
Example Entry:'Aaron Appindangoye',187,?,?,?
Example Answer:'Aaron Appindangoye',187,'1992-02-29 00:00:00','right',182.88

Target Entry:'{player_name}',{weight},?,?,?
Answer:
'''
