#gerar_par_chaves.py
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def gerar_par_chaves(nome_arquivo_chave_privada, nome_arquivo_chave_publica):
    chave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    print(f"Chave Privada: {chave_privada}")
    chave_publica = chave_privada.public_key()

    print(f"Chave Publica: {chave_publica}")
    # Salvar chave privada em formato PEM
    with open(nome_arquivo_chave_privada, 'wb') as chave_privada_arquivo:
        chave_privada_arquivo.write(
            chave_privada.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Salvar chave pública em formato PEM
    with open(nome_arquivo_chave_publica, 'wb') as chave_publica_arquivo:
        chave_publica_arquivo.write(
            chave_publica.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
