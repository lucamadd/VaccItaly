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

CREATE TABLE db_vaccini(
    nome_regione VARCHAR(100) NOT NULL,
    num_vaccini INTEGER NOT NULL,
    CONSTRAINT PRIMARY KEY(nome_regione)
)