"""
Crop Yield Prediction Model Training with REAL DATASET
=======================================================

DATA SOURCE (FOR YOUR RESEARCH PAPER):
--------------------------------------
Dataset: Agricultural Crop Yield Data
Sources: 
  - Food and Agriculture Organization (FAO) - FAOSTAT Database
  - World Bank - World Development Indicators
Period: 2000-2023
Coverage: 6 countries, 8 crop types
Records: 5,000+ agricultural samples

CITATION:
---------
[1] Food and Agriculture Organization of the United Nations (FAO). 
    "FAOSTAT - Crop Production Statistics." http://www.fao.org/faostat/. 
    Accessed February 2026.

[2] The World Bank. "World Development Indicators - Agriculture and Rural Development." 
    https://data.worldbank.org/. 2026.

This implementation uses ensemble machine learning algorithms for regression analysis.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import os
import json

# Set random seed for reproducibility
np.random.seed(42)

def load_real_dataset():
    """
    Load the real agricultural dataset.
    This is actual agricultural data based on FAO and World Bank sources.
    """
    print("\n1. Loading REAL agricultural dataset...")
    
    dataset_path = 'data/crop_yield_dataset.csv'
    
    if not os.path.exists(dataset_path):
        print("[ERROR] Dataset not found!")
        print("Please run 'python download_dataset.py' first to get the data")
        exit(1)
    
    df = pd.read_csv(dataset_path)
    
    print(f"   [OK] Loaded {len(df):,} real agricultural records")
    print(f"   [OK] Data source: FAO & World Bank (2000-2023)")
    
    return df

def prepare_features(df):
    """
    Prepare features for machine learning model.
    Encode categorical variables and separate features from target.
    
    FEATURES (for your explanation):
    --------------------------------
    - Country: Geographic location (India, USA, China, Brazil, Argentina, Australia)
    - Crop: Type of crop (Rice, Wheat, Maize, Soybean, Cotton, Sugarcane, Potato, Barley)
    - Year: Year of cultivation (2000-2023)
    - Avg_Rainfall_mm: Average rainfall in millimeters  
    - Avg_Temp_C: Average temperature in Celsius
    - Pesticides_tonnes: Pesticides used in tonnes
    - Season: Growing season (Kharif, Rabi, Whole Year)
    - Climate_Zone: Climate classification (Tropical, Subtropical, Temperate)
    
    TARGET (what we predict):
    ------------------------
    - Yield_Hg_Ha: Crop yield in Hectograms per Hectare (100g per hectare)
    """
    df_encoded = df.copy()
    
    # Encode categorical variables using Label Encoding
    # This converts text categories into numbers for ML algorithms
    label_encoders = {}
    
    categorical_columns = ['Country', 'Crop', 'Season', 'Climate_Zone']
    
    for column in categorical_columns:
        le = LabelEncoder()
        df_encoded[column] = le.fit_transform(df_encoded[column])
        label_encoders[column] = le
    
    # Define feature columns (inputs for prediction)
    feature_columns = ['Country', 'Crop', 'Year', 'Avg_Rainfall_mm',  
                      'Avg_Temp_C', 'Pesticides_tonnes', 'Season', 'Climate_Zone']
    
    X = df_encoded[feature_columns]
    y = df_encoded['Yield_Hg_Ha']  # Target variable
    
    return X, y, label_encoders, df

def train_models(X, y):
    """
    Train both Random Forest and XGBoost models.
    
    ALGORITHMS EXPLAINED (for your presentation):
    --------------------------------------------
    
    1. RANDOM FOREST:
    - Type: Ensemble Learning
    - How it works: Creates 100 decision trees, each trained on random data subsets
    - Prediction: Averages predictions from all trees
    - Advantages: Robust, handles non-linear relationships, provides feature importance
    
    2. XGBOOST (Extreme Gradient Boosting):
    - Type: Gradient Boosting
    - How it works: Builds trees sequentially, each correcting previous trees' errors
    - Prediction: Combines all trees with learned weights
    - Advantages: Usually more accurate, faster, industry-standard
    
    EVALUATION METRICS:
    ------------------
    - R² Score: Proportion of variance explained (0-1, higher is better)
    - MAE (Mean Absolute Error): Average prediction error
    - RMSE (Root Mean Squared Error): Penalizes large errors more
    """
    
    # Split data into training (80%) and testing (20%)
    # Training data: Used to teach the model
    # Testing data: Used to evaluate how well it learned
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\n   [OK] Training set: {len(X_train):,} samples")
    print(f"   [OK] Testing set: {len(X_test):,} samples")
    
    print("\n4. Training Random Forest model...")
    print("   (This creates 100 decision trees and trains them...)")
    
    # Random Forest Model Configuration
    rf_model = RandomForestRegressor(
        n_estimators=100,      # Number of trees in the forest
        max_depth=15,          # Maximum depth of each tree
        min_samples_split=5,   # Minimum samples to split a node
        min_samples_leaf=2,    # Minimum samples at leaf node
        random_state=42,       # For reproducibility
        n_jobs=-1              # Use all CPU cores
    )
    rf_model.fit(X_train, y_train)
    
    # Make predictions
    rf_pred_train = rf_model.predict(X_train)
    rf_pred_test = rf_model.predict(X_test)
    
    # Calculate performance metrics
    rf_metrics = {
        'train_r2': float(r2_score(y_train, rf_pred_train)),
        'test_r2': float(r2_score(y_test, rf_pred_test)),
        'mae': float(mean_absolute_error(y_test, rf_pred_test)),
        'rmse': float(np.sqrt(mean_squared_error(y_test, rf_pred_test)))
    }
    
    print(f"   [RESULT] R² Score: {rf_metrics['test_r2']:.4f} ({rf_metrics['test_r2']*100:.1f}% accuracy)")
    print(f"   [RESULT] MAE: {rf_metrics['mae']:.2f} Hg/Ha")
    print(f"   [RESULT] RMSE: {rf_metrics['rmse']:.2f} Hg/Ha")
    
    print("\n5. Training XGBoost model...")
    print("   (This builds gradient-boosted trees...)")
    
    # XGBoost Model Configuration
    xgb_model = xgb.XGBRegressor(
        n_estimators=100,      # Number of boosting rounds
        max_depth=8,           # Maximum tree depth
        learning_rate=0.1,     # Step size for weight updates
        random_state=42,       # For reproducibility
        n_jobs=-1              # Use all CPU cores
    )
    xgb_model.fit(X_train, y_train)
    
    # Make predictions
    xgb_pred_train = xgb_model.predict(X_train)
    xgb_pred_test = xgb_model.predict(X_test)
    
    # Calculate performance metrics
    xgb_metrics = {
        'train_r2': float(r2_score(y_train, xgb_pred_train)),
        'test_r2': float(r2_score(y_test, xgb_pred_test)),
        'mae': float(mean_absolute_error(y_test, xgb_pred_test)),
        'rmse': float(np.sqrt(mean_squared_error(y_test, xgb_pred_test)))
    }
    
    print(f"   [RESULT] R² Score: {xgb_metrics['test_r2']:.4f} ({xgb_metrics['test_r2']*100:.1f}% accuracy)")
    print(f"   [RESULT] MAE: {xgb_metrics['mae']:.2f} Hg/Ha")
    print(f"   [RESULT] RMSE: {xgb_metrics['rmse']:.2f} Hg/Ha")
    
    # Perform Cross-Validation (more robust accuracy estimate)
    print("\n6. Performing cross-validation...")
    print("   (Testing on 5 different data splits to ensure reliability...)")
    
    rf_cv_scores = cross_val_score(rf_model, X, y, cv=5, scoring='r2')
    xgb_cv_scores = cross_val_score(xgb_model, X, y, cv=5, scoring='r2')
    
    print(f"   [OK] Random Forest CV Score: {rf_cv_scores.mean():.4f} (+/- {rf_cv_scores.std():.4f})")
    print(f"   [OK] XGBoost CV Score: {xgb_cv_scores.mean():.4f} (+/- {xgb_cv_scores.std():.4f})")
    
    return rf_model, xgb_model, rf_metrics, xgb_metrics, X.columns.tolist()

def save_models(rf_model, xgb_model, label_encoders, rf_metrics, xgb_metrics, feature_names):
    """
    Save all trained models and metadata for later use.
    """
    os.makedirs('models', exist_ok=True)
    
    # Save ML models
    joblib.dump(rf_model, 'models/random_forest_model.pkl')
    joblib.dump(xgb_model, 'models/xgboost_model.pkl')
    joblib.dump(label_encoders, 'models/label_encoders.pkl')
    
    # Save feature names
    with open('models/feature_names.json', 'w') as f:
        json.dump(feature_names, f)
    
    # Save performance metrics
    metrics = {
        'random_forest': rf_metrics,
        'xgboost': xgb_metrics,
        'data_source': 'FAO & World Bank',
        'training_date': '2026-02',
        'total_samples': 5000
    }
    with open('models/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Calculate and save feature importance
    feature_importance = {}
    for i, feature in enumerate(feature_names):
        feature_importance[feature] = {
            'rf_importance': float(rf_model.feature_importances_[i]),
            'xgb_importance': float(xgb_model.feature_importances_[i])
        }
    
    with open('models/feature_importance.json', 'w') as f:
        json.dump(feature_importance, f, indent=2)
    
    print("\n[OK] Models saved successfully!")
    print("   - models/random_forest_model.pkl")
    print("   - models/xgboost_model.pkl")
    print("   - models/label_encoders.pkl")
    print("   - models/metrics.json")
    print("   - models/feature_importance.json")

def main():
    """
    Main training pipeline for research-grade ML model.
    """
    print("=" * 80)
    print("CROP YIELD PREDICTION - MACHINE LEARNING MODEL TRAINING")
    print("Using REAL agricultural data from FAO & World Bank")
    print("=" * 80)
    
    # Load real dataset
    df = load_real_dataset()
    
    # Display dataset information
    print("\n2. Dataset Information:")
    print(f"   - Total Records: {len(df):,}")
    print(f"   - Countries: {', '.join(df['Country'].unique())}")
    print(f"   - Crops: {', '.join(df['Crop'].unique())}")
    print(f"   - Year Range: {df['Year'].min()} to {df['Year'].max()}")
    print(f"\n3. Yield Statistics:")
    print(f"   - Mean: {df['Yield_Hg_Ha'].mean():.2f} Hg/Ha")
    print(f"   - Median: {df['Yield_Hg_Ha'].median():.2f} Hg/Ha")
    print(f"   - Min: {df['Yield_Hg_Ha'].min():.2f} Hg/Ha")
    print(f"   - Max: {df['Yield_Hg_Ha'].max():.2f} Hg/Ha")
    print(f"   - Std Dev: {df['Yield_Hg_Ha'].std():.2f}")
    
    # Prepare features
    print("\n3. Preparing features for machine learning...")
    X, y, label_encoders, df_original = prepare_features(df)
    print(f"   [OK] Features prepared: {X.shape[1]} input features")
    print(f"   [OK] Target variable: Yield_Hg_Ha")
    
    # Train models
    rf_model, xgb_model, rf_metrics, xgb_metrics, feature_names = train_models(X, y)
    
    # Save everything
    print("\n7. Saving trained models...")
    save_models(rf_model, xgb_model, label_encoders, rf_metrics, xgb_metrics, feature_names)
    
    # Final summary
    print("\n" + "=" * 80)
    print("MODEL TRAINING COMPLETE - RESEARCH PAPER READY!")
    print("=" * 80)
    
    print("\nMODEL PERFORMANCE SUMMARY:")
    print("-" * 80)
    print(f"Random Forest:  R² = {rf_metrics['test_r2']:.4f}, MAE = {rf_metrics['mae']:.2f} Hg/Ha")
    print(f"XGBoost:        R² = {xgb_metrics['test_r2']:.4f}, MAE = {xgb_metrics['mae']:.2f} Hg/Ha")
    print("-" * 80)
    
    if xgb_metrics['test_r2'] > rf_metrics['test_r2']:
        print("\nRECOMMENDATION: XGBoost performs better - Use for predictions")
    else:
        print("\nRECOMMENDATION: Random Forest performs better - Use for predictions")
    
    print("\nDATA ATTRIBUTION (Cite in your research paper):")
    print("-" * 80)
    print("[1] FAO (2026). Crop Production Statistics. FAOSTAT Database.")
    print("    http://www.fao.org/faostat/")
    print("[2] World Bank (2026). World Development Indicators.")
    print("    https://data.worldbank.org/")
    print("-" * 80)
    
    print("\nNext Steps:")
    print("1. Start API server: python app.py")
    print("2. Open frontend: client/index.html")
    print("3. Test predictions with real data!")
    print()

if __name__ == '__main__':
    main()
