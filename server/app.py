"""
Flask REST API for Crop Yield Prediction
Provides endpoints for making predictions and getting model information.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import json
import os
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load models and encoders
print("Loading models...")
try:
    rf_model = joblib.load('models/random_forest_model.pkl')
    xgb_model = joblib.load('models/xgboost_model.pkl')
    label_encoders = joblib.load('models/label_encoders.pkl')
    
    with open('models/metrics.json', 'r') as f:
        metrics = json.load(f)
    
    with open('models/feature_importance.json', 'r') as f:
        feature_importance = json.load(f)
    
    with open('models/feature_names.json', 'r') as f:
        feature_names = json.load(f)
    
    print("[OK] Models loaded successfully!")
except FileNotFoundError:
    print("[ERROR] Models not found!")
    print("Please run 'python model.py' first to train the models.")
    exit(1)

def prepare_input(data):
    """
    Prepare input data for prediction.
    Encodes categorical variables and arranges features in correct order.
    """
    # Encode crop and soil_type
    crop_encoded = label_encoders['crop'].transform([data['crop']])[0]
    soil_encoded = label_encoders['soil_type'].transform([data['soil_type']])[0]
    
    # Create feature array in the same order as training
    features = [
        crop_encoded,
        soil_encoded,
        float(data['temperature']),
        float(data['rainfall']),
        float(data['humidity']),
        float(data['ph_level']),
        float(data['field_area']),
        int(data['irrigation']),
        float(data['fertilizer_used'])
    ]
    
    return np.array([features])

@app.route('/', methods=['GET'])
def home():
    """
    API home endpoint with documentation.
    """
    return jsonify({
        'message': 'Crop Yield Prediction API',
        'version': '1.0',
        'endpoints': {
            '/predict': 'POST - Get crop yield prediction',
            '/model-info': 'GET - Get model performance information',
            '/feature-importance': 'GET - Get feature importance data',
            '/options': 'GET - Get available crop and soil types'
        }
    })

@app.route('/options', methods=['GET'])
def get_options():
    """
    Get available options for categorical fields.
    """
    return jsonify({
        'crops': label_encoders['crop'].classes_.tolist(),
        'soil_types': label_encoders['soil_type'].classes_.tolist()
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict crop yield based on input parameters.
    
    Expected JSON input:
    {
        "crop": "Rice",
        "soil_type": "Loamy",
        "temperature": 28.5,
        "rainfall": 1200,
        "humidity": 65,
        "ph_level": 6.8,
        "field_area": 5,
        "irrigation": 1,
        "fertilizer_used": 150,
        "model": "random_forest"  // or "xgboost"
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['crop', 'soil_type', 'temperature', 'rainfall', 
                          'humidity', 'ph_level', 'field_area', 'irrigation', 
                          'fertilizer_used']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate crop and soil_type
        if data['crop'] not in label_encoders['crop'].classes_:
            return jsonify({
                'error': f"Invalid crop type. Choose from: {label_encoders['crop'].classes_.tolist()}"
            }), 400
        
        if data['soil_type'] not in label_encoders['soil_type'].classes_:
            return jsonify({
                'error': f"Invalid soil type. Choose from: {label_encoders['soil_type'].classes_.tolist()}"
            }), 400
        
        # Prepare input
        input_features = prepare_input(data)
        
        # Select model
        model_type = data.get('model', 'random_forest')
        if model_type == 'xgboost':
            model = xgb_model
            model_name = 'XGBoost'
        else:
            model = rf_model
            model_name = 'Random Forest'
        
        # Make prediction
        yield_per_hectare = model.predict(input_features)[0]
        total_yield = yield_per_hectare * float(data['field_area'])
        
        # Calculate confidence interval (approximation based on model's MAE)
        mae = metrics[model_type.replace('_', '_')]['mae']
        confidence_lower = max(0, yield_per_hectare - mae)
        confidence_upper = yield_per_hectare + mae
        
        # Prepare response
        response = {
            'success': True,
            'prediction': {
                'yield_per_hectare': round(yield_per_hectare, 2),
                'total_yield': round(total_yield, 2),
                'unit': 'quintals',
                'confidence_interval': {
                    'lower': round(confidence_lower, 2),
                    'upper': round(confidence_upper, 2)
                }
            },
            'model_used': model_name,
            'input_summary': {
                'crop': data['crop'],
                'field_area': data['field_area'],
                'location_conditions': f"{data['temperature']}°C, {data['rainfall']}mm rainfall"
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """
    Get information about the trained models.
    """
    return jsonify({
        'random_forest': {
            'name': 'Random Forest Regressor',
            'description': 'Ensemble learning method using multiple decision trees',
            'metrics': {
                'r2_score': round(metrics['random_forest']['test_r2'], 4),
                'mae': round(metrics['random_forest']['mae'], 2),
                'rmse': round(metrics['random_forest']['rmse'], 2)
            },
            'advantages': [
                'Robust to outliers',
                'Handles non-linear relationships',
                'Provides feature importance',
                'Less prone to overfitting'
            ]
        },
        'xgboost': {
            'name': 'XGBoost Regressor',
            'description': 'Gradient boosting algorithm optimized for performance',
            'metrics': {
                'r2_score': round(metrics['xgboost']['test_r2'], 4),
                'mae': round(metrics['xgboost']['mae'], 2),
                'rmse': round(metrics['xgboost']['rmse'], 2)
            },
            'advantages': [
                'High prediction accuracy',
                'Fast training and prediction',
                'Handles complex patterns',
                'Built-in regularization'
            ]
        },
        'explanation': {
            'r2_score': 'Proportion of variance explained (0-1, higher is better)',
            'mae': 'Mean Absolute Error in quintals/hectare (lower is better)',
            'rmse': 'Root Mean Squared Error in quintals/hectare (lower is better)'
        }
    })

@app.route('/feature-importance', methods=['GET'])
def get_feature_importance():
    """
    Get feature importance for both models.
    """
    # Prepare data for visualization
    features = []
    for feature_name, importance in feature_importance.items():
        features.append({
            'name': feature_name.replace('_', ' ').title(),
            'rf_importance': round(importance['rf_importance'] * 100, 2),
            'xgb_importance': round(importance['xgb_importance'] * 100, 2)
        })
    
    # Sort by Random Forest importance
    features.sort(key=lambda x: x['rf_importance'], reverse=True)
    
    return jsonify({
        'features': features,
        'description': 'Feature importance shows which factors most influence crop yield predictions'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'models_loaded': True
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("CROP YIELD PREDICTION API SERVER")
    print("="*60)
    print(f"\nServer running on: http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /              - API documentation")
    print("  GET  /options       - Get crop and soil type options")
    print("  POST /predict       - Make yield prediction")
    print("  GET  /model-info    - Get model information")
    print("  GET  /feature-importance - Get feature importance")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
