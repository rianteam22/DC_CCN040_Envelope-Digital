# DC_CCN040_Envelope-Digital
#### Disciplina: Segurança em Sistemas Computacionais
#### Professor da disciplina: Carlos André Batista de Carvalho 
#### Trabalho 01 – Implementação: Envelope Digital Assinado

# Exemplo de Envelope Criptografado e Assinado

Este programa em Python demonstra a criação e abertura de envelopes criptografados e assinados usando uma combinação de criptografia simétrica e assimétrica. O programa consiste em três scripts principais:

1. **`gerar_par_chaves.py`**: Gera um par de arquivos de chave RSA tanto para o remetente quanto para o destinatário.

2. **`envelope_assinado.py`**: Cria e abre envelopes assinados. Ele criptografa um arquivo com uma chave simétrica, assina os dados criptografados com uma chave privada e, em seguida, envia os dados criptografados e assinados juntamente com as informações necessárias para o destinatário descriptografar.

3. **`main.py`**: Utiliza as funções dos scripts acima para demonstrar todo o processo.

## Uso

1. **Gerar Pares de Chaves:**

    ```bash
    python gerar_par_chaves.py
    ```

    Isso gerará pares de chaves tanto para o remetente quanto para o destinatário e os salvará como `chave_privada_remetente.pem`, `chave_publica_remetente.pem`, `chave_privada_destinatario.pem` e `chave_publica_destinatario.pem`.

2. **Criar Envelope Assinado:**

    ```bash
    python main.py
    ```

    Isso criará um envelope assinado criptografando um arquivo de exemplo (`arquivo_claro.txt`) com uma chave simétrica e assinando os dados criptografados com a chave privada do remetente. Os dados criptografados e a chave simétrica criptografada serão salvos como `envelope_assinado.enc` e `chave_secao_cifrada.pem`, respectivamente.

3. **Abrir Envelope Assinado:**

    ```bash
    python main.py
    ```

    Isso abrirá o envelope assinado usando a chave privada do destinatário e a chave pública do remetente. Os dados descriptografados serão salvos como `arquivo_decifrado.txt`.

## Dependências

- [cryptography](https://cryptography.io/en/latest/)

Instale as dependências necessárias usando:

```bash
pip install cryptography
```
