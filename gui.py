# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os

from quantum_key import QuantumKeyManager
from aes_crypto import encrypt_data, decrypt_data

class QuantumCryptoGUI:
    def __init__(self, master):
        self.master = master
        self.key_manager = QuantumKeyManager()
        master.title("基于BB84的QKD与AES加密系统")
        master.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # 省略重复，保持不变，同原始内容
        # 可继续分拆成 create_file_widgets, create_key_widgets 等函数

        # 示例按钮绑定
        tk.Button(crypto_frame, text="加密文件", command=self.encrypt_file).pack(pady=5)

    def encrypt_file(self):
        if not self.key_manager.aes_key:
            messagebox.showwarning("警告", "请先生成量子密钥！")
            return

        filename = self.file_path_var.get()
        if not filename or not os.path.exists(filename):
            messagebox.showerror("错误", "请先选择有效文件！")
            return

        try:
            with open(filename, 'rb') as f:
                data = f.read()

            iv, ct_hex, ct_bytes = encrypt_data(self.key_manager.aes_key, data)
            self.key_manager.iv = iv
            self.key_manager.encrypted_data = ct_hex

            new_name = f"{os.path.splitext(filename)[0]}_encrypted.bin"
            with open(new_name, 'wb') as f:
                f.write(ct_bytes)

            self.update_status(f"文件加密成功！保存为：{new_name}")
        except Exception as e:
            messagebox.showerror("错误", f"加密失败: {str(e)}")

    def decrypt_file(self):
        if not all([self.key_manager.aes_key, self.key_manager.iv, self.key_manager.encrypted_data]):
            messagebox.showwarning("警告", "缺少必要的解密参数！")
            return

        try:
            pt_bytes = decrypt_data(self.key_manager.aes_key,
                                    self.key_manager.iv,
                                    self.key_manager.encrypted_data)

            filename = self.file_path_var.get()
            new_name = f"{os.path.splitext(filename)[0]}_decrypted"
            with open(new_name, 'wb') as f:
                f.write(pt_bytes)

            self.update_status(f"文件解密成功！保存为：{new_name}")
        except Exception as e:
            messagebox.showerror("错误", f"解密失败: {str(e)}")
