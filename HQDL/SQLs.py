create_california_llm_table = '''
CREATE TABLE llm (
    "School Name" TEXT,
    "District Name" TEXT,
    "Educational Option Type" TEXT,
    "Charter School (Y/N)" TEXT,
    "Charter Funding Type" TEXT,
    "Street" TEXT,
    "School" TEXT,
    "City" TEXT,
    "Magnet" TEXT,
    "Website" TEXT,
    "ExclusivelyVirtual" TEXT,
    "County" TEXT
)
'''

california_llm_table_insert_records = '''
INSERT INTO llm (
    "School Name", 
    "District Name", 
    "Educational Option Type", 
    "Charter School (Y/N)", 
    "Charter Funding Type", 
    "Street", 
    "School", 
    "City",
    "County",
    "Magnet", 
    "Website",
    "ExclusivelyVirtual"
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''


create_superhero_llm_table = '''
CREATE TABLE llm (
    "superhero_name" TEXT,
    "full_name" TEXT,
    "eye_color" TEXT,
    "hair_color" TEXT,
    "skin_color" TEXT,
    "publisher_name" TEXT,
    "race" TEXT,
    "gender" TEXT,
    "moral_alignment" TEXT
)
'''

create_superhero_llm_hero_2_power_table = '''
CREATE TABLE llm_hero_2_power (
    "superhero_name" TEXT,
    "full_name" TEXT,
    "power_name" TEXT
)
'''

superhero_llm_insert_records = '''
INSERT INTO llm (
    "superhero_name", 
    "full_name", 
    "eye_color",
    "hair_color",
    "skin_color",
    "publisher_name",
    "race",
    "gender",
    "moral_alignment"
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
'''



llm_hero_2_power_insert_records = '''
INSERT INTO llm_hero_2_power (
    "superhero_name", 
    "full_name", 
    "power_name"
) VALUES (?, ?, ?)
'''

create_formula_1_llm_circuits = '''
CREATE TABLE llm_circuits (
    "location" TEXT,
    "name" TEXT,
    "country" TEXT,
    "url" TEXT,
    "lat" REAL,
    "lng" REAL
)
'''

create_formula_1_llm_people = '''
CREATE TABLE llm_people (
    "name" TEXT,
    "nationality" TEXT,
    "dob" TEXT,
    "person_url" TEXT,
    "driver_code" TEXT
)
'''
create_formula_1_llm_races = '''
CREATE TABLE llm_races (
    "name" TEXT,
    "year" TEXT,
    "date" TEXT,
    "season_url" TEXT
)
'''

llm_circuits_insert_records = '''
INSERT INTO llm_circuits (
    "location",
    "name",
    "country",
    "url",
    "lat",
    "lng"
) VALUES (?, ?, ?, ?, ?, ?)
'''

llm_people_insert_records = '''
INSERT INTO llm_people (
    "name",
    "nationality",
    "dob",
    "person_url",
    "driver_code"
) VALUES (?, ?, ?, ?, ?)
'''

llm_races_insert_records = '''
INSERT INTO llm_races (
    "name",
    "year",
    "date",
    "season_url"
) VALUES (?, ?, ?, ?)
'''


create_football_llm_match = '''
CREATE TABLE llm_match (
    "home_team" TEXT,
    "away_team" TEXT,
    "date" TEXT,
    "league_name" TEXT,
    "home_team_goal" INT,
    "away_team_goal" INT,
    "country_name" TEXT
)
'''

create_football_llm_team = '''
CREATE TABLE llm_team (
    "team_long_name" TEXT,
    "team_short_name" TEXT
)
'''

create_football_llm_player = '''
CREATE TABLE llm_player (
    "player_name" TEXT,
    "weight" INT,
    "birthday" TEXT,
    "preferred_foot" TEXT,
    "height" INTEGER
)
'''

llm_match_insert_records = '''
INSERT INTO llm_match (
    "home_team",
    "away_team",
    "date",
    "league_name",
    "home_team_goal",
    "away_team_goal",
    "country_name"
) VALUES (?, ?, ?, ?, ?, ?, ?)
'''


llm_team_insert_records = '''
INSERT INTO llm_team (
    "team_long_name",
    "team_short_name"
) VALUES (?, ?)
'''

llm_player_insert_records = '''
INSERT INTO llm_player (
    "player_name",
    "weight",
    "birthday",
    "preferred_foot",
    "height"
) VALUES (?, ?, ?, ? ,?)
'''





