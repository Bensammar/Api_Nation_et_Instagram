import requests
import json
import pyodbc


def save_to_database(reponse_json):

    with open('reponse_json_countries.json', 'w') as jsonFile:
        json.dump(reponse_json, jsonFile)

    conn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=DESKTOP-VI25AP9;'
                          'DATABASE=countries;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute("""DECLARE @json NVARCHAR(MAX); SET @json = (SELECT  * FROM OPENROWSET 
    (BULK 'C:\\Users\\Fouzi\\PycharmProjects\\untitled\\BDDAPI\\reponse_json_countries.json',SINGLE_CLOB) AS json);    
      
    IF OBJECT_ID('dbo.currencies') IS NOT NULL
      DROP TABLE dbo.currencies;
      
    IF OBJECT_ID('dbo.primary_languages') IS NOT NULL
      DROP TABLE dbo.primary_languages;
    
    IF OBJECT_ID('dbo.regionalBlocs') IS NOT NULL
      DROP TABLE dbo.regionalBlocs;
      
    IF OBJECT_ID('dbo.countries') IS NOT NULL
      DROP TABLE dbo.countries;
      
    SELECT * INTO countries
    FROM OPENJSON(@json)
      WITH (        
        alpha2Code NVARCHAR(500) '$.alpha2Code',
        alpha3Code NVARCHAR(500) '$.alpha3Code',
        numericCode NVARCHAR(500) '$.numericCode',
        name NVARCHAR(500) '$.name',
        capital NVARCHAR(500) '$.capital',
        demonym NVARCHAR(500) '$.demonym',
        area NVARCHAR(500) '$.area',
        population NVARCHAR(500) '$.population',
        region NVARCHAR(500) '$.region',
        subregion NVARCHAR(500) '$.subregion',
        nativeName NVARCHAR(500) '$.nativeName'                        
      );
            
    ALTER TABLE countries ALTER COLUMN alpha2Code NVARCHAR(500) NOT NULL;    
    ALTER TABLE countries ADD PRIMARY KEY (alpha2Code);
    
    SELECT * INTO currencies
    FROM OPENJSON(@json)
      WITH (
        alpha2Code NVARCHAR(500) '$.alpha2Code',       
        code NVARCHAR(500) '$.currencies[0].code',
        name NVARCHAR(500) '$.currencies[0].name',
        symbol NVARCHAR(500) '$.currencies[0].symbol'                               
      );
      
    ALTER TABLE currencies ALTER COLUMN alpha2Code NVARCHAR(500) NOT NULL;    
    ALTER TABLE currencies ADD CONSTRAINT FK FOREIGN KEY (alpha2Code) REFERENCES countries (alpha2Code);
    
    SELECT * INTO primary_languages
    FROM OPENJSON(@json)
      WITH (        
        alpha2Code NVARCHAR(500) '$.alpha2Code',
        iso639_1 NVARCHAR(500) '$.languages[0].iso639_1',
        iso639_2 NVARCHAR(500) '$.languages[0].iso639_2',
        name NVARCHAR(500) '$.languages[0].name',
        nativeName NVARCHAR(500) '$.languages[0].nativeName'                           
      );
      
    ALTER TABLE primary_languages ALTER COLUMN alpha2Code NVARCHAR(500) NOT NULL;    
    ALTER TABLE primary_languages ADD CONSTRAINT FK1 FOREIGN KEY (alpha2Code) REFERENCES countries (alpha2Code);

    SELECT * INTO regionalBlocs
    FROM OPENJSON(@json)
      WITH (        
        alpha2Code NVARCHAR(500) '$.alpha2Code',
        acronym NVARCHAR(500) '$.regionalBlocs[0].acronym',
        name NVARCHAR(500) '$.regionalBlocs[0].name'                           
      );
      
    ALTER TABLE regionalBlocs ALTER COLUMN alpha2Code NVARCHAR(500) NOT NULL;    
    ALTER TABLE regionalBlocs ADD CONSTRAINT FK2 FOREIGN KEY (alpha2Code) REFERENCES countries (alpha2Code);""")

    conn.commit()


if __name__ == '__main__':
    response = requests.get('https://restcountries.eu/rest/v2/all').json()
    print(json.dumps(response, indent=4, sort_keys=True))
    save_to_database(response)
