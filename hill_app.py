import streamlit as st
import numpy as np

def mod_inverse(a, m):
    """Menghitung invers modulo."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def hill_encrypt(message, key):
    """Fungsi enkripsi Hill Cipher."""
    message = message.upper().replace(" ", "")
    key_size = int(len(key)**0.5)
    
    # Pastikan panjang pesan sesuai dengan ukuran matriks
    while len(message) % key_size != 0:
        message += "X"
    
    # Ubah pesan menjadi angka (A=0, B=1, ..., Z=25)
    message_vector = [ord(char) - 65 for char in message]
    message_matrix = np.array(message_vector).reshape(-1, key_size)
    
    # Konversi kunci ke matriks
    key_matrix = np.array(key).reshape(key_size, key_size)
    
    # Enkripsi
    cipher_matrix = (np.dot(message_matrix, key_matrix) % 26).flatten()
    cipher_text = "".join(chr(num + 65) for num in cipher_matrix)
    
    return cipher_text

def hill_decrypt(cipher_text, key):
    """Fungsi dekripsi Hill Cipher."""
    key_size = int(len(key)**0.5)
    
    # Konversi ciphertext menjadi angka
    cipher_vector = [ord(char) - 65 for char in cipher_text]
    cipher_matrix = np.array(cipher_vector).reshape(-1, key_size)
    
    # Cari invers matriks kunci
    key_matrix = np.array(key).reshape(key_size, key_size)
    determinant = int(np.round(np.linalg.det(key_matrix))) % 26
    determinant_inv = mod_inverse(determinant, 26)
    if determinant_inv is None:
        raise ValueError("Matriks kunci tidak dapat di-invers.")
    
    key_matrix_inv = determinant_inv * np.round(
        determinant * np.linalg.inv(key_matrix)
    ).astype(int) % 26
    
    # Dekripsi
    decrypted_matrix = (np.dot(cipher_matrix, key_matrix_inv) % 26).flatten()
    decrypted_text = "".join(chr(num + 65) for num in decrypted_matrix)
    
    return decrypted_text

# Streamlit App
st.title("Hill Cipher Encryptor & Decryptor")

st.sidebar.header("Input")
option = st.sidebar.radio("Pilih operasi:", ["Enkripsi", "Dekripsi"])
message = st.sidebar.text_input("Masukkan pesan (tanpa spasi):", "")
key_input = st.sidebar.text_input("Masukkan kunci (sebagai list, contoh: 6,24,1,18):", "")

if st.sidebar.button("Proses"):
    try:
        # Konversi input kunci ke list integer
        key = list(map(int, key_input.split(',')))
        
        if len(key) > 0:
            key_size = int(len(key)**0.5)
            if key_size * key_size != len(key):
                raise ValueError("Matriks kunci harus berupa matriks persegi (2x2, 3x3, dll).")
            
            if option == "Enkripsi":
                cipher_text = hill_encrypt(message, key)
                st.success(f"Teks terenkripsi: {cipher_text}")
            elif option == "Dekripsi":
                decrypted_text = hill_decrypt(message, key)
                st.success(f"Teks terdekripsi: {decrypted_text}")
    except Exception as e:
        st.error(f"Error: {e}")
