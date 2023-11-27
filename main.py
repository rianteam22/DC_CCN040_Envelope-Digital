import tkinter as tk
from tkinter import filedialog
from gerar_par_chaves import gerar_par_chaves
from envelope_assinado import criar_envelope_assinado, abrir_envelope_assinado

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho 01 – Implementação: Envelope Digital Assinado")
        self.root.geometry("600x300")
        
        # Widgets
        self.label_text = tk.Label(root, text="Digite um texto:")
        self.text_entry = tk.Entry(root, width=50)
        self.text_entry.size
        self.label_algorithm = tk.Label(root, text="Selecione o algoritmo simétrico:")
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("AES") 
        self.algorithm_menu = tk.OptionMenu(root, self.algorithm_var, "AES", "3DES", "RC4")

        self.encrypt_button = tk.Button(root, text="Criptografar e assinar", command=self.criptografar_e_assinar)
        self.decrypt_button = tk.Button(root, text="Descriptografar e verificar", command=self.descriptografar_e_verificar)
        
        self.label_key_size = tk.Label(root, text="Tamanho da chave simétrica:")
        self.key_size_entry = tk.Entry(root)
        self.key_size_entry.insert(0, "256") 

        # Layout
        self.label_text.pack(pady=5)
        self.text_entry.pack(pady=5)
        self.label_algorithm.pack(pady=5)
        self.algorithm_menu.pack(pady=5)
        self.label_key_size.pack(pady=5)
        self.key_size_entry.pack(pady=5)
        self.encrypt_button.pack(pady=10)
        self.decrypt_button.pack(pady=10)

    def criptografar_e_assinar(self):
        text_to_encrypt = self.text_entry.get()

        if not text_to_encrypt:
            self.show_error("Digite o texto a ser criptografado.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, 'w') as file:
                file.write(text_to_encrypt)

            try:
                gerar_par_chaves('chave_privada_remetente.pem', 'chave_publica_remetente.pem')
                gerar_par_chaves('chave_privada_destinatario.pem', 'chave_publica_destinatario.pem')

                algoritmo_simetrico = self.algorithm_var.get()
                tamanho_chave_simetrica = int(self.key_size_entry.get()) 

                criar_envelope_assinado(file_path, 'chave_publica_destinatario.pem',
                                        'chave_privada_remetente.pem', algoritmo_simetrico, tamanho_chave_simetrica,
                                        'chave_secao_cifrada.pem', 'envelope_assinado.enc')

                self.show_message("Criptografia e assinatura bem-sucedidas!")

            except Exception as e:
                self.show_error(f"Error: {str(e)}")

    def descriptografar_e_verificar(self):
        file_path = filedialog.askopenfilename(defaultextension=".enc", filetypes=[("Encrypted files", "*.enc")])

        if file_path:
            try:
                algoritmo_simetrico = self.algorithm_var.get()
                
                abrir_envelope_assinado(file_path, 'chave_secao_cifrada.pem', 'chave_privada_destinatario.pem',
                                        'chave_publica_remetente.pem', algoritmo_simetrico, 'arquivo_decifrado.txt')

                self.show_message("A descriptografia e a verificação foram bem-sucedidas!")

            except Exception as e:
                self.show_error(f"Erro: {str(e)}")

    def show_message(self, message):
        tk.messagebox.showinfo("Mensagem", message)

    def show_error(self, message):
        tk.messagebox.showerror("Erro", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
