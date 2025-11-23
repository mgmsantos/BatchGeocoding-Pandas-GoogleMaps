# Python Geocoding Engine: Solução com Pandas & Google Maps API

---

## Visão Geral do Projeto

Este projeto consiste em uma solução robusta em **Python** para realizar a **geocodificação em lote (batch geocoding)** de endereços, nomes de locais e pontos de interesse, convertendo-os em coordenadas geográficas **(Latitude e Longitude)**.

O código é tecnicamente versátil, sendo aplicável a qualquer setor que trabalhe com grandes bases de dados geográficos e necessite de precisão na localização.

### Funcionalidades Chave:

* **API Geocoding:** Utilização do cliente `googlemaps` para consultas eficientes.
* **Integração Pandas:** Aplicação direta da função em `DataFrames` do Pandas para processamento em lote.
* **Robustez:** Implementação de `try/except Exception as e` para gerenciamento de falhas de API (limites de uso, erros de rede, etc.).

---

## 🛠️ Stack Técnico e Configuração

### Requisitos

| Componente | Função |
| :--- | :--- |
| **Linguagem:** | Python 3.x |
| **Bibliotecas:** | `googlemaps`, `pandas` |
| **API:** | Google Maps Geocoding API |



```python
# ----------------------------------------------------------------------
# 1. IMPORTAÇÃO DAS BIBLIOTÉCAS NECESSÁRIAS
# ----------------------------------------------------------------------

import os
import googlemaps
import pandas as pd
import numpy as np # Adicionado para uso em um DataFrame de exemplo

# ----------------------------------------------------------------------
# 2. CONFIGURAÇÃO DO CLIENTE GOOGLE MAPS
# ----------------------------------------------------------------------

# A chave deve ser definida como uma variável de ambiente (ex: export CHAVE_API_GOOGLE="SUA_CHAVE")
CHAVE_API_GOOGLE = os.environ.get("CHAVE_API_GOOGLE") 
gmaps = None

try:
    if CHAVE_API_GOOGLE:
        # Tenta iniciar o cliente da API
        gmaps = googlemaps.Client(key=CHAVE_API_GOOGLE)
        print("Cliente Google Maps inicializado com sucesso.")
    else:
        print("AVISO: A variável de ambiente CHAVE_API_GOOGLE não foi definida.")
except Exception as e:
    # Captura e exibe qualquer erro de inicialização
    print(f"ERRO CRÍTICO ao iniciar o cliente Google Maps: {e}")
    gmaps = None

# ----------------------------------------------------------------------
# 3. FUNÇÃO DE GEOCODIFICAÇÃO
# ----------------------------------------------------------------------

def get_coordenadas_google(query_completa):
    """
    Converte um endereço de texto em coordenadas geográficas (Lat/Lon) usando 
    a API do Google Maps.
    
    Args:
        query_completa (str): O endereço ou nome do local a ser geocodificado.
        
    Returns:
        pd.Series: Uma série do Pandas contendo [latitude, longitude].
                   Retorna [None, None] em caso de falha.
    """
    
    # Se o cliente não foi inicializado (gmaps é None), não prossegue
    if gmaps is None: 
        return pd.Series([None, None])
        
    try:
        # Realiza a chamada à API
        geocode_result = gmaps.geocode(query_completa)
        
        if geocode_result:
            # Extrai as coordenadas do primeiro resultado
            lat = geocode_result[0]['geometry']['location']['lat']
            lon = geocode_result[0]['geometry']['location']['lng']
            return pd.Series([lat, lon])
        else:
            # Retorna None se a API não encontrar o endereço
            print(f"AVISO: Endereço não encontrado pela API. Query: {query_completa}")
            return pd.Series([None, None]) 
            
    except Exception as e:
        # Trata erros inesperados da API (limite de uso, rede, etc.)
        print(f"ERRO na API: {e} | Query: {query_completa}")
        return pd.Series([None, None])

# ----------------------------------------------------------------------
# 4. EXEMPLO DE APLICAÇÃO EM DATAFRAME
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Cria um DataFrame de exemplo com endereços
    data = {
        'ID_Fazenda': [101, 102, 103, 104, 105],
        'ENDERECO_FULL': [
            'Fazenda São João, zona rural de Uberaba, MG, Brasil', 
            'Rua da Agricultura, 1200, Campinas, SP, Brasil', 
            'Endereço Inexistente XYZ', # Simula um endereço que falhará
            'Granja Modelo, Toledo, PR, Brasil',
            'Rua XV de Novembro, 10, Curitiba, PR'
        ],
        'Produtividade': [95.5, 88.0, 72.3, 91.2, 85.0]
    }
    df = pd.DataFrame(data)

    print("\nDataFrame Original:")
    print(df)
    print("-" * 50)

    # Aplica a função de geocodificação na coluna 'ENDERECO_FULL'
    # e cria duas novas colunas ('latitude' e 'longitude')
    df[["latitude", "longitude"]] = df['ENDERECO_FULL'].apply(get_coordenadas_google)

    df_coord = df.copy()

    print("\nDataFrame Após Geocodificação:")
    print(df_coord)
    print("\nProcesso concluído.")
```
