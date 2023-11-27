# DC_CCN040_Envelope-Digital
#### Disciplina: Segurança em Sistemas Computacionais
#### Trabalho 01 – Implementação: Envelope Digital Assinado

# Envelope Digital Assinado

Este é um programa simples implementado em Python usando a biblioteca Tkinter e o módulo `cryptography`. Ele permite a criação de um envelope digital assinado, que envolve a criptografia e assinatura de um texto, e a posterior abertura e verificação desse envelope.

## Funcionalidades

1. **Criptografar e Assinar:**
   - Insira um texto no campo designado.
   - Escolha um algoritmo de criptografia simétrica (AES, 3DES, ou RC4).
   - Clique no botão "Criptografar e assinar" para gerar chaves, salvar o texto em um arquivo, criptografar e assinar o arquivo, e salvar a chave simétrica cifrada e o IV.

2. **Descriptografar e Verificar:**
   - Clique no botão "Descriptografar e verificar" para selecionar um arquivo criptografado e assinado.
   - O programa tentará descriptografar o arquivo e verificar a assinatura, usando as chaves privadas e públicas adequadas.

3. **Mensagens Pop-up:**
   - Mensagens informativas e de erro são exibidas através do método `messagebox` do Tkinter.

4. **Geração de Chaves e Operações Criptográficas:**
   - As operações criptográficas são realizadas por funções contidas nos scripts `gerar_par_chaves` e `envelope_assinado`.

5. **Algoritmo Padrão:**
   - O algoritmo simétrico padrão é definido como AES.

## Uso

1. Certifique-se de ter a biblioteca `cryptography` instalada.
   ```bash
   pip install cryptography
   ```

2. Execute o script main.
   ```bash
   python main.py
   ```

3. Siga as instruções na interface gráfica para criptografar, assinar, descriptografar e verificar seus envelopes digitais.

## Observações

- Certifique-se de ter as permissões adequadas para acessar os arquivos de chave privada e pública.
- Mantenha os scripts `gerar_par_chaves.py` e `envelope_assinado.py` no mesmo diretório que o script `main.py`, ou forneça os caminhos corretos se estiverem em diretórios diferentes.

Este programa foi desenvolvido como parte de um trabalho prático e destina-se a fins educacionais. 
