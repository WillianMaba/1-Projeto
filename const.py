import secrets

# Gerar uma chave secreta de 32 bytes (256 bits)
secret_key = secrets.token_hex(25)  # Gera uma string hexadecimal
print(secret_key)