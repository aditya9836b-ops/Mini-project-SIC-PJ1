import pandas as pd
import numpy as np

def clean_mobile_data(filepath=None):
    """
    Loads and cleans the mobile dataset.
    Handles price strings, storage conversion to GB, missing processors, and numerical formatting.
    """
    if filepath is None:
        import os
        paths = ['../datasets/sic_mobile_spec_PJ1.xlsx', 'data/sic_mobile_spec_PJ1.xlsx']
        filepath = next((p for p in paths if os.path.exists(p)), 'data/sic_mobile_spec_PJ1.xlsx')
        
    df = pd.read_excel(filepath)
    
    # 1. Clean Price: Remove '$', commas, and convert to float
    if not pd.api.types.is_numeric_dtype(df['price']):
        df['price'] = (
            df['price']
            .astype(str)
            .str.replace('$', '', regex=False)
            .str.replace(',', '', regex=False)
            .astype(float)
        )
    else:
        df['price'] = df['price'].astype(float)
        
    # 2. Clean Storage: Convert '256GB', '1TB', etc., to integer GB
    def parse_storage(val):
        if pd.isna(val):
            return 128
        val_str = str(val).upper().strip()
        if 'TB' in val_str:
            try:
                num = float(val_str.replace('TB', '').strip())
                return int(num * 1024)
            except:
                return 1024
        elif 'GB' in val_str:
            try:
                num = float(val_str.replace('GB', '').strip())
                return int(num)
            except:
                return 128
        else:
            try:
                return int(float(val_str))
            except:
                return 128

    df['storage_gb'] = df['storage'].apply(parse_storage)
    
    # 3. Clean Processor & Handle Missing Data
    df['processor'] = df['processor'].fillna('Not Mentioned')
    df['processor_cleaned'] = df['processor'].apply(
        lambda x: 'Not Mentioned' if str(x).lower() in ['not mentioned', 'nan', 'none', ''] else str(x)
    )
    
    # Heuristic processor scoring (tiers are documented in prompts/scoring_template.md).
    # Names in the dataset are squashed (e.g. 'Snapdragon8Gen2Processor') and the
    # dataset spells Helio as 'Heilo', so we lowercase, strip spaces and match both.
    TIERS = [
        (1.0, ['8gen', '8plusgen', 'dimensity9000', 'snapdragon888', 'a16', 'a17', 'tensor']),   # flagship
        (0.8, ['gen8', 'snapdragon750', 'dimensity1080']),                                      # upper mid-range
        (0.6, ['snapdragon720', 'snapdragon695', 'dimensity720', 'dimensity700', 'dimensity800',
               'snapdragon778', 'heilo80', 'helio80', 'heilo806769', 'heilo67653512', 'heilo356765', 'helio356765']),  # mid-range
        (0.4, ['snapdragon450', 'snapdragon425', 'snapdragon410', 'sdm450', 'sdm439',
               'heilo35', 'helio35']),                                                          # entry level
    ]

    def score_processor(proc):
        p = str(proc).lower().replace(' ', '')
        if 'notmentioned' in p:
            return 0.3  # Penalised: missing info must not beat a known chip
        for score, keys in TIERS:
            if any(k in p for k in keys):
                return score
        return 0.5      # Known brand but unrecognised model (e.g. 'MediaTek', 'Snapdragon1P')

    df['processor_score'] = df['processor_cleaned'].apply(score_processor)
    
    return df

if __name__ == "__main__":
    df = clean_mobile_data()
    print("Data cleaning successful!")
    print(f"Total Phones Loaded: {len(df)}")
    print(df[['name', 'price', 'ram', 'storage_gb', 'battery', 'processor_score']].head())