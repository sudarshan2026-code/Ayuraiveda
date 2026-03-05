"""
API Client for ML Model Integration
"""

import requests
from typing import Dict, Optional

class ModelAPIClient:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if API is available"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def predict(self, data: Dict) -> Optional[Dict]:
        """Get prediction from ML model API"""
        if not self.available:
            return None
        
        try:
            response = requests.post(
                f"{self.api_url}/predict",
                json=data,
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            print(f"API call failed: {e}")
            return None
