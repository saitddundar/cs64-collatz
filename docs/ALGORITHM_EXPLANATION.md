# ALGORITMA ACIKLAMASI

## Collatz Tabanli Kriptografik Algoritma

---

## 1. GIRIS

Bu algoritma, **Collatz Sanisi** uzerine kurulu, iki katmanli sifreleme sisteminden olusan ozgun bir kriptografik yontemdir:

1. **Affine Cipher** - Matematiksel donusum
2. **Transposition Cipher** - Pozisyon karistirma

---

## 2. COLLATZ SANISI

### Tanim
Collatz sanisi, herhangi bir pozitif tam sayi icin tekrarlanan islemlerle sonunda 1'e ulasilacagini one surer:

| Kosul | Islem |
|-------|-------|
| Sayi **cift** | `n -> n / 2` |
| Sayi **tek** | `n -> 3n + 1` |

### Ornek: n = 27
```
27 -> 82 -> 41 -> 124 -> 62 -> 31 -> 94 -> 47 -> 142 -> ...
```

### Kriptografide Kullanimi
Her adimda:
- **Cift sayiya gidildi** -> `0` biti
- **Tek sayiya gidildi** -> `1` biti

Bu sayede deterministik ama tahmin edilmesi zor bir bit dizisi uretilir.

---

## 3. AFFINE CIPHER

### Matematiksel Tanim

**Sifreleme:**
```
E(x) = (a * x + b) mod m
```

**Sifre Cozme:**
```
D(y) = a^(-1) * (y - b) mod m
```

### Parametreler

| Parametre | Aciklama | Kisitlama |
|-----------|----------|-----------|
| `a` | Carpan | `gcd(a, m) = 1` (aralrinda asal) |
| `b` | Toplam | `0 <= b < m` |
| `m` | Modulus | 256 (byte icin) |
| `a^(-1)` | a'nin tersi | Extended Euclidean Algorithm |

### Ornek
```
a = 5, b = 8, m = 256

Sifreleme: E(65) = (5 * 65 + 8) mod 256 = 333 mod 256 = 77
Sifre Cozme: D(77) = 205 * (77 - 8) mod 256 = 205 * 69 mod 256 = 65

Not: 205, 5'in mod 256'daki tersidir.
```

### Neden Affine?
- **Geri Donuslu:** Her karakterin benzersiz bir sifreli karsiligi var
- **Anahtara Bagli:** a ve b degerleri gizli tutulur
- **Hizli:** Sadece carpma ve toplama islemleri

---

## 4. TRANSPOSITION CIPHER

### Calisma Prensibi

Veriyi bloklara bol ve her blogu belirli bir anahtara gore yeniden sirala.

### Ornek

**Anahtar:** `3142`
**Yorumlama:** 3. harf once, 1. harf ikinci, 4. harf ucuncu, 2. harf son

**Orijinal Blok:** `ABCD`
**Sifreli Blok:** `BADC`

```
Pozisyon:  1  2  3  4
Orijinal:  A  B  C  D
Anahtar:   3  1  4  2
Yeni Poz:  2  4  1  3
Sonuc:     B  A  D  C -> BADC
```

### Neden Transposition?
- **Difuzyon:** Karakterlerin konumlari degisir
- **Konfuzyon:** Orijinal yapi gizlenir
- **Katmanli Guvenlik:** Affine ile birlikte cok daha guclu

---

## 5. SIFRELEME ZINCIRI

### Adim 1: Metin -> Byte
```
"AB" -> [65, 66]
```

### Adim 2: Collatz XOR
Collatz dizisinden uretilen bitlerle XOR:
```
[65, 66] XOR [23, 87] -> [86, 117]
```

### Adim 3: Affine Cipher
Her byte'a Affine uygula:
```
E(86) = (5 * 86 + 8) mod 256 = 182
E(117) = (5 * 117 + 8) mod 256 = 73
Sonuc: [182, 73]
```

### Adim 4: Transposition
Bloklari yeniden sirala:
```
[182, 73, 0, 0] -> key "3142" -> [73, 0, 182, 0]
```

### Adim 5: Hex Cikti
```
[73, 0, 182, 0] -> "4900b600"
```

---

## 6. SIFRE COZME ZINCIRI (Ters Sira)

1. **Hex -> Byte**
2. **Transposition (ters)** - Ters anahtar siralamasi
3. **Affine (ters)** - `D(y) = a^(-1) * (y - b) mod m`
4. **Collatz XOR** - Ayni XOR islemi (A XOR B XOR B = A)
5. **Byte -> Metin**

---

## 7. ANAHTAR YAPISI

Tam anahtar 4 bilesenden olusur:

```
SEED:AFFINE_A:AFFINE_B:TRANS_KEY
Ornek: 27:5:8:3142
```

| Bilesen | Deger | Aciklama |
|---------|-------|----------|
| Seed | 27 | Collatz baslangic degeri |
| a | 5 | Affine carpan |
| b | 8 | Affine toplam |
| Trans Key | 3142 | Transposition siralamasi |

---

## 8. 0/1 DENGESI

### Problem
Sifreli metinde esit sayida 0 ve 1 olmasi isteniyor.

### Cozum
1. Sifreleme sonrasi bit dagilimini analiz et
2. Collatz seed secimi ile dengeyi optimize et
3. Istatistiksel testlerle dogrula

### Dogal Denge
Collatz dizisi dogal olarak belirli bir dengeye sahiptir:
- Cift adimlar (0) genellikle biraz daha fazla
- Affine ve Transposition bu dengeyi dagitir

---

## 9. GUVENLIK ANALIZI

### Guclu Yonler
- **Cok Katmanli:** 3 farkli sifreleme katmani
- **Anahtar Uzayi:** Genis anahtar kombinasyonlari
- **Difuzyon:** Transposition ile karakter yayilimi
- **Konfuzyon:** Affine ve XOR ile deger gizleme

### Zayif Yonler (Egitim Amacli)
- Affine cipher tek basina frekans analizine karsi zayif
- Collatz dizisi deterministik
- Modern standartlara (AES, RSA) kiyasla basit

### Oneriler
Bu algoritma **egitim amaclidir**. Gercek uygulamalarda AES, ChaCha20 gibi standart algoritmalar tercih edilmelidir.

---

## 10. KARMASIKLIK ANALIZI

| Islem | Zaman | Alan |
|-------|-------|------|
| Collatz Uretimi | O(n) | O(n) |
| Affine Sifreleme | O(n) | O(1) |
| Transposition | O(n) | O(k) |
| **Toplam** | **O(n)** | **O(n)** |

n: Veri uzunlugu, k: Transposition anahtar uzunlugu

---

## 11. TEST VE DOGRULAMA

### Kullanilan Testler
1. **Monobit Testi** - 0/1 frekans dagilimi
2. **Ki-Kare Testi** - Blok bazli rastgelelik
3. **Runs Testi** - Ardisik bit analizi
4. **Frekans Analizi** - Byte dagilimi

### Basari Kriterleri
- p-value >= 0.01: Test basarili (rastgele davranis)
- p-value < 0.01: Test basarisiz (oruntu tespit edildi)

---

## 12. ORNEK KULLANIM

```python
from collatz_crypto import CollatzCrypto

# Sifreleme
crypto = CollatzCrypto(seed=27, affine_a=5, affine_b=8, trans_key="3142")
ciphertext, metadata = crypto.encrypt("Gizli Mesaj")
print(f"Sifreli: {ciphertext}")

# Sifre Cozme
plaintext = crypto.decrypt(ciphertext, metadata['original_length'])
print(f"Cozulmus: {plaintext}")
```

---

## 13. SONUC

Bu algoritma, kriptografi temellerini anlamak icin tasarlanmis egitimsel bir projedir:

- Collatz sanisinin bit uretiminde kullanimi
- Affine cipher matematiksel donusumu
- Transposition ile pozisyon karistirma
- Cok katmanli sifreleme yapisi
- Istatistiksel test ve dogrulama
