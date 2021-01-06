import ast
import pyodbc
from instagram_private_api import Client, ClientCompatPatch
import json

user_name = 'user27101992'
password = 'Mff@95517553'
api = Client(user_name, password, auto_patch=True)

print("connexion succes")

results = api.feed_timeline()
print(json.dumps(results, indent=4, sort_keys=True))

with open('Nouveau document texte.json', 'w') as jsonFile:
    json.dump(results, jsonFile)

conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=DESKTOP-DQHM2SB;'
                      'DATABASE=Api-Instagram;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

cursor.execute("""DECLARE @json NVARCHAR(MAX); SET @json = (SELECT  * FROM OPENROWSET 
(BULK 'C:\\Users\\Bensammar\\PycharmProjects\\pythonProject7\\Nouveau document texte.json',SINGLE_CLOB) AS json);

IF OBJECT_ID('dbo.user_actualite') IS NOT NULL
  DROP TABLE dbo.user_actualite;
  
    
SELECT * INTO user_actualite
FROM OPENJSON(@json,'$.feed_items')
  WITH (
    id_publication NVARCHAR(Max) '$.media_or_ad.id',
	media_type NVARCHAR(500) '$.media_or_ad.type',
    locations NVARCHAR(500) '$.media_or_ad.location.name',
	username NVARCHAR(500) '$.media_or_ad.user.username',
	id_user NVARCHAR(500) '$.media_or_ad.user.id',
	lien_publication NVARCHAR(500) '$.media_or_ad.link',
	comment_count NVARCHAR(500) '$.media_or_ad.comments.count',
	text_de_publication NVARCHAR(500) '$.media_or_ad.caption.text',
	Likes_nombre NVARCHAR(500) '$.media_or_ad.likes.count'
  );
  
    ALTER TABLE user_actualite ALTER COLUMN id_publication NVARCHAR(500) NOT NULL;    
    ALTER TABLE user_actualite ADD PRIMARY KEY (id_publication);
  
  """)

conn.commit()
