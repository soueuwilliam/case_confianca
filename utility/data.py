import pandas as pd

class Data:
    
    def __init__(self, conexao):
        self.conexao = conexao
        
    def tratamento_fato_stocks(self, df: pd.DataFrame) -> pd.DataFrame:
        dim_data = pd.read_sql('select id_data, data from dim_data',con=self.conexao)
        dim_data['data'] = pd.to_datetime(dim_data['data'])
        df['Date'] = pd.to_datetime(df['Date'])
        df_final = df.merge(dim_data, how='left', left_on='Date',right_on='data').drop(columns=['data', 'Date'])


        dim_stock = pd.read_sql('select id_stocks, symbol from dim_stocks',con=self.conexao)
        df_final = df_final.merge(dim_stock, how='left', left_on='Ticker',right_on='symbol').drop(columns=['symbol','Ticker'])
        colunas_reordenadas = ['id_stocks', 'id_data', 'Open', 'High', 'Low', 'Close', 'Volume']
        df_final = df_final[colunas_reordenadas]
        return df_final
    
    def tratamento_dim_stocks(self, df: pd.DataFrame) -> pd.DataFrame:
        colunas = [
        'symbol', 'shortName', 'longName', 'address1', 'address2', 'city', 'state', 'zip',
        'country', 'phone', 'website', 'industry', 'industryKey', 'industryDisp',
        'sector', 'sectorKey', 'sectorDisp', 'currency', 'exchange', 'fullExchangeName',
        'region',
        ]
        df_final = pd.DataFrame(columns=colunas)

        # Criando o DataFrame vazio com essas colunas
        df_final = df.reindex(columns=colunas, fill_value=None)
        df_final = df_final.rename(columns={
                'shortName': 'short_name',
                'longName': 'long_name',
                'address1': 'address_1',
                'address2': 'address_2',
                'industryKey': 'industry_key',
                'industryDisp': 'industry_disp',
                'sectorKey': 'sector_key',
                'sectorDisp': 'sector_disp',
                'fullExchangeName': 'full_exchange_name',
                'exchange': 'exchange',
                'zip': 'zip'
                })
        
        return df_final
    
    def sobe_dados_banco(self, df: pd.DataFrame, nome_tabela: str, tipo: str) -> None:
        df.to_sql(name=nome_tabela, if_exists=tipo, index=False, con=self.conexao)
        