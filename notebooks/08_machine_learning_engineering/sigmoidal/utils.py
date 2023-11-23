import os

import warnings
import zipfile
from calendar import monthrange
from datetime import datetime, timedelta
from io import BytesIO

import pandas as pd
import requests

warnings.filterwarnings('ignore')

from dotenv import load_dotenv

load_dotenv()


"""
Funções básicas
"""


def convert_date_to_unix(x):
    """
    Converte uma data no formato 'YYYY-MM-DD' para um timestamp em milissegundos.

    Args:
        x (str): Data no formato 'YYYY-MM-DD'.

    Returns:
        int: Timestamp em milissegundos.
    """
    dt_obj = datetime.strptime(str(x), '%Y-%m-%d')
    dt_obj = dt_obj.timestamp() * 1000
    return int(dt_obj)


def convert_unix_to_date(x):
    """
    Converte um timestamp em milissegundos para uma data no formato 'YYYY-MM-DD'.

    Args:
        x (int): Timestamp em milissegundos.

    Returns:
        str: Data no formato 'YYYY-MM-DD'.
    """
    x //= 1000
    x = datetime.fromtimestamp(x)
    return datetime.strftime(x, '%Y-%m-%d')


def get_next_date(date):
    """
    Retorna a data seguinte à data fornecida.

    Args:
        date (str): Data no formato 'YYYY-MM-DD'.

    Returns:
        str: Data seguinte no formato 'YYYY-MM-DD'.
    """
    next_date = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
    return datetime.strftime(next_date, '%Y-%m-%d')


def get_last_date_in_fg(fg):
    """
    Retorna a última data em um objeto FeatureGroup.

    Args:
        fg (FeatureGroup): Objeto FeatureGroup.

    Returns:
        str: Última data no formato 'YYYY-MM-DD'.
    """
    for col in fg.statistics.content['columns']:
        if col['column'] == 'timestamp':
            res = col['maximum']
            return convert_unix_to_date(res)


###############################################################################
# Processamento básico de dados


def select_stations_info(df):
    """
    Seleciona as informações das estações a partir de um DataFrame.

    Args:
        df (DataFrame): DataFrame contendo as informações das estações.

    Returns:
        DataFrame: DataFrame contendo as informações selecionadas das estações.
    """
    df_res = df[
        ['start_station_id', 'start_station_name', 'start_lat', 'start_lng']
    ].rename(
        columns={
            'start_station_id': 'station_id',
            'start_station_name': 'station_name',
            'start_lat': 'lat',
            'start_lng': 'long',
        }
    )
    df_res = df_res.drop_duplicates()
    return df_res


def process_df(original_df, month, year):
    """
    Processa um DataFrame contendo dados de viagens.

    Args:
        original_df (DataFrame): DataFrame contendo os dados de viagens.
        month (int): Mês.
        year (int): Ano.

    Returns:
        DataFrame: DataFrame processado.
    """
    df_res = original_df[['started_at', 'start_station_id']]
    df_res.started_at = pd.to_datetime(df_res.started_at)
    df_res.started_at = df_res.started_at.dt.floor('d')
    df_res = (
        df_res.groupby(['started_at', 'start_station_id'])
        .size()
        .reset_index(name='users_count')
    )

    df_res = df_res.rename(
        columns={
            'started_at': 'date',
            'start_station_id': 'station_id',
            0: 'users_count',
        }
    )
    # vamos selecionar apenas as estações populares - uma estação será considerada popular
    # se ela foi utilizada todos os dias durante o mês
    days_in_month = monthrange(int(year), int(month))[1]
    popular_stations = df_res.station_id.value_counts()[
        df_res.station_id.value_counts() == days_in_month
    ].index
    df_res = df_res[df_res.station_id.isin(popular_stations)]
    return df_res.sort_values(by=['date', 'station_id'])


def update_month_data(main_df, month, year):
    """
    Atualiza os dados do DataFrame principal com os dados de um determinado mês e ano.

    Args:
        main_df (DataFrame): DataFrame principal.
        month (int): Mês.
        year (int): Ano.

    Returns:
        DataFrame: DataFrame atualizado.
    """
    if month < 10:
        month = f'0{month}'
    print(f'_____ Processando {month}/{year}... _____')

    if f'{year}{month}' in ['202206', '202207']:
        citibike = 'citbike'
    else:
        citibike = 'citibike'
    url = f'https://s3.amazonaws.com/tripdata/{year}{month}-{citibike}-tripdata.csv.zip'
    print(url)
    filename = 'data/' + url.split('/')[-1].split('.')[0] + '.csv'
    fn_list = filename.split('.')
    processed_filename = fn_list[-2] + '_processed.' + fn_list[-1]

    if os.path.isfile(processed_filename):
        print('Recuperando DataFrame do arquivo csv existente...💿')
        return pd.concat([pd.read_csv(processed_filename), main_df])

    print('Download iniciado...⏳')

    req = requests.get(url)

    print('Download concluído!👌')

    file = zipfile.ZipFile(BytesIO(req.content))

    file.extractall('data/')

    print('Recuperando DataFrame do arquivo csv...💿')
    print('-' * 32)

    original_df = pd.read_csv(filename)

    if not os.path.isfile('data/stations_info.csv'):
        stations_info_df = select_stations_info(original_df)
    else:
        present_stations_df = pd.read_csv('data/stations_info.csv')
        stations_info_batch = select_stations_info(original_df)
        stations_info_df = pd.concat(
            [present_stations_df, stations_info_batch]
        ).reset_index(drop=True)
    stations_info_df.to_csv('data/stations_info.csv', index=False)

    processed_df = process_df(original_df, month, year)

    # deletar o arquivo grande não processado original
    os.remove(filename)

    # salvar o arquivo processado em csv
    processed_df.to_csv(processed_filename, index=False)

    return pd.concat([processed_df, main_df])


def get_citibike_data(
    start_date='01/2023', end_date='09/2023'
) -> pd.DataFrame:
    """
    Obtém os dados do Citibike em um intervalo de datas.

    Args:
        start_date (str): Data de início no formato 'MM/YYYY'.
        end_date (str): Data de término no formato 'MM/YYYY'.

    Returns:
        DataFrame: DataFrame contendo os dados do Citibike.
    """
    start_month, start_year = (
        start_date.split('/')[0],
        start_date.split('/')[1],
    )
    end_month, end_year = end_date.split('/')[0], end_date.split('/')[1]

    df_res = pd.DataFrame(columns=['date', 'station_id', 'users_count'])

    if start_year == end_year:
        for month in range(int(start_month), int(end_month) + 1):
            df_res = update_month_data(df_res, month, start_year)

    else:
        for month in range(int(start_month), 12 + 1):
            df_res = update_month_data(df_res, month, start_year)
        for month in range(1, int(end_month) + 1):
            df_res = update_month_data(df_res, month, end_year)

    df_res['users_count'] = df_res['users_count'].astype(int)

    print('\n✅ Concluído ✅')

    return df_res.reset_index(drop=True)


def moving_average(df, window=7):
    """
    Calcula a média móvel de uma coluna em um DataFrame.

    Args:
        df (DataFrame): DataFrame contendo os dados.
        window (int): Tamanho da janela da média móvel.

    Returns:
        DataFrame: DataFrame com a coluna da média móvel adicionada.
    """
    df[f'mean_{window}_days'] = (
        df.groupby('station_id')['users_count']
        .rolling(window=window)
        .mean()
        .reset_index(0, drop=True)
        .shift(1)
    )
    return df


def moving_std(df, window):
    """
    Calcula o desvio padrão móvel de uma coluna em um DataFrame.

    Args:
        df (DataFrame): DataFrame contendo os dados.
        window (int): Tamanho da janela do desvio padrão móvel.

    Returns:
        DataFrame: DataFrame com a coluna do desvio padrão móvel adicionada.
    """
    df[f'std_{window}_days'] = (
        df.groupby('station_id')['users_count']
        .rolling(window=window)
        .std()
        .reset_index(0, drop=True)
        .shift(1)
    )
    return df


def exponential_moving_average(df, window):
    """
    Calcula a média móvel exponencial de uma coluna em um DataFrame.

    Args:
        df (DataFrame): DataFrame contendo os dados.
        window (int): Tamanho da janela da média móvel exponencial.

    Returns:
        DataFrame: DataFrame com a coluna da média móvel exponencial adicionada.
    """
    df[f'exp_mean_{window}_days'] = (
        df.groupby('station_id')['users_count']
        .ewm(span=window)
        .mean()
        .reset_index(0, drop=True)
        .shift(1)
    )
    return df


def exponential_moving_std(df, window):
    """
    Calcula o desvio padrão móvel exponencial de uma coluna em um DataFrame.

    Args:
        df (DataFrame): DataFrame contendo os dados.
        window (int): Tamanho da janela do desvio padrão móvel exponencial.

    Returns:
        DataFrame: DataFrame com a coluna do desvio padrão móvel exponencial adicionada.
    """
    df[f'exp_std_{window}_days'] = (
        df.groupby('station_id')['users_count']
        .ewm(span=window)
        .std()
        .reset_index(0, drop=True)
        .shift(1)
    )
    return df


def engineer_citibike_features(df):
    """
    Realiza a engenharia de features nos dados do Citibike.

    Args:
        df (DataFrame): DataFrame contendo os dados do Citibike.

    Returns:
        DataFrame: DataFrame com as features engenheiradas.
    """
    df_res = df.copy()
    # existem linhas duplicadas (vários registros para o mesmo dia e estação). vamos removê-las.
    df_res = df_res.groupby(['date', 'station_id'], as_index=False)[
        'users_count'
    ].sum()

    df_res['prev_users_count'] = df_res.groupby('station_id')[
        'users_count'
    ].shift(+1)
    df_res = df_res.dropna()
    df_res = moving_average(df_res, 7)
    df_res = moving_average(df_res, 14)

    for i in [7, 14]:
        for func in [
            moving_std,
            exponential_moving_average,
            exponential_moving_std,
        ]:
            df_res = func(df_res, i)
    df_res = df_res.reset_index(drop=True)
    return df_res.sort_values(by=['date', 'station_id']).dropna()
