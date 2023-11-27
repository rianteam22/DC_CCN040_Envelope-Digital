# envelope_assinado.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, hmac
from cryptography.hazmat.primitives.asymmetric import padding
import os

def criar_envelope_assinado(arquivo_claro, arquivo_chave_publica_destinatario,
                            arquivo_chave_privada_remetente, algoritmo_simetrico, tamanho_chave_simetrica,
                            nome_arquivo_chave_secao, nome_arquivo_envelope_assinado):
    print("\nInicio criar_envelope_assinado\n")
    # Carregar chave pública do destinatário
    with open(arquivo_chave_publica_destinatario, 'rb') as arquivo_chave_publica:
        chave_publica_destinatario = serialization.load_pem_public_key(
            arquivo_chave_publica.read(),
            backend=default_backend()
        )

    # Gerar chave simétrica temporária/aleatória e IV
    if algoritmo_simetrico == 'AES':
        chave_simetrica = os.urandom(tamanho_chave_simetrica // 8)
        iv = os.urandom(16)  # O tamanho do IV para o AES é de 16 bytes
    elif algoritmo_simetrico == '3DES':
        chave_simetrica = os.urandom(24)
        iv = os.urandom(8) # O tamanho do IV para o 3DES é de 8 bytes
    elif algoritmo_simetrico == 'RC4':
        chave_simetrica = os.urandom(tamanho_chave_simetrica // 8)
        iv = os.urandom(0)  # O RC4 não usa um IV
    else:
        raise ValueError("Algoritmo simetrico invalido")
        
    print(f"Chave Simetrica: {chave_simetrica}\n\nIV: {iv}\n")
    
    # Cifrar arquivo em claro com a chave simétrica e IV
    with open(arquivo_claro, 'rb') as arquivo:
        texto_claro = arquivo.read()
        
    print(f"Texto Claro: {texto_claro}\n")
    
    print(f"Algoritmo Simetrico: {algoritmo_simetrico}\n")
    if algoritmo_simetrico == 'AES':
        cipher = Cipher(algorithms.AES(chave_simetrica), modes.CFB8(iv), backend=default_backend())
    elif algoritmo_simetrico == '3DES':
        cipher = Cipher(algorithms.TripleDES(chave_simetrica), modes.CFB8(iv), backend=default_backend())
    elif algoritmo_simetrico == 'RC4':
        cipher = Cipher(algorithms.ARC4(chave_simetrica), mode=None, backend=default_backend())
    else:
        raise ValueError("Algoritmo simetrico invalido")

    encryptor = cipher.encryptor()
    texto_cifrado = encryptor.update(texto_claro) + encryptor.finalize()
    
    print(f"Texto Cifrado: {texto_cifrado}\n")
    
    # Assinar o arquivo criptografado com a chave privada do remetente
    with open(arquivo_chave_privada_remetente, 'rb') as arquivo_chave_privada:
        chave_privada_remetente = serialization.load_pem_private_key(
            arquivo_chave_privada.read(),
            password=None,
            backend=default_backend()
        )

    assinatura = chave_privada_remetente.sign(
        texto_cifrado,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print(f"Assinatura: {assinatura}\n")
    
    # Cifrar a chave temporária com a chave do destinatário
    chave_simetrica_cifrada = chave_publica_destinatario.encrypt(
        chave_simetrica,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    print(f"Chave Simetrica Cifrada: {chave_simetrica_cifrada}\n")
    
    # Salvar chave de seção criptografada e IV
    with open(nome_arquivo_chave_secao, 'wb') as arquivo_chave_secao:
        arquivo_chave_secao.write(chave_simetrica_cifrada)

    # Salvar arquivo criptografado assinado
    with open(nome_arquivo_envelope_assinado, 'wb') as arquivo_envelope:
        arquivo_envelope.write(assinatura + iv + texto_cifrado)
        
    print("\nFim criar_envelope_assinado\n")


def abrir_envelope_assinado(arquivo_envelope_assinado, arquivo_chave_secao_privada, 
                            arquivo_chave_privada_destinatario, arquivo_chave_publica_remetente, 
                            algoritmo_simetrico, nome_arquivo_saida):
    
    print("\nInicio abrir_envelope_assinado\n")
    
    # Carregar chave privada do destinatário
    with open(arquivo_chave_privada_destinatario, 'rb') as arquivo_chave_privada:
        chave_privada_destinatario = serialization.load_pem_private_key(
            arquivo_chave_privada.read(),
            password=None,
            backend=default_backend()
        )

    # Carregar chave pública do remetente
    with open(arquivo_chave_publica_remetente, 'rb') as arquivo_chave_publica:
        chave_publica_remetente = serialization.load_pem_public_key(
            arquivo_chave_publica.read(),
            backend=default_backend()
        )
    
    # Carregar chave simetrica cifrada
    with open(arquivo_chave_secao_privada, 'rb') as arquivo_chave_secao:
        chave_simetrica_cifrada = arquivo_chave_secao.read()

    # Carregar envelope assinado
    with open(arquivo_envelope_assinado, 'rb') as arquivo_envelope:
        envelope_assinado = arquivo_envelope.read()

    print(f"Envelope Assinado: {envelope_assinado}\n")

    # Separar assinatura, IV e texto cifrado
    assinatura = envelope_assinado[:256]
    dados_cifrados = envelope_assinado[256:]
    
    print(f"Assinatura: {assinatura}\n\nDados Cifrados: {dados_cifrados}\n")

    # Determine the IV size based on the symmetric algorithm
    if algoritmo_simetrico == 'AES':
        tamanho_iv = 16  # Assuming a common IV size for AES
    elif algoritmo_simetrico == '3DES':
        tamanho_iv = 8
    elif algoritmo_simetrico == 'RC4':
        tamanho_iv = 0  # RC4 doesn't use an IV
    else:
        raise ValueError("Algoritmo simetrico invalido")

    # Extract IV and ciphertext
    iv = dados_cifrados[:tamanho_iv]
    texto_cifrado = dados_cifrados[tamanho_iv:]

    print(f"Assinatura: {assinatura}\n\nIV: {iv}\n\nTexto Cifrado: {texto_cifrado}")
    # Verificar a assinatura
    try:
        chave_publica_remetente.verify(
            assinatura,
            texto_cifrado,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Assinatura válida.")
    except Exception as e:
        raise ValueError("Assinatura inválida")

    
    chave_simetrica = chave_privada_destinatario.decrypt(
        chave_simetrica_cifrada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"Chave Simetrica Decifrada: {chave_simetrica}\n")
    
    print(f"Algoritmo Simetrico: {algoritmo_simetrico}\n")
    # Decifrar o texto cifrado
    if algoritmo_simetrico == 'AES':
        cipher = Cipher(algorithms.AES(chave_simetrica), modes.CFB8(iv), backend=default_backend())
    elif algoritmo_simetrico == '3DES':
        cipher = Cipher(algorithms.TripleDES(chave_simetrica), modes.CFB8(iv), backend=default_backend())
    elif algoritmo_simetrico == 'RC4':
        cipher = Cipher(algorithms.ARC4(chave_simetrica), mode=None, backend=default_backend())
    else:
        raise ValueError("Algoritmo simetrico invalido")

    decryptor = cipher.decryptor()
    texto_decifrado = decryptor.update(texto_cifrado) + decryptor.finalize()

    print(f"Texto Decifrado: {texto_decifrado}\n")
    # Salvar o arquivo decifrado
    with open(nome_arquivo_saida, 'wb') as arquivo_saida:
        arquivo_saida.write(texto_decifrado)

    print("\nFim abrir_envelope_assinado\n")
