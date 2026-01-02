#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
İstatistiksel Testler
=====================
Şifreleme algoritmasının rastgelelik kalitesini ölçen testler.
"""

import numpy as np
from scipy import stats
from typing import List, Dict, Tuple
from collatz_crypto import CollatzCrypto


def bits_to_list(data: bytes) -> List[int]:
    """Byte dizisini bit listesine dönüştür."""
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def monobit_test(bits: List[int]) -> Dict:
    """
    Monobit (Frekans) Testi
    Bit dizisindeki 0 ve 1'lerin dağılımını kontrol eder.
    H0: Bitler eşit dağılmış (p > 0.01)
    """
    n = len(bits)
    ones = sum(bits)
    zeros = n - ones
    
    # Test istatistiği
    s_obs = abs(ones - zeros) / np.sqrt(n)
    p_value = 2 * (1 - stats.norm.cdf(s_obs))
    
    return {
        'test_name': 'Monobit (Frekans) Testi',
        'n': n, 'ones': ones, 'zeros': zeros,
        's_obs': s_obs, 'p_value': p_value,
        'passed': p_value >= 0.01,
        'interpretation': 'Rastgele' if p_value >= 0.01 else 'Rastgele değil'
    }


def chi_square_test(bits: List[int], block_size: int = 8) -> Dict:
    """
    Ki-Kare Testi
    Bloklar halinde bit dağılımını kontrol eder.
    """
    n_blocks = len(bits) // block_size
    if n_blocks == 0:
        return {'test_name': 'Ki-Kare Testi', 'error': 'Yetersiz veri'}
    
    block_sums = []
    for i in range(n_blocks):
        block = bits[i * block_size:(i + 1) * block_size]
        block_sums.append(sum(block))
    
    # Her blokta beklenen 1 sayısı
    expected = block_size / 2
    
    # Ki-kare istatistiği
    chi_sq = sum((obs - expected) ** 2 / expected for obs in block_sums)
    df = n_blocks - 1
    p_value = 1 - stats.chi2.cdf(chi_sq, df)
    
    return {
        'test_name': 'Ki-Kare Testi',
        'chi_square': chi_sq, 'degrees_of_freedom': df,
        'p_value': p_value, 'passed': p_value >= 0.01,
        'interpretation': 'Rastgele' if p_value >= 0.01 else 'Rastgele değil'
    }


def runs_test(bits: List[int]) -> Dict:
    """
    Runs Testi
    Ardışık aynı bitlerin (run) sayısını kontrol eder.
    """
    n = len(bits)
    ones = sum(bits)
    pi = ones / n
    
    # Ön koşul kontrolü
    tau = 2 / np.sqrt(n)
    if abs(pi - 0.5) >= tau:
        return {
            'test_name': 'Runs Testi',
            'passed': False,
            'interpretation': 'Monobit testi başarısız, runs testi uygulanamaz'
        }
    
    # Run sayısını hesapla
    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i-1]:
            runs += 1
    
    # Test istatistiği
    expected_runs = 2 * n * pi * (1 - pi) + 1
    variance = 2 * n * pi * (1 - pi) * (1 - 2 * pi * (1 - pi) / n)
    
    if variance <= 0:
        return {'test_name': 'Runs Testi', 'error': 'Varyans hesaplanamadi', 'passed': True}
    
    std_runs = np.sqrt(abs(variance))
    
    if std_runs == 0:
        return {'test_name': 'Runs Testi', 'error': 'Standart sapma sifir', 'passed': True}
    
    z = (runs - expected_runs) / std_runs
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    return {
        'test_name': 'Runs Testi',
        'runs': runs, 'expected': expected_runs,
        'z_score': z, 'p_value': p_value,
        'passed': p_value >= 0.01,
        'interpretation': 'Rastgele' if p_value >= 0.01 else 'Rastgele değil'
    }


def frequency_analysis(data: bytes) -> Dict:
    """Byte frekans analizi."""
    freq = [0] * 256
    for byte in data:
        freq[byte] += 1
    
    n = len(data)
    expected = n / 256
    chi_sq = sum((f - expected) ** 2 / expected for f in freq if expected > 0)
    df = 255
    p_value = 1 - stats.chi2.cdf(chi_sq, df)
    
    non_zero = sum(1 for f in freq if f > 0)
    
    return {
        'test_name': 'Byte Frekans Analizi',
        'total_bytes': n, 'unique_bytes': non_zero,
        'chi_square': chi_sq, 'p_value': p_value,
        'passed': p_value >= 0.01,
        'interpretation': 'Düzgün dağılmış' if p_value >= 0.01 else 'Düzgün dağılmamış'
    }


def run_all_tests(ciphertext_hex: str) -> List[Dict]:
    """Tüm testleri çalıştır."""
    data = bytes.fromhex(ciphertext_hex)
    bits = bits_to_list(data)
    
    return [
        monobit_test(bits),
        chi_square_test(bits),
        runs_test(bits),
        frequency_analysis(data)
    ]


def print_results(results: List[Dict]):
    """Sonuçları formatla ve yazdır."""
    print("\n" + "="*70)
    print("📊 İSTATİSTİKSEL TEST SONUÇLARI")
    print("="*70)
    
    passed = 0
    for r in results:
        print(f"\n🧪 {r['test_name']}")
        print("-" * 40)
        for k, v in r.items():
            if k != 'test_name':
                if isinstance(v, float):
                    print(f"   {k}: {v:.6f}")
                else:
                    print(f"   {k}: {v}")
        if r.get('passed'):
            passed += 1
            print("   ✅ TEST BAŞARILI")
        else:
            print("   ❌ TEST BAŞARISIZ")
    
    print("\n" + "="*70)
    print(f"📈 ÖZET: {passed}/{len(results)} test başarılı")
    print("="*70)


def main():
    """Demo: Örnek metin şifrele ve test et."""
    print("\n🔬 Collatz Kriptografik Algoritma - İstatistiksel Testler")
    print("="*70)
    
    # Test metinleri
    test_texts = [
        "Merhaba Dünya! Bu bir test mesajıdır.",
        "The quick brown fox jumps over the lazy dog.",
        "0123456789ABCDEF" * 10
    ]
    
    crypto = CollatzCrypto(seed=27, affine_a=5, affine_b=8, trans_key="3142")
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*70}")
        print(f"📝 TEST #{i}: {text[:30]}...")
        
        ciphertext, metadata = crypto.encrypt(text)
        print(f"\n📊 Şifreleme Metadata:")
        print(f"   Uzunluk: {metadata['encrypted_length']} byte")
        print(f"   0'lar: {metadata['zeros']}, 1'ler: {metadata['ones']}")
        print(f"   Denge Oranı: {metadata['balance_ratio']:.4f}")
        
        results = run_all_tests(ciphertext)
        print_results(results)


if __name__ == '__main__':
    main()
