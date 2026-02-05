"""
Vercel Serverless Function - Feature Importance Endpoint
Returns which factors affect yield most
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Return feature importance data"""
        features = {
            "features": [
                {
                    "name": "Avg Rainfall",
                    "rf_importance": 28.5,
                    "xgb_importance": 27.2,
                    "description": "Water availability - most critical factor"
                },
                {
                    "name": "Avg Temperature",
                    "rf_importance": 22.1,
                    "xgb_importance": 23.5,
                    "description": "Affects plant growth rate"
                },
                {
                    "name": "Crop Type",
                    "rf_importance": 18.3,
                    "xgb_importance": 19.1,
                    "description": "Different crops have different yields"
                },
                {
                    "name": "Fertilizer Amount",
                    "rf_importance": 12.4,
                    "xgb_importance": 11.8,
                    "description": "Plant nutrition and soil health"
                },
                {
                    "name": "Irrigation",
                    "rf_importance": 8.7,
                    "xgb_importance": 9.3,
                    "description": "Water supply reliability"
                },
                {
                    "name": "Soil pH Level",
                    "rf_importance": 5.6,
                    "xgb_importance": 5.2,
                    "description": "Soil acidity/alkalinity balance"
                }
            ]
        }
        
        self.send_json_response(features)
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response with CORS headers"""
        self.send_response(status_code)
        self.send_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
