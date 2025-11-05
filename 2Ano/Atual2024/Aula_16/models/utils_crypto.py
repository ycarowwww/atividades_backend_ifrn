from .utils_fileio import get_file_path
import base64
from cryptography.fernet import Fernet
import json
from typing import Optional

class Crypto:
    """Classe contendo métodos para criptografar dados usando o algoritmo AES (com a biblioteca do Python Cryptography)."""
    __key_file = get_file_path("../data/keys.json")
    __key: Optional[str] = None
    
    @classmethod
    def load_key(cls) -> str:
        if cls.__key is None:
            with open(cls.__key_file, "r") as file:
                cls.__key = json.load(file).get("key") # Pega a chave salva.
            
            if cls.__key is None:
                cls.__key = Fernet.generate_key().decode() # Gera uma chave aleatória caso não haja chaves salvas.
                cls.__save_file()
        
        return cls.__key
    
    @classmethod
    def encrypt(cls, text: str) -> str:
        """Encripta um texto usando a chave atual do App em keys.json com AES."""
        cipher = Fernet(cls.load_key())
        return cipher.encrypt(text.encode()).decode()
    
    @classmethod
    def decrypt(cls, text: str) -> str:
        """Decripta um texto usando a chave atual do App em keys.json com AES."""
        cipher = Fernet(cls.load_key())
        return cipher.decrypt(text.encode()).decode()

    @classmethod
    def __save_file(cls) -> None:
        with open(cls.__key_file, mode="w") as file:
            json_objects = { "key" : cls.__key }
            json.dump(json_objects, file, indent=4)

class CryptoBase64:
    @staticmethod
    def encrypt(data: bytes | str) -> str:
        if isinstance(data, str): data = data.encode()
        
        return base64.b64encode(data).decode()
    
    @staticmethod
    def decrypt(data: bytes | str) -> bytes:
        return base64.b64decode(data)
