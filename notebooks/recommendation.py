import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from data_cleaning import clean_mobile_data

# Define persona weights (all weights add up to exactly 1.0 / 100%)
PERSONA_WEIGHTS = {
    'Student': {
        'price': 0.40,
        'battery': 0.25,
        'ram': 0.15,
        'storage_gb': 0.10,
        'processor_score': 0.10
    },
    'Gamer': {
        'price': 0.05,
        'battery': 0.20,
        'ram': 0.30,
        'storage_gb': 0.10,
        'processor_score': 0.35
    },
    'Content Creator': {
        'price': 0.05,
        'battery': 0.05,
        'ram': 0.15,
        'storage_gb': 0.20,
        'camera': 0.40,
        'processor_score': 0.15
    },
    'Business Professional': {
        'price': 0.10,
        'battery': 0.30,
        'ram': 0.20,
        'storage_gb': 0.10,
        'processor_score': 0.30
    },
    'Senior Citizen': {
        'price': 0.40,
        'battery': 0.30,
        'ram': 0.15,
        'storage_gb': 0.10,
        'processor_score': 0.05
    }
}

def get_recommendations(df, persona, max_budget=2000, min_ram=0, min_storage=0):
    """
    Filters phones by budget, RAM, and storage, normalizes features via Min-Max scaling,
    applies inverted pricing, computes weighted scores, and returns top 5 recommendations.
    """
    # 1. Filter dataset
    filtered = df[
        (df['price'] <= max_budget) &
        (df['ram'] >= min_ram) &
        (df['storage_gb'] >= min_storage)
    ].copy()
    
    if filtered.empty:
        return pd.DataFrame()
        
    # 2. Get weights for the selected persona
    weights = PERSONA_WEIGHTS.get(persona, PERSONA_WEIGHTS['Student'])
    features = list(weights.keys())
    
    # Ensure all required feature columns exist in filtered df
    for feat in features:
        if feat not in filtered.columns:
            filtered[feat] = 0.0
            
    # 3. Min-Max Scaling (0 to 1)
    scaler = MinMaxScaler()
    scaled_values = scaler.fit_transform(filtered[features])
    scaled_df = pd.DataFrame(scaled_values, columns=features, index=filtered.index)
    
    # 4. Reverse price normalization so cheaper phones receive higher scores
    if 'price' in features:
        scaled_df['price'] = 1.0 - scaled_df['price']
        
    # 5. Calculate Final Weighted Score
    final_score = 0.0
    for feat, weight in weights.items():
        final_score += scaled_df[feat] * weight
        
    filtered['final_score'] = final_score * 100  # Scale to percentage (0 - 100)
    
    # 6. Sort and return top 5
    recommended = filtered.sort_values(by='final_score', ascending=False).head(5)
    return recommended

def generate_explanation(phone_row, persona):
    """Generates customized plain-English explanations for why a phone fits a persona."""
    reasons = []
    if persona == 'Student':
        if phone_row['price'] < 400:
            reasons.append(f"budget-friendly price of ${phone_row['price']:.0f}")
        if phone_row['battery'] >= 4500:
            reasons.append(f"long-lasting {phone_row['battery']} mAh battery for all-day classes")
        if phone_row['ram'] >= 6:
            reasons.append(f"reliable {phone_row['ram']}GB RAM for multitasking")
    elif persona == 'Gamer':
        if phone_row['processor_score'] >= 0.7:
            reasons.append("high-performance processor for lag-free gaming")
        if phone_row['ram'] >= 8:
            reasons.append(f"heavy-duty {phone_row['ram']}GB RAM")
        if phone_row['battery'] >= 4500:
            reasons.append(f"robust {phone_row['battery']} mAh battery")
    elif persona == 'Content Creator':
        if phone_row['camera'] >= 64:
            reasons.append(f"exceptional {phone_row['camera']}MP high-resolution camera")
        if phone_row['storage_gb'] >= 256:
            reasons.append(f"spacious {phone_row['storage_gb']}GB storage for photos and 4K videos")
    elif persona == 'Business Professional':
        if phone_row['battery'] >= 4500:
            reasons.append(f"dependable {phone_row['battery']} mAh battery for long work days")
        if phone_row['processor_score'] >= 0.7:
            reasons.append("powerful processor for smooth multitasking & productivity")
        if phone_row['ram'] >= 8:
            reasons.append(f"{phone_row['ram']}GB RAM for seamless app switching")
    elif persona == 'Senior Citizen':
        if phone_row['price'] < 350:
            reasons.append(f"very affordable price (${phone_row['price']:.0f})")
        if phone_row['battery'] >= 4500:
            reasons.append(f"reliable {phone_row['battery']} mAh battery requiring less frequent charging")
        reasons.append("balanced, practical specifications for everyday ease of use")
        
    if not reasons:
        reasons.append("balanced overall specifications matching your selected profile")
        
    return f"Selected for its " + ", ".join(reasons) + "."