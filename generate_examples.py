#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ornek Ciktilar Olusturucu
=========================
Collatz kriptografik algoritma icin ornek ciktilar uretir.
"""

import sys
import os

# Ana modulu import et
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collatz_crypto import CollatzCrypto
from key_generator import KeyGenerator


def run_examples():
    """Ornek sifreleme ve cozme islemleri."""
    
    output_lines = []
    
    def log(text=""):
        print(text)
        output_lines.append(text)
    
    log("=" * 70)
    log("COLLATZ KRIPTOGRAFIK ALGORITMA - ORNEK CIKTILAR")
    log("=" * 70)
    
    # Test metinleri
    test_texts = [
        "Hello World",
        "Cryptography Test 123",
        "ABCDEFGHIJKLMNOP",
        "The quick brown fox jumps over the lazy dog"
    ]
    
    # Varsayilan anahtar seti
    seed = 27
    affine_a = 5
    affine_b = 8
    trans_key = "3142"
    
    log(f"\n[ANAHTAR BILGILERI]")
    log(f"  Collatz Seed: {seed}")
    log(f"  Affine a: {affine_a}")
    log(f"  Affine b: {affine_b}")
    log(f"  Transposition Key: {trans_key}")
    log(f"  Modulus: 256")
    
    crypto = CollatzCrypto(
        seed=seed,
        affine_a=affine_a,
        affine_b=affine_b,
        trans_key=trans_key
    )
    
    log(f"  Affine a^(-1): {crypto.affine_a_inverse}")
    
    log("\n" + "=" * 70)
    log("SIFRELEME ORNEKLERI")
    log("=" * 70)
    
    for i, text in enumerate(test_texts, 1):
        log(f"\n--- ORNEK {i} ---")
        log(f"Duz Metin: \"{text}\"")
        log(f"Uzunluk: {len(text)} karakter")
        
        # Byte'lara donustur
        data = text.encode('utf-8')
        log(f"\n[ADIM 1] UTF-8 -> Byte:")
        log(f"  Hex: {data.hex()}")
        
        # Collatz XOR
        xor_data = crypto.xor_with_collatz(data)
        log(f"\n[ADIM 2] Collatz XOR:")
        log(f"  Hex: {xor_data.hex()}")
        
        # Affine Cipher
        affine_data = crypto.affine_encrypt(xor_data)
        log(f"\n[ADIM 3] Affine Cipher (a={affine_a}, b={affine_b}):")
        log(f"  Hex: {affine_data.hex()}")
        
        # Transposition
        trans_data = crypto.transpose_encrypt(affine_data)
        log(f"\n[ADIM 4] Transposition (key={trans_key}):")
        log(f"  Hex: {trans_data.hex()}")
        
        # Bit analizi
        bit_string = ''.join(format(b, '08b') for b in trans_data)
        zeros = bit_string.count('0')
        ones = bit_string.count('1')
        
        log(f"\n[BIT ANALIZI]")
        log(f"  Toplam bit: {len(bit_string)}")
        log(f"  0 sayisi: {zeros}")
        log(f"  1 sayisi: {ones}")
        log(f"  Denge orani (0/1): {zeros/ones:.4f}")
        
        # Sifrelenmis metin
        ciphertext = trans_data.hex()
        log(f"\n[SONUC] Sifreli Metin: {ciphertext}")
        
        # Simdi cozum
        log(f"\n[SIFRE COZME]")
        decrypted = crypto.decrypt(ciphertext, original_length=len(text))
        decrypted = decrypted.strip()  # Print olmadan
        
        # Dogrulama
        if decrypted == text:
            log(f"  Cozulmus: \"{decrypted}\"")
            log(f"  DOGRULAMA: BASARILI")
        else:
            log(f"  Cozulmus: \"{decrypted}\"")
            log(f"  DOGRULAMA: BASARISIZ")
    
    log("\n" + "=" * 70)
    log("ANAHTAR URETECI ORNEKLERI")
    log("=" * 70)
    
    generator = KeyGenerator()
    
    log("\n[RASTGELE ANAHTAR SETLERI]")
    for i in range(3):
        keyset = generator.generate_full_keyset(trans_key_length=4)
        exported = generator.export_key(keyset)
        log(f"\n  Anahtar #{i+1}:")
        log(f"    Seed: {keyset['collatz_seed']}")
        log(f"    Affine a: {keyset['affine_a']}")
        log(f"    Affine b: {keyset['affine_b']}")
        log(f"    Trans Key: {keyset['transposition_key']}")
        log(f"    Export: {exported}")
    
    log("\n" + "=" * 70)
    log("COLLATZ DIZISI ORNEKLERI")
    log("=" * 70)
    
    for seed_val in [27, 42, 100]:
        log(f"\n[Seed = {seed_val}]")
        analysis = generator.analyze_collatz_seed(seed_val, bits_needed=64)
        log(f"  64 bit uretimi:")
        log(f"  0 sayisi: {analysis['zeros']}")
        log(f"  1 sayisi: {analysis['ones']}")
        log(f"  Denge: {analysis['balance_ratio']:.4f}")
    
    log("\n" + "=" * 70)
    log("TEST TAMAMLANDI")
    log("=" * 70)
    
    # Dosyaya kaydet
    with open("examples/sample_outputs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    print("\n[INFO] Ciktilar 'examples/sample_outputs.txt' dosyasina kaydedildi.")


def run_without_print():
    """Print'siz versiyon - sadece sonuclari dondur."""
    crypto = CollatzCrypto(seed=27, affine_a=5, affine_b=8, trans_key="3142")
    
    results = []
    
    test_texts = [
        "Hello World",
        "Cryptography Test 123",
        "ABCDEFGHIJKLMNOP",
        "The quick brown fox jumps over the lazy dog"
    ]
    
    for text in test_texts:
        # Sifrele (print'leri gizle)
        data = text.encode('utf-8')
        original_length = len(data)
        
        data = crypto.xor_with_collatz(data)
        data = crypto.affine_encrypt(data)
        data = crypto.transpose_encrypt(data)
        ciphertext = data.hex()
        
        # Bit analizi
        bit_string = ''.join(format(b, '08b') for b in data)
        zeros = bit_string.count('0')
        ones = bit_string.count('1')
        
        results.append({
            'plaintext': text,
            'ciphertext': ciphertext,
            'zeros': zeros,
            'ones': ones,
            'balance': zeros/ones if ones > 0 else 0
        })
    
    return results


if __name__ == '__main__':
    run_examples()
