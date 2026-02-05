"""
Vercel Serverless Function - Options Endpoint
Returns available crops and soil types
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Return available options for dropdowns"""
        options = {
            "crops": [
                "Barley",
                "Cotton",
                "Maize",
                "Potato",
                "Rice",
                "Soybean",
                "Sugarcane",
                "Wheat"
            ],
            "soil_types": [
                "Black",
                "Clay",
                "Loamy",
                "Red",
                "Sandy"
            ],
            "countries": [
                "Argentina",
                "Australia",
                "Brazil",
                "China",
                "India",
                "USA"
            ]
        }
        
        self.send_json_response(options)
    
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
