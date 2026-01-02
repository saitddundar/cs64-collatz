#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Istatistiksel Test Sonuclari Olusturucu
=======================================
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from scipy import stats
from collatz_crypto import CollatzCrypto


def bits_to_list(data):
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def monobit_test(bits):
    n = len(bits)
    ones = sum(bits)
    zeros = n - ones
    s_obs = abs(ones - zeros) / np.sqrt(n)
    p_value = 2 * (1 - stats.norm.cdf(s_obs))
    return {
        'test_name': 'Monobit (Frekans) Testi',
        'n': n, 'ones': ones, 'zeros': zeros,
        's_obs': s_obs, 'p_value': p_value,
        'passed': p_value >= 0.01
    }


def chi_square_test(bits, block_size=8):
    n_blocks = len(bits) // block_size
    if n_blocks == 0:
        return {'test_name': 'Ki-Kare Testi', 'error': 'Yetersiz veri', 'passed': False}
    
    block_sums = []
    for i in range(n_blocks):
        block = bits[i * block_size:(i + 1) * block_size]
        block_sums.append(sum(block))
    
    expected = block_size / 2
    chi_sq = sum((obs - expected) ** 2 / expected for obs in block_sums)
    df = n_blocks - 1
    p_value = 1 - stats.chi2.cdf(chi_sq, df)
    
    return {
        'test_name': 'Ki-Kare Testi',
        'chi_square': chi_sq, 'degrees_of_freedom': df,
        'p_value': p_value, 'passed': p_value >= 0.01
    }


def runs_test(bits):
    n = len(bits)
    ones = sum(bits)
    pi = ones / n
    
    tau = 2 / np.sqrt(n)
    if abs(pi - 0.5) >= tau:
        return {
            'test_name': 'Runs Testi',
            'passed': False,
            'note': 'Monobit testi basarisiz, runs testi uygulanamaz'
        }
    
    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i-1]:
            runs += 1
    
    expected_runs = 2 * n * pi * (1 - pi) + 1
    variance = 2 * n * pi * (1 - pi) * (1 - 2 * pi * (1 - pi) / n)
    
    if variance <= 0:
        return {'test_name': 'Runs Testi', 'passed': True, 'note': 'Varyans hesaplanamadi'}
    
    std_runs = np.sqrt(abs(variance))
    if std_runs == 0:
        return {'test_name': 'Runs Testi', 'passed': True, 'note': 'Std sapma sifir'}
    
    z = (runs - expected_runs) / std_runs
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    return {
        'test_name': 'Runs Testi',
        'runs': runs, 'expected': expected_runs,
        'z_score': z, 'p_value': p_value,
        'passed': p_value >= 0.01
    }


def frequency_analysis(data):
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
        'passed': p_value >= 0.01
    }


def run_tests_and_save():
    output_lines = []
    
    def log(text=""):
        print(text)
        output_lines.append(text)
    
    log("=" * 70)
    log("ISTATISTIKSEL TEST SONUCLARI")
    log("=" * 70)
    
    crypto = CollatzCrypto(seed=27, affine_a=5, affine_b=8, trans_key="3142")
    
    test_texts = [
        "Hello World",
        "The quick brown fox jumps over the lazy dog",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 5,
        "0123456789" * 20
    ]
    
    for i, text in enumerate(test_texts, 1):
        log(f"\n{'='*70}")
        log(f"TEST #{i}: \"{text[:40]}...\"")
        log("=" * 70)
        
        # Sifrele
        data = text.encode('utf-8')
        data = crypto.xor_with_collatz(data)
        data = crypto.affine_encrypt(data)
        data = crypto.transpose_encrypt(data)
        
        bits = bits_to_list(data)
        
        log(f"\nVeri Bilgisi:")
        log(f"  Byte sayisi: {len(data)}")
        log(f"  Bit sayisi: {len(bits)}")
        
        # Testler
        tests = [
            monobit_test(bits),
            chi_square_test(bits),
            runs_test(bits),
            frequency_analysis(data)
        ]
        
        passed_count = 0
        for test in tests:
            log(f"\n[{test['test_name']}]")
            for k, v in test.items():
                if k != 'test_name':
                    if isinstance(v, float):
                        log(f"  {k}: {v:.6f}")
                    else:
                        log(f"  {k}: {v}")
            if test.get('passed'):
                passed_count += 1
                log("  SONUC: BASARILI")
            else:
                log("  SONUC: BASARISIZ")
        
        log(f"\nOZET: {passed_count}/4 test basarili")
    
    log("\n" + "=" * 70)
    log("TUM TESTLER TAMAMLANDI")
    log("=" * 70)
    
    # Dosyaya kaydet
    with open("examples/statistical_test_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    print(f"\n[INFO] Sonuclar 'examples/statistical_test_results.txt' dosyasina kaydedildi.")


if __name__ == '__main__':
    run_tests_and_save()
