import streamlit as st
import numpy as np

def mod_inverse(a, m):
    """Menghitung invers modulo."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def validate_key_matrix(key):
    """Memvalidasi matriks kunci Hill Cipher."""
    key_matrix = np.array(key).reshape(int(len(key)**0.5), -1)
    determinant = int(np.round(np.linalg.det(key_matrix))) % 26
    if np.gcd(determinant, 26) != 1:
        raise ValueError(
            f"Determinant matriks adalah {determinant}, tidak memiliki invers modulo 26. Pilih matriks lain."
        )
    return True

def hill_encrypt(message, key):
    """Fungsi enkripsi Hill Cipher."""
    message = message.upper().replace(" ", "")
    key_size = int(len(key)**0.5)
    
    # Pastikan panjang pesan sesuai dengan ukuran matriks
    while len(message) % key_size != 0:
        message += "X"  # Tambahkan padding X
    
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
    
    # Hapus padding "X" yang ditambahkan selama enkripsi
    return decrypted_text.rstrip("X")

# Streamlit App
st.title("Cipher Encryptor & Decryptor")

st.sidebar.header("Input")
option = st.sidebar.radio("Pilih operasi:", ["Enkripsi", "Dekripsi"])
message = st.sidebar.text_input("Masukkan pesan (tanpa spasi):", "")
key_input = st.sidebar.text_input("Masukkan kunci (sebagai list, contoh: 6,24,1,13):", "")

if st.sidebar.button("Proses"):
    try:
        # Konversi input kunci ke list integer
        key = list(map(int, key_input.split(',')))
        
        if len(key) > 0:
            key_size = int(len(key)**0.5)
            if key_size * key_size != len(key):
                raise ValueError("Matriks kunci harus berupa matriks persegi (2x2, 3x3, dll).")
            
            # Validasi matriks
            validate_key_matrix(key)
            
            if option == "Enkripsi":
                cipher_text = hill_encrypt(message, key)
                st.success(f"Teks terenkripsi: {cipher_text}")
            elif option == "Dekripsi":
                decrypted_text = hill_decrypt(message, key)
                st.success(f"Teks terdekripsi: {decrypted_text}")
    except Exception as e:
        st.error(f"Error: {e}")
