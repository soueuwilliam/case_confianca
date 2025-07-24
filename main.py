# Libs internas
import os

# Libs externas
import pandas as pd

# Libs internos do app
from utility.models import Models
from utility.data import Data
from utility.rpa import Rpa

# Instâncias das classes
py_models =  Models()
py_dados = Data(py_models.conexao)
py_rpa = Rpa()

# Criando as tabelas no banco SQLite3
py_models.criacao_tabelas()

# ----------------------------------------[POPULANDO TABELAS]-----------------------------------------

## ---------------------------------------------[DIM DATA]---------------------------------------------

df_data = pd.read_excel(os.path.join("./data", "dim_data.xlsx"))
py_dados.sobe_dados_banco(df=df_data, nome_tabela='dim_data', tipo="replace")

## --------------------------------------------[DIM STOCKS]--------------------------------------------

df_final_1 = pd.DataFrame()
for stock in ["ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "SANB11.SA", "BPAC11.SA"]:
    df_temp = py_rpa.get_info_stock(ticker=stock)
    df_final_1 = pd.concat([df_final_1, df_temp], ignore_index=True)
    
df_1 = py_dados.tratamento_dim_stocks(df=df_final_1)
py_dados.sobe_dados_banco(df=df_1, nome_tabela='dim_stocks', tipo="append")

## --------------------------------------------[FATO STOCKS]--------------------------------------------

df_final_2 = pd.DataFrame()
for stock in ["ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "SANB11.SA", "BPAC11.SA"]:
    df_temp = py_rpa.get_popula_fato(ticker=stock)
    df_final_2 = pd.concat([df_final_2, df_temp])
    

df_2 = py_dados.tratamento_fato_stocks(df=df_final_2)   
py_dados.sobe_dados_banco(df=df_2, nome_tabela='fato_stocks', tipo="append")


## --------------------------------------------[FATO STOCKS - Diario ]--------------------------------------------

df_final_3 = pd.DataFrame()
for stock in ["ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "SANB11.SA", "BPAC11.SA"]:
    df_temp = py_rpa.get_data_ticker(ticker=stock)
    df_final_2 = pd.concat([df_final_3, df_temp])

df_3 = py_dados.tratamento_fato_stocks(df=df_final_3)   
py_dados.sobe_dados_banco(df=df_3, nome_tabela='fato_stocks', tipo="append")

