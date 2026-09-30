# file: 2fa.py
import pyotp
import base64
import os
import hashlib
import qrcode
import io
import json
from datetime import datetime
import secrets
from typing import Optional, Dict, Tuple, List

class TwoFactorAuth:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        # Secret untuk enkripsi (gunakan environment variable di production)
        self.secret_key = app.config.get('SECRET_KEY', os.urandom(24))
    
    @staticmethod
    def generate_secret_key(user_id: str, app_secret: str = None) -> str:
        """Generate consistent secret key per user"""
        if app_secret:
            seed = f"{user_id}{app_secret}{datetime.now().isoformat()}"
            hash_obj = hashlib.sha256(seed.encode())
            secret = base64.b32encode(hash_obj.digest())[:32].decode()
        else:
            # Generate random secret
            secret = base64.b32encode(os.urandom(20)).decode()
        return secret.rstrip('=')
    
    @staticmethod
    def verify_totp(secret: str, user_code: str, valid_window: int = 1) -> bool:
        """Verify TOTP code with time window"""
        if not secret or not user_code:
            return False
        
        if len(user_code) != 6 or not user_code.isdigit():
            return False
        
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(user_code, valid_window=valid_window)
        except Exception:
            return False
    
    @staticmethod
    def generate_backup_codes(count: int = 8) -> List[str]:
        """Generate backup recovery codes"""
        codes = []
        for _ in range(count):
            code = secrets.token_hex(4).upper()[:10]
            codes.append(code)
        return codes
    
    @staticmethod
    def get_provisioning_uri(secret: str, user_id: str, issuer: str = "Pizza Thury") -> str:
        """Get URI for QR code generation"""
        return pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_id,
            issuer_name=issuer
        )
    
    @staticmethod
    def generate_qr_code(provisioning_uri: str) -> str:
        """Generate QR code as base64 string"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(provisioning_uri)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            return base64.b64encode(buffer.getvalue()).decode()
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return ""
    
    @staticmethod
    def hash_backup_code(code: str) -> str:
        """Hash backup code for secure storage"""
        return hashlib.sha256(code.encode()).hexdigest()
    
    @staticmethod
    def verify_backup_code(hashed_codes: List[str], user_code: str) -> Tuple[bool, List[str]]:
        """Verify backup code and return updated list"""
        if not user_code:
            return False, hashed_codes
        
        user_code_hash = hashlib.sha256(user_code.encode()).hexdigest()
        
        if user_code_hash in hashed_codes:
            # Remove used code
            hashed_codes.remove(user_code_hash)
            return True, hashed_codes
        
        return False, hashed_codes
    
    @staticmethod
    def get_current_otp(secret: str) -> str:
        """Get current valid OTP code (for debugging/testing)"""
        totp = pyotp.TOTP(secret)
        return totp.now()

# Singleton instance
two_fa = TwoFactorAuth()