# Libs nativas
import sqlite3

class Models:
    
    def __init__(self):
        self.conexao = sqlite3.connect("db.sqlite3")
        self.cursor = self.conexao.cursor()

    def criacao_tabelas(self) -> None:
                
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dim_data (
                id_data INTEGER PRIMARY KEY,
                data TEXT,
                dia INTEGER,
                mes INTEGER,
                ano INTEGER,
                mesano TEXT,
                dia_semana INTEGER,
                nome_dia_semana TEXT,
                semana_ano INTEGER,
                bimestre INTEGER,
                trimestre INTEGER,
                quadrimestre INTEGER,
                semestre INTEGER,
                feriado INTEGER,
                periodo_feriado TEXT,
                periodo_sazonal TEXT,
                nome_mes TEXT,
                id_feriado INTEGER
            )
        ''')

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_stocks (
                id_stocks INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                short_name TEXT,
                long_name TEXT,
                address_1 TEXT,
                address_2 TEXT,
                city TEXT,
                state TEXT,
                zip TEXT,
                country TEXT,
                phone TEXT,
                website TEXT,
                industry TEXT,
                industry_key TEXT,
                industry_disp TEXT,
                sector TEXT,
                sector_key TEXT,
                sector_disp TEXT,
                currency TEXT,
                exchange TEXT,
                full_exchange_name TEXT,
                region TEXT
            )
            """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fato_stocks (
                id_data INTEGER,
                id_stocks INTEGER,
                close REAL,
                high REAL,
                low REAL,
                open REAL,
                volume INTEGER,
                ticker TEXT
            )
            """)
        
        self.conexao.commit()   
    