
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import aes_module, rsa_module, hybrid_module
from backend.rsa_module import generate_rsa_keys
from backend import file_crypto


class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Encryption-Decryption Tool")
        self.root.geometry("600x500")

        self.mode_var = tk.StringVar(value="AES")

        tk.Label(root, text="Enter Text:").pack()
        self.input_text = scrolledtext.ScrolledText(root, height=5)
        self.input_text.pack()

        tk.Label(root, text="Key (for AES):").pack()
        self.key_entry = tk.Entry(root)
        self.key_entry.pack()

        tk.Label(root, text="Encryption Mode:").pack()
        for mode in ["AES", "RSA", "Hybrid"]:
            tk.Radiobutton(root, text=mode, variable=self.mode_var, value=mode).pack(anchor=tk.W)

        # File encryption buttons
        tk.Button(self.root, text="Encrypt File (AES)", command=self.encrypt_file).pack(pady=2)
        tk.Button(self.root, text="Decrypt File (AES)", command=self.decrypt_file).pack(pady=2)

        # Text encryption buttons
        tk.Button(root, text="Encrypt", command=self.encrypt).pack(pady=5)
        tk.Button(root, text="Decrypt", command=self.decrypt).pack(pady=5)

        # RSA key generation
        tk.Button(root, text="Generate RSA Keys", command=self.generate_keys).pack(pady=10)

        tk.Label(root, text="Output:").pack()
        self.output_text = scrolledtext.ScrolledText(root, height=10)
        self.output_text.pack()

    def generate_keys(self):
        try:
            generate_rsa_keys()
            messagebox.showinfo("Success", "RSA keys generated and saved to /keys folder.")
        except Exception as e:
            messagebox.showerror("Error", f"Key generation failed: {str(e)}")

    def encrypt(self):
        text = self.input_text.get("1.0", tk.END).strip()
        mode = self.mode_var.get()
        key = self.key_entry.get()

        try:
            if mode == "AES":
                result = aes_module.encrypt_aes(text, key)
            elif mode == "RSA":
                result = rsa_module.encrypt_rsa(text)
            else:
                result = hybrid_module.hybrid_encrypt(text)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))

    def decrypt(self):
        ciphertext = self.input_text.get("1.0", tk.END).strip()
        mode = self.mode_var.get()
        key = self.key_entry.get()

        try:
            if mode == "AES":
                result = aes_module.decrypt_aes(ciphertext, key)
            elif mode == "RSA":
                result = rsa_module.decrypt_rsa(ciphertext)
            else:
                result = hybrid_module.hybrid_decrypt(ciphertext)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))

    def encrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Encrypt")
        if not file_path:
            return
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Error", "Please enter a key.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".enc", title="Save Encrypted File As")
        if output_file:
            try:
                file_crypto.encrypt_file_aes(file_path, output_file, key)
                messagebox.showinfo("Success", f"File encrypted and saved as {output_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Encryption failed: {str(e)}")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select Encrypted File")
        if not file_path:
            return
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Error", "Please enter a key.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".dec", title="Save Decrypted File As")
        if output_file:
            try:
                file_crypto.decrypt_file_aes(file_path, output_file, key)
                messagebox.showinfo("Success", f"File decrypted and saved as {output_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Decryption failed: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
