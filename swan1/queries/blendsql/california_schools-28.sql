SELECT COUNT(schools.CDSCode) 
 FROM schools
WHERE schools.MailState = 'CA' AND schools.StatusType = 'Active' AND {{
        LLMMap(
            'Is the address located in San Joaquin City?',
            schools.Street
        )
    }} = TRUE
