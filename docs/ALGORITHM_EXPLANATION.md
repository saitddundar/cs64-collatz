# 📚 ALGORİTMA AÇIKLAMASI

## Collatz Tabanlı Kriptografik Algoritma

---

## 1. 🎯 GİRİŞ

Bu algoritma, **Collatz Sanısı** üzerine kurulu, iki katmanlı şifreleme sisteminden oluşan özgün bir kriptografik yöntemdir:

1. **Affine Cipher** - Matematiksel dönüşüm
2. **Transposition Cipher** - Pozisyon karıştırma

---

## 2. 🔢 COLLATZ SANISI

### Tanım
Collatz sanısı, herhangi bir pozitif tam sayı için tekrarlanan işlemlerle sonunda 1'e ulaşılacağını öne sürer:

| Koşul | İşlem |
|-------|-------|
| Sayı **çift** | `n → n / 2` |
| Sayı **tek** | `n → 3n + 1` |

### Örnek: n = 27
```
27 → 82 → 41 → 124 → 62 → 31 → 94 → 47 → 142 → ...
```

### Kriptografide Kullanımı
Her adımda:
- **Çift sayıya gidildi** → `0` biti
- **Tek sayıya gidildi** → `1` biti

Bu sayede deterministik ama tahmin edilmesi zor bir bit dizisi üretilir.

---

## 3. 🔐 AFFINE CIPHER

### Matematiksel Tanım

**Şifreleme:**
```
E(x) = (a × x + b) mod m
```

**Şifre Çözme:**
```
D(y) = a⁻¹ × (y - b) mod m
```

### Parametreler

| Parametre | Açıklama | Kısıtlama |
|-----------|----------|-----------|
| `a` | Çarpan | `gcd(a, m) = 1` (aralarında asal) |
| `b` | Toplam | `0 ≤ b < m` |
| `m` | Modulus | 256 (byte için) |
| `a⁻¹` | a'nın tersi | Extended Euclidean Algorithm |

### Örnek
```
a = 5, b = 8, m = 256

Şifreleme: E(65) = (5 × 65 + 8) mod 256 = 333 mod 256 = 77
Şifre Çözme: D(77) = 205 × (77 - 8) mod 256 = 205 × 69 mod 256 = 65

Not: 205, 5'in mod 256'daki tersidir.
```

### Neden Affine?
- **Geri Dönüşlü:** Her karakterin benzersiz bir şifreli karşılığı var
- **Anahtara Bağlı:** a ve b değerleri gizli tutulur
- **Hızlı:** Sadece çarpma ve toplama işlemleri

---

## 4. 🔀 TRANSPOSITION CIPHER

### Çalışma Prensibi

Veriyi bloklara böl ve her bloğu belirli bir anahtara göre yeniden sırala.

### Örnek

**Anahtar:** `3142`
**Yorumlama:** 3. harf önce, 1. harf ikinci, 4. harf üçüncü, 2. harf son

**Orijinal Blok:** `ABCD`
**Şifreli Blok:** `BADC`

```
Pozisyon:  1  2  3  4
Orijinal:  A  B  C  D
Anahtar:   3  1  4  2
Yeni Poz:  2  4  1  3
Sonuç:     B  A  D  C → BADC
```

### Neden Transposition?
- **Difüzyon:** Karakterlerin konumları değişir
- **Konfüzyon:** Orijinal yapı gizlenir
- **Katmanlı Güvenlik:** Affine ile birlikte çok daha güçlü

---

## 5. 🔗 ŞİFRELEME ZİNCİRİ

### Adım 1: Metin → Byte
```
"AB" → [65, 66]
```

### Adım 2: Collatz XOR
Collatz dizisinden üretilen bitlerle XOR:
```
[65, 66] XOR [23, 87] → [86, 117]
```

### Adım 3: Affine Cipher
Her byte'a Affine uygula:
```
E(86) = (5 × 86 + 8) mod 256 = 182
E(117) = (5 × 117 + 8) mod 256 = 73
Sonuç: [182, 73]
```

### Adım 4: Transposition
Blokları yeniden sırala:
```
[182, 73, 0, 0] → key "3142" → [73, 0, 182, 0]
```

### Adım 5: Hex Çıktı
```
[73, 0, 182, 0] → "4900b600"
```

---

## 6. 🔓 ŞİFRE ÇÖZME ZİNCİRİ (Ters Sıra)

1. **Hex → Byte**
2. **Transposition (ters)** - Ters anahtar sıralaması
3. **Affine (ters)** - `D(y) = a⁻¹ × (y - b) mod m`
4. **Collatz XOR** - Aynı XOR işlemi (A ⊕ B ⊕ B = A)
5. **Byte → Metin**

---

## 7. 🔑 ANAHTAR YAPISI

Tam anahtar 4 bileşenden oluşur:

```
SEED:AFFINE_A:AFFINE_B:TRANS_KEY
Örnek: 27:5:8:3142
```

| Bileşen | Değer | Açıklama |
|---------|-------|----------|
| Seed | 27 | Collatz başlangıç değeri |
| a | 5 | Affine çarpan |
| b | 8 | Affine toplam |
| Trans Key | 3142 | Transposition sıralaması |

---

## 8. ⚖️ 0/1 DENGESİ

### Problem
Şifreli metinde eşit sayıda 0 ve 1 olması isteniyor.

### Çözüm
1. Şifreleme sonrası bit dağılımını analiz et
2. Collatz seed seçimi ile dengeyi optimize et
3. İstatistiksel testlerle doğrula

### Doğal Denge
Collatz dizisi doğal olarak belirli bir dengeye sahiptir:
- Çift adımlar (0) genellikle biraz daha fazla
- Affine ve Transposition bu dengeyi dağıtır

---

## 9. 🛡️ GÜVENLİK ANALİZİ

### Güçlü Yönler
- **Çok Katmanlı:** 3 farklı şifreleme katmanı
- **Anahtar Uzayı:** Geniş anahtar kombinasyonları
- **Difüzyon:** Transposition ile karakter yayılımı
- **Konfüzyon:** Affine ve XOR ile değer gizleme

### Zayıf Yönler (Eğitim Amaçlı)
- Affine cipher tek başına frekans analizine karşı zayıf
- Collatz dizisi deterministik
- Modern standartlara (AES, RSA) kıyasla basit

### Öneriler
Bu algoritma **eğitim amaçlıdır**. Gerçek uygulamalarda AES, ChaCha20 gibi standart algoritmalar tercih edilmelidir.

---

## 10. 📊 KARMAŞIKLIK ANALİZİ

| İşlem | Zaman | Alan |
|-------|-------|------|
| Collatz Üretimi | O(n) | O(n) |
| Affine Şifreleme | O(n) | O(1) |
| Transposition | O(n) | O(k) |
| **Toplam** | **O(n)** | **O(n)** |

n: Veri uzunluğu, k: Transposition anahtar uzunluğu

---

## 11. 🧪 TEST VE DOĞRULAMA

### Kullanılan Testler
1. **Monobit Testi** - 0/1 frekans dağılımı
2. **Ki-Kare Testi** - Blok bazlı rastgelelik
3. **Runs Testi** - Ardışık bit analizi
4. **Frekans Analizi** - Byte dağılımı

### Başarı Kriterleri
- p-value ≥ 0.01: Test başarılı (rastgele davranış)
- p-value < 0.01: Test başarısız (örüntü tespit edildi)

---

## 12. 📝 ÖRNEK KULLANIM

```python
from collatz_crypto import CollatzCrypto

# Şifreleme
crypto = CollatzCrypto(seed=27, affine_a=5, affine_b=8, trans_key="3142")
ciphertext, metadata = crypto.encrypt("Gizli Mesaj")
print(f"Şifreli: {ciphertext}")

# Şifre Çözme
plaintext = crypto.decrypt(ciphertext, metadata['original_length'])
print(f"Çözülmüş: {plaintext}")
```

---

## 13. 🎓 SONUÇ

Bu algoritma, kriptografi temellerini anlamak için tasarlanmış eğitimsel bir projedir:

- ✅ Collatz sanısının bit üretiminde kullanımı
- ✅ Affine cipher matematiksel dönüşümü
- ✅ Transposition ile pozisyon karıştırma
- ✅ Çok katmanlı şifreleme yapısı
- ✅ İstatistiksel test ve doğrulama

**Başarılar! 🚀**
