"""
Seeds the database from the Kaggle dataset:
  https://www.kaggle.com/datasets/jockeroika/cars-dataset

Kaggle credentials are required. Add to .env:
  KAGGLE_API_TOKEN=your_token

Get your API key from: https://www.kaggle.com/settings -> API -> Create New Token
"""

import os
import shutil
from dotenv import load_dotenv

load_dotenv()  # Must be before kaggle import so the token is in the environment

import kaggle
import pandas as pd
from database import Session
from models import CarModel, Trim, Price, Sales, Advertisement


DATASET_SLUG = 'jockeroika/cars-dataset'
DATA_DIR = 'data/'


def download_dataset():
    print('  Downloading dataset from Kaggle...')
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(DATASET_SLUG, path=DATA_DIR, unzip=True)
    print('  Download complete.')


def seed_car_models(session):
    df = pd.read_csv(f'{DATA_DIR}Basic_table.csv')
    records = [
        {'model_id': row['Genmodel_ID'], 'brand_name': row['Automaker'], 'model_name': row['Genmodel']}
        for _, row in df.iterrows()
    ]
    session.bulk_insert_mappings(CarModel, records)
    session.commit()
    print(f'  Seeded {len(records)} car models')


def seed_trims(session):
    df = pd.read_csv(f'{DATA_DIR}Trim_table.csv')
    records = [
        {
            'model_id': row['Genmodel_ID'],
            'trim_name': row['Trim'],
            'year': row['Year'],
            'engine_type': row['Fuel_type'],
            'engine_size': row['Engine_size'],
            'selling_price': row['Price'],
        }
        for _, row in df.iterrows()
    ]
    session.bulk_insert_mappings(Trim, records)
    session.commit()
    print(f'  Seeded {len(records)} trims')


def seed_prices(session):
    df = pd.read_csv(f'{DATA_DIR}Price_table.csv')
    records = [
        {'model_id': row['Genmodel_ID'], 'year': row['Year'], 'entry_level_price': row['Entry_price']}
        for _, row in df.iterrows()
    ]
    session.bulk_insert_mappings(Price, records)
    session.commit()
    print(f'  Seeded {len(records)} prices')


def seed_sales(session):
    df = pd.read_csv(f'{DATA_DIR}Sales_table.csv')

    # Sales CSV is wide-format: one column per year (2001-2020)
    # Melt it into rows of (model_id, year, units_sold)
    year_columns = [col for col in df.columns if col.isdigit()]
    melted = df.melt(id_vars=['Genmodel_ID'], value_vars=year_columns, var_name='year', value_name='units_sold')
    melted = melted.dropna(subset=['units_sold'])

    records = [
        {'model_id': row['Genmodel_ID'], 'year': int(row['year']), 'units_sold': int(row['units_sold']), 'region': 'UK'}
        for _, row in melted.iterrows()
    ]
    session.bulk_insert_mappings(Sales, records)
    session.commit()
    print(f'  Seeded {len(records)} sales records')


def seed_advertisements(session):
    df = pd.read_csv(f'{DATA_DIR}Ad_table (extra).csv')
    df.columns = df.columns.str.strip()  # remove any leading/trailing spaces from column names

    records = []
    for _, row in df.iterrows():
        records.append({
            'ad_id': row['Adv_ID'],
            'model_id': row['Genmodel_ID'],
            'ad_year': row['Adv_year'],
            'ad_month': row['Adv_month'],
            'color': row['Color'],
            'reg_year': row['Reg_year'],
            'body_type': row['Bodytype'],
            'mileage': row['Runned_Miles'],
            'engine_size': row['Engin_size'],
            'gearbox': row['Gearbox'],
            'fuel_type': row['Fuel_type'],
            'price': row['Price'],
            'engine_power': row['Engine_power'] if pd.notna(row['Engine_power']) else None,
        })

    session.bulk_insert_mappings(Advertisement, records)
    session.commit()
    print(f'  Seeded {len(records)} advertisements')


def run(cleanup_after=True):
    download_dataset()

    session = Session()
    try:
        print('Seeding tables...')
        # Order matters — parent rows must exist before child rows referencing them
        seed_car_models(session)
        seed_trims(session)
        seed_prices(session)
        seed_sales(session)
        seed_advertisements(session)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    if cleanup_after:
        shutil.rmtree(DATA_DIR)
        print(f'  Cleaned up {DATA_DIR}')
