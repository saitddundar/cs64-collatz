#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collatz Tabanlı Kriptografik Algoritma
======================================
Affine Cipher ve Transposition (Yer Değiştirme) şifreleme yöntemlerini kullanan,
Collatz sanısına dayalı özgün bir şifreleme algoritması.

Yazar: Mehmet Sait Dündar
"""

import argparse
import math
from typing import Tuple, List


class CollatzCrypto:
    """
    Collatz sanısı üzerine kurulu kriptografik algoritma sınıfı.
    
    Şifreleme Katmanları:
    1. Collatz Dizisi → Bit üretimi (0/1)
    2. Affine Cipher → Matematiksel dönüşüm
    3. Transposition → Pozisyon karıştırma
    """
    
    def __init__(self, seed: int = 27, affine_a: int = 5, affine_b: int = 8, 
                 trans_key: str = "3142", modulus: int = 256):
        """
        Algoritma parametrelerini başlat.
        
        Args:
            seed: Collatz dizisi için başlangıç değeri
            affine_a: Affine cipher için çarpan (m ile aralarında asal olmalı)
            affine_b: Affine cipher için toplam değeri
            trans_key: Transposition için yer değiştirme anahtarı
            modulus: Affine cipher için mod değeri (varsayılan 256 - ASCII)
        """
        self.seed = seed
        self.affine_a = affine_a
        self.affine_b = affine_b
        self.trans_key = trans_key
        self.modulus = modulus
        
        # Affine cipher için a değerinin m ile aralarında asal olduğunu kontrol et
        if math.gcd(affine_a, modulus) != 1:
            raise ValueError(f"Affine 'a' değeri ({affine_a}) modulus ({modulus}) ile aralarında asal olmalı!")
        
        # Ters çarpanı hesapla (şifre çözme için)
        self.affine_a_inverse = self._mod_inverse(affine_a, modulus)
    
    # ==================== COLLATZ DİZİSİ ÜRETİMİ ====================
    
    def generate_collatz_sequence(self, n: int, length: int) -> List[int]:
        """
        Collatz dizisi üret ve bit dizisine dönüştür.
        
        Çift adım → 0
        Tek adım → 1
        
        Args:
            n: Başlangıç sayısı
            length: İstenen bit uzunluğu
            
        Returns:
            0 ve 1'lerden oluşan bit listesi
        """
        bits = []
        current = n
        
        while len(bits) < length:
            if current == 1:
                # 1'e ulaştık, seed'i yeniden başlat
                current = self.seed
            
            if current % 2 == 0:
                bits.append(0)  # Çift → 0
                current = current // 2
            else:
                bits.append(1)  # Tek → 1
                current = 3 * current + 1
        
        return bits[:length]
    
    def balance_bits(self, bits: List[int]) -> Tuple[List[int], int]:
        """
        Bit dizisini eşit sayıda 0 ve 1 içerecek şekilde dengele.
        
        Dengeleme Yöntemi:
        - Fazla olan bit türünden azalt
        - Padding bilgisini sakla
        
        Args:
            bits: Dengelenmemiş bit listesi
            
        Returns:
            (Dengelenmiş bitler, padding uzunluğu)
        """
        count_zeros = bits.count(0)
        count_ones = bits.count(1)
        
        if count_zeros == count_ones:
            return bits, 0
        
        # Uzunluğu çift sayıya yuvarlayalım
        target_length = len(bits)
        if target_length % 2 != 0:
            target_length += 1
        
        half = target_length // 2
        balanced = []
        
        # Önce orijinal bitleri ekle
        zeros_added = 0
        ones_added = 0
        
        for bit in bits:
            if bit == 0 and zeros_added < half:
                balanced.append(0)
                zeros_added += 1
            elif bit == 1 and ones_added < half:
                balanced.append(1)
                ones_added += 1
            elif zeros_added < half:
                balanced.append(0)
                zeros_added += 1
            elif ones_added < half:
                balanced.append(1)
                ones_added += 1
        
        # Eksik bitleri tamamla
        while zeros_added < half:
            balanced.append(0)
            zeros_added += 1
        while ones_added < half:
            balanced.append(1)
            ones_added += 1
        
        padding = len(balanced) - len(bits)
        return balanced, padding
    
    # ==================== AFFINE CIPHER ====================
    
    def _mod_inverse(self, a: int, m: int) -> int:
        """
        Modüler ters çarpanı hesapla (Extended Euclidean Algorithm).
        
        Args:
            a: Tersini bulacağımız sayı
            m: Modulus
            
        Returns:
            a'nın mod m altında tersi
        """
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        _, x, _ = extended_gcd(a % m, m)
        return (x % m + m) % m
    
    def affine_encrypt_byte(self, byte_val: int) -> int:
        """
        Tek bir byte'ı Affine cipher ile şifrele.
        
        Formül: E(x) = (a × x + b) mod m
        
        Args:
            byte_val: Şifrelenecek byte değeri (0-255)
            
        Returns:
            Şifrelenmiş byte değeri
        """
        return (self.affine_a * byte_val + self.affine_b) % self.modulus
    
    def affine_decrypt_byte(self, byte_val: int) -> int:
        """
        Tek bir byte'ı Affine cipher ile çöz.
        
        Formül: D(y) = a^(-1) × (y - b) mod m
        
        Args:
            byte_val: Çözülecek byte değeri (0-255)
            
        Returns:
            Çözülmüş byte değeri
        """
        return (self.affine_a_inverse * (byte_val - self.affine_b)) % self.modulus
    
    def affine_encrypt(self, data: bytes) -> bytes:
        """
        Byte dizisini Affine cipher ile şifrele.
        
        Args:
            data: Şifrelenecek veri
            
        Returns:
            Şifrelenmiş veri
        """
        return bytes([self.affine_encrypt_byte(b) for b in data])
    
    def affine_decrypt(self, data: bytes) -> bytes:
        """
        Byte dizisini Affine cipher ile çöz.
        
        Args:
            data: Çözülecek veri
            
        Returns:
            Çözülmüş veri
        """
        return bytes([self.affine_decrypt_byte(b) for b in data])
    
    # ==================== TRANSPOSITION CIPHER ====================
    
    def _parse_trans_key(self) -> List[int]:
        """
        Transposition anahtarını sayısal diziye dönüştür.
        
        Örnek: "3142" → [3, 1, 4, 2] → [2, 0, 3, 1] (0-indexed sıralama)
        
        Returns:
            Pozisyon değiştirme dizisi
        """
        # Anahtarı sayılara dönüştür
        key_nums = [int(c) for c in self.trans_key]
        
        # Sıralama pozisyonlarını bul (0-indexed)
        sorted_positions = []
        sorted_key = sorted(enumerate(key_nums), key=lambda x: x[1])
        
        result = [0] * len(key_nums)
        for new_pos, (old_pos, _) in enumerate(sorted_key):
            result[old_pos] = new_pos
            
        return result
    
    def transpose_encrypt(self, data: bytes) -> bytes:
        """
        Veriyi transposition cipher ile şifrele.
        
        Veriyi anahtar uzunluğundaki bloklara böl ve her bloğu
        anahtar sırasına göre yeniden düzenle.
        
        Args:
            data: Şifrelenecek veri
            
        Returns:
            Şifrelenmiş veri
        """
        key_order = self._parse_trans_key()
        key_len = len(key_order)
        
        # Veriyi bloklara böl
        result = bytearray()
        
        for i in range(0, len(data), key_len):
            block = data[i:i + key_len]
            
            # Blok eksikse padding ekle
            if len(block) < key_len:
                block = block + bytes([0] * (key_len - len(block)))
            
            # Bloğu yeniden sırala
            new_block = [0] * key_len
            for old_pos, new_pos in enumerate(key_order):
                new_block[new_pos] = block[old_pos]
            
            result.extend(new_block)
        
        return bytes(result)
    
    def transpose_decrypt(self, data: bytes) -> bytes:
        """
        Transposition cipher ile şifrelenmiş veriyi çöz.
        
        Args:
            data: Çözülecek veri
            
        Returns:
            Çözülmüş veri
        """
        key_order = self._parse_trans_key()
        key_len = len(key_order)
        
        # Ters sıralama oluştur
        reverse_order = [0] * key_len
        for old_pos, new_pos in enumerate(key_order):
            reverse_order[new_pos] = old_pos
        
        result = bytearray()
        
        for i in range(0, len(data), key_len):
            block = data[i:i + key_len]
            
            # Bloğu eski haline getir
            new_block = [0] * key_len
            for old_pos, new_pos in enumerate(reverse_order):
                if old_pos < len(block):
                    new_block[new_pos] = block[old_pos]
            
            result.extend(new_block)
        
        return bytes(result)
    
    # ==================== XOR İŞLEMİ (Collatz ile) ====================
    
    def xor_with_collatz(self, data: bytes, encrypt: bool = True) -> bytes:
        """
        Veriyi Collatz dizisinden üretilen bitlerle XOR'la.
        
        Args:
            data: İşlenecek veri
            encrypt: True ise şifreleme, False ise çözme
            
        Returns:
            XOR'lanmış veri
        """
        # Her byte için 8 bit gerekli
        needed_bits = len(data) * 8
        collatz_bits = self.generate_collatz_sequence(self.seed, needed_bits)
        
        # Bitleri byte'lara dönüştür
        collatz_bytes = []
        for i in range(0, len(collatz_bits), 8):
            byte_bits = collatz_bits[i:i+8]
            byte_val = 0
            for bit in byte_bits:
                byte_val = (byte_val << 1) | bit
            collatz_bytes.append(byte_val)
        
        # XOR işlemi
        result = bytes([d ^ c for d, c in zip(data, collatz_bytes)])
        return result
    
    # ==================== ANA ŞİFRELEME/ÇÖZME ====================
    
    def encrypt(self, plaintext: str) -> Tuple[str, dict]:
        """
        Metni tamamen şifrele.
        
        Şifreleme Zinciri:
        1. Metin → Byte'lar
        2. Collatz XOR
        3. Affine Cipher
        4. Transposition
        5. Hex çıktı
        
        Args:
            plaintext: Şifrelenecek düz metin
            
        Returns:
            (Şifrelenmiş hex string, metadata dictionary)
        """
        # Metin → Byte
        data = plaintext.encode('utf-8')
        original_length = len(data)
        
        print(f"[1] Orijinal veri: {data.hex()}")
        
        # Collatz XOR
        data = self.xor_with_collatz(data, encrypt=True)
        print(f"[2] Collatz XOR sonrası: {data.hex()}")
        
        # Affine Cipher
        data = self.affine_encrypt(data)
        print(f"[3] Affine Cipher sonrası: {data.hex()}")
        
        # Transposition
        data = self.transpose_encrypt(data)
        print(f"[4] Transposition sonrası: {data.hex()}")
        
        # Bit dağılımını analiz et
        bit_string = ''.join(format(b, '08b') for b in data)
        zeros = bit_string.count('0')
        ones = bit_string.count('1')
        
        metadata = {
            'original_length': original_length,
            'encrypted_length': len(data),
            'zeros': zeros,
            'ones': ones,
            'balance_ratio': zeros / ones if ones > 0 else float('inf')
        }
        
        return data.hex(), metadata
    
    def decrypt(self, ciphertext_hex: str, original_length: int = None) -> str:
        """
        Şifreli metni çöz.
        
        Çözme Zinciri (ters sıra):
        1. Hex → Byte
        2. Transposition (ters)
        3. Affine Cipher (ters)
        4. Collatz XOR
        5. Byte → Metin
        
        Args:
            ciphertext_hex: Şifrelenmiş hex string
            original_length: Orijinal veri uzunluğu (padding için)
            
        Returns:
            Çözülmüş düz metin
        """
        # Hex → Byte
        data = bytes.fromhex(ciphertext_hex)
        
        print(f"[1] Şifreli veri: {data.hex()}")
        
        # Transposition (ters)
        data = self.transpose_decrypt(data)
        print(f"[2] Transposition çözümü sonrası: {data.hex()}")
        
        # Affine Cipher (ters)
        data = self.affine_decrypt(data)
        print(f"[3] Affine çözümü sonrası: {data.hex()}")
        
        # Collatz XOR
        data = self.xor_with_collatz(data, encrypt=False)
        print(f"[4] Collatz XOR sonrası: {data.hex()}")
        
        # Orijinal uzunluğa kırp (padding'i kaldır)
        if original_length:
            data = data[:original_length]
        
        # Byte → Metin
        return data.decode('utf-8', errors='replace')
    
    # ==================== ANAHTAR BİLGİSİ ====================
    
    def get_key_info(self) -> dict:
        """
        Mevcut anahtar bilgilerini döndür.
        
        Returns:
            Anahtar parametreleri sözlüğü
        """
        return {
            'seed': self.seed,
            'affine_a': self.affine_a,
            'affine_b': self.affine_b,
            'affine_a_inverse': self.affine_a_inverse,
            'modulus': self.modulus,
            'trans_key': self.trans_key
        }


def main():
    """Ana program giriş noktası."""
    parser = argparse.ArgumentParser(
        description='Collatz Tabanlı Kriptografik Algoritma',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  Şifreleme:
    python collatz_crypto.py encrypt "Merhaba Dünya"
    python collatz_crypto.py encrypt "Gizli Mesaj" --seed 42 --affine-a 7 --affine-b 13

  Şifre Çözme:
    python collatz_crypto.py decrypt "HEXSTRING" --original-length 13
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Komut seçin')
    
    # Şifreleme komutu
    encrypt_parser = subparsers.add_parser('encrypt', help='Metin şifrele')
    encrypt_parser.add_argument('text', help='Şifrelenecek metin')
    encrypt_parser.add_argument('--seed', type=int, default=27, 
                                help='Collatz seed değeri (varsayılan: 27)')
    encrypt_parser.add_argument('--affine-a', type=int, default=5,
                                help='Affine çarpan (varsayılan: 5)')
    encrypt_parser.add_argument('--affine-b', type=int, default=8,
                                help='Affine toplam (varsayılan: 8)')
    encrypt_parser.add_argument('--trans-key', type=str, default='3142',
                                help='Transposition anahtarı (varsayılan: 3142)')
    
    # Çözme komutu
    decrypt_parser = subparsers.add_parser('decrypt', help='Şifre çöz')
    decrypt_parser.add_argument('ciphertext', help='Şifrelenmiş hex string')
    decrypt_parser.add_argument('--seed', type=int, default=27,
                                help='Collatz seed değeri')
    decrypt_parser.add_argument('--affine-a', type=int, default=5,
                                help='Affine çarpan')
    decrypt_parser.add_argument('--affine-b', type=int, default=8,
                                help='Affine toplam')
    decrypt_parser.add_argument('--trans-key', type=str, default='3142',
                                help='Transposition anahtarı')
    decrypt_parser.add_argument('--original-length', type=int,
                                help='Orijinal veri uzunluğu')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        crypto = CollatzCrypto(
            seed=args.seed,
            affine_a=args.affine_a,
            affine_b=args.affine_b,
            trans_key=args.trans_key
        )
        
        print("\n" + "="*60)
        print("🔐 COLLATZ KRİPTOGRAFİK ALGORİTMA")
        print("="*60)
        
        print(f"\n📋 Anahtar Bilgileri:")
        key_info = crypto.get_key_info()
        for key, value in key_info.items():
            print(f"   {key}: {value}")
        
        if args.command == 'encrypt':
            print(f"\n📝 Orijinal Metin: {args.text}")
            print("\n🔄 Şifreleme Adımları:")
            
            ciphertext, metadata = crypto.encrypt(args.text)
            
            print(f"\n🔒 Şifreli Metin (Hex): {ciphertext}")
            print(f"\n📊 Metadata:")
            for key, value in metadata.items():
                print(f"   {key}: {value}")
                
        elif args.command == 'decrypt':
            print(f"\n🔒 Şifreli Metin: {args.ciphertext}")
            print("\n🔄 Çözme Adımları:")
            
            plaintext = crypto.decrypt(
                args.ciphertext, 
                original_length=args.original_length
            )
            
            print(f"\n📝 Çözülmüş Metin: {plaintext}")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        return 1


if __name__ == '__main__':
    main()
