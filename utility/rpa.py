# Libs nativas
from datetime import datetime as dt

# Libs externas
import pandas as pd 
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

import yfinance as yf


class Rpa:
    
    def __init__(self, data_inicio = None, data_fim = None):
        self.data_inicio = dt.now().date() if data_inicio == None else data_inicio
        self.data_fim = dt.now().date() if data_fim == None else data_fim
    
    def get_data_ticker(self, ticker: str) -> pd.DataFrame:
        try:
            try:
                service = Service()  
                options = Options()
                options.add_argument('--ignore-certificate-errors')  
                options.add_argument('--start-maximized')           
                options.set_preference("dom.webnotifications.enabled", False)
                driver = webdriver.Firefox(service=service, options=options)
                
                url_base = f'https://finance.yahoo.com/quote/{ticker}/history/'
                
                driver.maximize_window()
                driver.get(url_base)
                tabela = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/section/section/section/article/div[1]/div[3]/table'))
                )
                print("Tabela carregada com sucesso!")
                
                try:
                    # Extrair nomes das colunas
                    colunas_th = tabela.find_elements(By.CSS_SELECTOR, 'thead th')
                    cabecalhos = [coluna.text for  coluna in colunas_th]
                    # Extrair primeira linha de dados (após cabeçalho)
                    primeira_linha = tabela.find_element(By.CSS_SELECTOR, 'tbody tr')
                    celulas = primeira_linha.find_elements(By.TAG_NAME, 'td')
                    dados_linha = [celula.text for celula in celulas]
                    
                    df = pd.DataFrame([dados_linha], columns=cabecalhos)
                    df['Ticker'] = ticker
                    return df
                except Exception as e:
                    print("Erro ao processar a linha da tabela: ")
            
            except Exception as e:
                print("Erro ao carregar a tabela:", e)

        except:
            df = yf.download(ticker)
            df['Ticker'] = ticker
            df.columns = df.columns.get_level_values(0)
            df = df.reset_index()
            df.columns.name = None
            return df
    
    
    def get_info_stock(self, ticker: str) -> pd.DataFrame:
        df_info_ticker = pd.DataFrame([yf.Ticker(ticker).info])
        return df_info_ticker
    
    def get_popula_fato(self, ticker: str) -> pd.DataFrame:
        df = yf.download([ticker], period="10y")
        df.insert(0,'Ticker',ticker)
        df.columns = df.columns.get_level_values(0)
        df = df.reset_index()
        df.columns.name = None
        
        return df
    
    
