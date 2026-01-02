#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anahtar Üreteci (Key Generator)
===============================
Collatz tabanlı kriptografik algoritma için güvenli anahtar üretimi.
"""

import random
import math
import secrets
from typing import Tuple, Dict


class KeyGenerator:
    """Kriptografik anahtar üreteci sınıfı."""
    
    def __init__(self, modulus: int = 256):
        self.modulus = modulus
        self.valid_a_values = [a for a in range(1, modulus) if math.gcd(a, modulus) == 1]
    
    def generate_collatz_seed(self, min_val: int = 10, max_val: int = 1000) -> int:
        """Rastgele Collatz seed değeri üret."""
        return secrets.randbelow(max_val - min_val) + min_val
    
    def analyze_collatz_seed(self, seed: int, bits_needed: int = 256) -> Dict:
        """Bir Collatz seed'inin kalitesini analiz et."""
        bits = []
        current = seed
        steps = 0
        
        while len(bits) < bits_needed:
            if current == 1:
                current = seed
            if current % 2 == 0:
                bits.append(0)
                current = current // 2
            else:
                bits.append(1)
                current = 3 * current + 1
            steps += 1
        
        zeros = bits.count(0)
        ones = bits.count(1)
        return {
            'seed': seed, 'total_bits': len(bits), 'zeros': zeros,
            'ones': ones, 'balance_ratio': zeros / ones if ones > 0 else float('inf')
        }
    
    def generate_affine_params(self) -> Tuple[int, int]:
        """Geçerli Affine cipher parametreleri üret."""
        a = secrets.choice(self.valid_a_values)
        b = secrets.randbelow(self.modulus)
        return a, b
    
    def validate_affine_a(self, a: int) -> bool:
        return math.gcd(a, self.modulus) == 1
    
    def mod_inverse(self, a: int) -> int:
        """a değerinin modüler tersini hesapla."""
        def extended_gcd(a, b):
            if a == 0: return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            return gcd, y1 - (b // a) * x1, x1
        _, x, _ = extended_gcd(a % self.modulus, self.modulus)
        return (x % self.modulus + self.modulus) % self.modulus
    
    def generate_transposition_key(self, length: int = 4) -> str:
        """Rastgele transposition anahtarı üret."""
        nums = list(range(1, length + 1))
        random.shuffle(nums)
        return ''.join(map(str, nums))
    
    def validate_transposition_key(self, key: str) -> Tuple[bool, str]:
        if not key.isdigit():
            return False, "Anahtar sadece rakamlardan oluşmalı"
        nums = [int(c) for c in key]
        if len(nums) != len(set(nums)):
            return False, "Rakamlar benzersiz olmalı"
        if set(nums) != set(range(1, len(nums) + 1)):
            return False, f"Anahtar 1'den {len(nums)}'e kadar rakamları içermeli"
        return True, "Geçerli anahtar"
    
    def generate_full_keyset(self, trans_key_length: int = 4) -> Dict:
        """Tam bir anahtar seti üret."""
        seed = self.generate_collatz_seed()
        affine_a, affine_b = self.generate_affine_params()
        trans_key = self.generate_transposition_key(trans_key_length)
        return {
            'collatz_seed': seed, 'affine_a': affine_a, 'affine_b': affine_b,
            'affine_a_inverse': self.mod_inverse(affine_a),
            'transposition_key': trans_key, 'modulus': self.modulus
        }
    
    def export_key(self, keyset: Dict) -> str:
        return f"{keyset['collatz_seed']}:{keyset['affine_a']}:{keyset['affine_b']}:{keyset['transposition_key']}"
    
    def import_key(self, key_string: str) -> Dict:
        parts = key_string.split(':')
        if len(parts) != 4:
            raise ValueError("Geçersiz anahtar formatı. Beklenen: SEED:A:B:TRANSKEY")
        seed, affine_a, affine_b, trans_key = int(parts[0]), int(parts[1]), int(parts[2]), parts[3]
        if not self.validate_affine_a(affine_a):
            raise ValueError(f"Geçersiz Affine 'a' değeri: {affine_a}")
        valid, msg = self.validate_transposition_key(trans_key)
        if not valid:
            raise ValueError(f"Geçersiz transposition anahtarı: {msg}")
        return {
            'collatz_seed': seed, 'affine_a': affine_a, 'affine_b': affine_b,
            'affine_a_inverse': self.mod_inverse(affine_a),
            'transposition_key': trans_key, 'modulus': self.modulus
        }


def main():
    print("\n" + "="*60)
    print("🔑 ANAHTAR ÜRETECİ (KEY GENERATOR)")
    print("="*60)
    
    generator = KeyGenerator()
    keyset = generator.generate_full_keyset(trans_key_length=4)
    
    print("\n🔐 Üretilen Anahtar Seti:")
    for key, value in keyset.items():
        print(f"   {key}: {value}")
    
    exported = generator.export_key(keyset)
    print(f"\n📤 Dışa Aktarılmış Anahtar: {exported}")
    
    print("\n📊 Collatz Seed Analizi:")
    analysis = generator.analyze_collatz_seed(keyset['collatz_seed'])
    for key, value in analysis.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*60)


if __name__ == '__main__':
    main()
