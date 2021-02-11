--------------------------------------- metadata

CREATE TABLE db_utente(
    cod_fis VARCHAR(50) NOT NULL,
    email VARCHAR(500) NOT NULL,
    nome VARCHAR(500) NOT NULL,
    cognome VARCHAR(500) NOT NULL,
    data_nascita DATE NOT NULL,
    luogo_nascita VARCHAR(500) NOT NULL,
    password VARCHAR(40) NOT NULL,
    CONSTRAINT PRIMARY KEY(cod_fis, email)
)

CREATE TABLE db_regione(
    nome_regione VARCHAR(100) NOT NULL,
    num_vaccini INTEGER NOT NULL,
    CONSTRAINT PRIMARY KEY(nome_regione)
)

CREATE TABLE db_asl(
    nome_asl VARCHAR(200) NOT NULL,
    regione VARCHAR(100) NOT NULL,
    CONSTRAINT PRIMARY KEY(nome_asl),
    CONSTRAINT FOREIGN KEY(regione) REFERENCES db_regione(nome_regione)
)

CREATE TABLE db_amministratori(
    id_amministratore VARCHAR(500) NOT NULL,
    regione VARCHAR(100) NOT NULL,
    asl VARCHAR(200) NOT NULL,
    nome VARCHAR(500) DEFAULT '',
    cognome VARCHAR(500) DEFAULT '',
    password VARCHAR(40) NOT NULL,
    CONSTRAINT PRIMARY KEY(id_amministratore),
    CONSTRAINT FOREIGN KEY(regione) REFERENCES db_regione(nome_regione),
    CONSTRAINT FOREIGN KEY(asl) REFERENCES db_asl(nome_asl)
)

CREATE TABLE db_prenotazione(
    cod_fis VARCHAR(50) NOT NULL,
    email VARCHAR(500) NOT NULL,
    regione VARCHAR(100) NOT NULL,
    asl VARCHAR(200) NOT NULL,
    data_prenotazione DATE NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT PRIMARY KEY(cod_fis, email, asl, data_prenotazione),
    CONSTRAINT FOREIGN KEY(cod_fis, email) REFERENCES db_utente(cod_fis, email),
    CONSTRAINT FOREIGN KEY(regione) REFERENCES db_regione(nome_regione),
    CONSTRAINT FOREIGN KEY(asl) REFERENCES db_asl(nome_asl)
)

----update to do
UPDATE db_regione
SET num_vaccini = num_vaccini + 20
WHERE nome_regione = 'Lazio';

----similtrigger
UPDATE db_regione
SET num_vaccini = (SELECT sum(num_vaccini)
				  FROM (SELECT * FROM db_regione) AS db_reg
                  WHERE nome_regione <> 'Italia')
WHERE nome_regione = 'Italia';

--------------------------------------- default data

INSERT INTO db_regione VALUES
    ("Italia",0),
    ("Abruzzo", 0),
    ("Basilicata",0),
    ("Calabria",0),
    ("Campania",0),
    ("Emilia Romagna",0),
    ("Friuli Venezia Giulia",0),
    ("Lazio",0),
    ("Liguria",0),
    ("Lombardia",0),
    ("Marche",0),
    ("Molise",0),
    ("Prov. Auton. Bolzano",0),
    ("Prov. Auton. Trento",0),
    ("Piemonte",0),
    ("Puglia",0),
    ("Sardegna",0),
    ("Sicilia",0),
    ("Toscana",0),
    ("Umbria",0),
    ("Valle D'Aosta",0),
    ("Veneto",0)

INSERT INTO db_asl VALUES
    ('To3','Piemonte'),
    ('To4','Piemonte'),
    ('To5','Piemonte'),
    ('Vc','Piemonte'),
    ('Bi','Piemonte'),
    ('No','Piemonte'),
    ('Vco','Piemonte'),
    ('Cn1','Piemonte'),
    ('Cn2','Piemonte'),
    ('At','Piemonte'),
    ('Al','Piemonte'),
    ('Asl Citta'' Di Torino','Piemonte'),
    ('Azienda U.S.L. Valle D''Aosta','Valle D''Aosta'),
    ('Ats Della Citta'' Metropolitana Di Milano','Lombardia'),
    ('Ats Dell''Insubria','Lombardia'),
    ('Ats Della Montagna','Lombardia'),
    ('Ats Della Brianza','Lombardia'),
    ('Ats Di Bergamo','Lombardia'),
    ('Ats Di Brescia','Lombardia'),
    ('Ats Della Val Padana','Lombardia'),
    ('Ats Di Pavia','Lombardia'),
    ('Azienda Sanitaria Della P.A. Di Bolzano','Prov. Auton. Bolzano'),
    ('Trento','Prov. Auton. Trento'),
    ('Azienda Ulss N. 1 Dolomiti','Veneto'),
    ('Azienda Ulss N. 2 Marca Trevigiana','Veneto'),
    ('Azienda Ulss N. 3 Serenissima','Veneto'),
    ('Azienda Ulss N. 4 Veneto Orientale','Veneto'),
    ('Azienda Ulss N. 5 Polesana','Veneto'),
    ('Azienda Ulss N. 6 Euganea','Veneto'),
    ('Azienda Ulss N. 7 Pedemontana','Veneto'),
    ('Azienda Ulss N. 8 Berica','Veneto'),
    ('Azienda Ulss N. 9 Scaligera','Veneto'),
    ('Asui Di Trieste','Friuli Venezia Giulia'),
    ('Bassa Friulana - Isontina','Friuli Venezia Giulia'),
    ('Alto Friuli - Collinare - Medio Friuli','Friuli Venezia Giulia'),
    ('Asui Di Udine','Friuli Venezia Giulia'),
    ('Friuli Occidentale','Friuli Venezia Giulia'),
    ('Imperiese','Liguria'),
    ('Savonese','Liguria'),
    ('Genovese','Liguria'),
    ('Chiavarese','Liguria'),
    ('Spezzino','Liguria'),
    ('Azienda Usl Piacenza','Emilia Romagna'),
    ('Azienda Usl Parma','Emilia Romagna'),
    ('Azienda Usl Reggio Emilia','Emilia Romagna'),
    ('Azienda Usl Modena','Emilia Romagna'),
    ('Azienda Usl Bologna','Emilia Romagna'),
    ('Azienda Usl Imola','Emilia Romagna'),
    ('Azienda Usl Ferrara','Emilia Romagna'),
    ('Azienda Usl Della Romagna','Emilia Romagna'),
    ('Azienda Usl Toscana Centro','Toscana'),
    ('Azienda Usl Toscana Nord-Ovest','Toscana'),
    ('Azienda Usl Toscana Sud-Est','Toscana'),
    ('Ausl Umbria N. 1','Umbria'),
    ('Ausl Umbria N. 2','Umbria'),
    ('Asur','Marche'),
    ('Viterbo','Lazio'),
    ('Rieti','Lazio'),
    ('Latina','Lazio'),
    ('Frosinone','Lazio'),
    ('Roma 1','Lazio'),
    ('Roma 2','Lazio'),
    ('Roma 3','Lazio'),
    ('Roma 4','Lazio'),
    ('Roma 5','Lazio'),
    ('Roma 6','Lazio'),
    ('Avezzano-Sulmona-L''Aquila','Abruzzo'),
    ('Lanciano-Vasto-Chieti','Abruzzo'),
    ('Pescara','Abruzzo'),
    ('Teramo','Abruzzo'),
    ('Asrem','Molise'),
    ('A.S.L. Avellino','Campania'),
    ('A.S.L. Benevento','Campania'),
    ('A.S.L. Caserta','Campania'),
    ('A.S.L. Napoli 1 Centro','Campania'),
    ('A.S.L. Napoli 2 Nord','Campania'),
    ('A.S.L. Napoli 3 Sud','Campania'),
    ('A.S.L. Salerno','Campania'),
    ('Asl Br','Puglia'),
    ('Asl Ta','Puglia'),
    ('Asl Bt','Puglia'),
    ('Asl Ba','Puglia'),
    ('Asl Fg','Puglia'),
    ('Asl Le','Puglia'),
    ('Azienda Sanitaria Locale Di Potenza Asp','Basilicata'),
    ('Azienda Sanitaria Locale Di Matera  Asm','Basilicata'),
    ('A.S.P. Cosenza','Calabria'),
    ('A.S.P. Crotone','Calabria'),
    ('A.S.P. Catanzaro','Calabria'),
    ('A.S.P. Vibo Valentia','Calabria'),
    ('A.S.P. Reggio Calabria','Calabria'),
    ('Asp Agrigento','Sicilia'),
    ('Asp Caltanissetta','Sicilia'),
    ('Asp Catania','Sicilia'),
    ('Asp Enna','Sicilia'),
    ('Asp Messina','Sicilia'),
    ('Asp Palermo','Sicilia'),
    ('Asp Ragusa','Sicilia'),
    ('Asp Siracusa','Sicilia'),
    ('Asp Di Trapani','Sicilia'),
    ('Azienda Per La Tutela Della Salute','Sardegna')

INSERT INTO db_utente VALUES
    ('global_admin','admin@admin.com',
    'Amministratore','VaccItaly',
    STR_TO_DATE('19/05/1996','%d/%m/%Y'),
    'VaccItaly','c4a42607d8690946a9b740dd9d875ec84d0d8fab')
