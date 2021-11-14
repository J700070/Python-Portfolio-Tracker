
import numpy as np


def parseDegiro(df):

    # Remove Columns
    df.drop(['Unnamed: 8', 'Unnamed: 12', 'Unnamed: 15'], axis=1, inplace=True)

    # Rename Columns
    df.rename(
        columns={"Unnamed: 10": "Moneda Local"}, inplace=True)
    df.rename(
        columns={"Unnamed: 17": "Moneda"}, inplace=True)

    # Fix empty values
    df.dropna(subset=['Fecha'], inplace=True)
    df["Centro de ejecución"].replace(np.nan, "Desconocido", inplace=True)
    df["Costes de transacción"].replace(np.nan, 0, inplace=True)
    df["ID Orden"].replace(np.nan, "Desconocido", inplace=True)

    return df
