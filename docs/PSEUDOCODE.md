# 📝 SÖZDE KOD (PSEUDOCODE)

## Collatz Tabanlı Şifreleme Algoritması

---

## 1. ANAHTAR ÜRETİMİ

```
FUNCTION GenerateKeySet():
    // Collatz Seed Üretimi
    seed = SecureRandom(10, 1000)
    
    // Affine Cipher Parametreleri
    // a değeri 256 ile aralarında asal olmalı
    valid_a_values = FindAllCoprimes(256)
    a = RandomChoice(valid_a_values)
    b = SecureRandom(0, 255)
    
    // Modüler ters hesapla (şifre çözme için)
    a_inverse = ModularInverse(a, 256)
    
    // Transposition Anahtarı
    trans_key = GeneratePermutation(4)  // Örn: "3142"
    
    RETURN {seed, a, b, a_inverse, trans_key}
```

---

## 2. COLLATZ DİZİSİ ÜRETİMİ

```
FUNCTION GenerateCollatzBits(seed, length):
    bits = []
    current = seed
    
    WHILE Length(bits) < length:
        IF current == 1:
            current = seed  // Yeniden başlat
        ENDIF
        
        IF current MOD 2 == 0:
            Append(bits, 0)     // Çift → 0
            current = current / 2
        ELSE:
            Append(bits, 1)     // Tek → 1
            current = 3 * current + 1
        ENDIF
    ENDWHILE
    
    RETURN bits[0:length]
```

---

## 3. AFFINE CIPHER

### 3.1 Şifreleme
```
FUNCTION AffineEncrypt(byte, a, b, m):
    // E(x) = (a × x + b) mod m
    RETURN (a * byte + b) MOD m
```

### 3.2 Şifre Çözme
```
FUNCTION AffineDecrypt(byte, a_inverse, b, m):
    // D(y) = a^(-1) × (y - b) mod m
    RETURN (a_inverse * (byte - b)) MOD m
```

### 3.3 Modüler Ters Hesaplama
```
FUNCTION ModularInverse(a, m):
    // Extended Euclidean Algorithm
    FUNCTION ExtendedGCD(a, b):
        IF a == 0:
            RETURN (b, 0, 1)
        ENDIF
        (gcd, x1, y1) = ExtendedGCD(b MOD a, a)
        x = y1 - (b / a) * x1
        y = x1
        RETURN (gcd, x, y)
    
    (_, x, _) = ExtendedGCD(a MOD m, m)
    RETURN (x MOD m + m) MOD m
```

---

## 4. TRANSPOSITION CIPHER

### 4.1 Anahtar Sıralama
```
FUNCTION ParseTransKey(key):
    // "3142" → [2, 0, 3, 1] (0-indexed pozisyonlar)
    key_nums = [CharToInt(c) FOR c IN key]
    sorted_indices = []
    
    FOR new_pos, (old_pos, val) IN Enumerate(SortByValue(key_nums)):
        sorted_indices[old_pos] = new_pos
    
    RETURN sorted_indices
```

### 4.2 Şifreleme
```
FUNCTION TransposeEncrypt(data, key):
    key_order = ParseTransKey(key)
    key_len = Length(key_order)
    result = []
    
    FOR i = 0 TO Length(data) STEP key_len:
        block = data[i : i + key_len]
        
        // Padding ekle
        IF Length(block) < key_len:
            block = Pad(block, key_len)
        ENDIF
        
        // Yeniden sırala
        new_block = []
        FOR old_pos = 0 TO key_len:
            new_pos = key_order[old_pos]
            new_block[new_pos] = block[old_pos]
        
        Extend(result, new_block)
    
    RETURN result
```

### 4.3 Şifre Çözme
```
FUNCTION TransposeDecrypt(data, key):
    key_order = ParseTransKey(key)
    reverse_order = InverseMapping(key_order)
    // Aynı mantık, ters sıralama ile
    ...
```

---

## 5. XOR İŞLEMİ

```
FUNCTION XorWithCollatz(data, seed):
    needed_bits = Length(data) * 8
    collatz_bits = GenerateCollatzBits(seed, needed_bits)
    
    // Bitleri byte'lara dönüştür
    collatz_bytes = []
    FOR i = 0 TO needed_bits STEP 8:
        byte_bits = collatz_bits[i : i + 8]
        byte_val = BitsToInt(byte_bits)
        Append(collatz_bytes, byte_val)
    
    // XOR uygula
    result = []
    FOR i = 0 TO Length(data):
        Append(result, data[i] XOR collatz_bytes[i])
    
    RETURN result
```

---

## 6. ANA ŞİFRELEME

```
FUNCTION Encrypt(plaintext, keyset):
    // Adım 1: Metin → Byte
    data = TextToBytes(plaintext, "UTF-8")
    original_length = Length(data)
    
    // Adım 2: Collatz XOR
    data = XorWithCollatz(data, keyset.seed)
    
    // Adım 3: Affine Cipher
    FOR i = 0 TO Length(data):
        data[i] = AffineEncrypt(data[i], keyset.a, keyset.b, 256)
    
    // Adım 4: Transposition
    data = TransposeEncrypt(data, keyset.trans_key)
    
    // Adım 5: Hex çıktı
    ciphertext = BytesToHex(data)
    
    RETURN (ciphertext, original_length)
```

---

## 7. ANA ŞİFRE ÇÖZME

```
FUNCTION Decrypt(ciphertext_hex, keyset, original_length):
    // Adım 1: Hex → Byte
    data = HexToBytes(ciphertext_hex)
    
    // Adım 2: Transposition (ters)
    data = TransposeDecrypt(data, keyset.trans_key)
    
    // Adım 3: Affine Cipher (ters)
    FOR i = 0 TO Length(data):
        data[i] = AffineDecrypt(data[i], keyset.a_inverse, keyset.b, 256)
    
    // Adım 4: Collatz XOR
    data = XorWithCollatz(data, keyset.seed)
    
    // Adım 5: Padding kaldır ve metin döndür
    data = data[0 : original_length]
    plaintext = BytesToText(data, "UTF-8")
    
    RETURN plaintext
```

---

## 8. DENGE KONTROLÜ

```
FUNCTION AnalyzeBitBalance(data):
    bit_string = ""
    FOR byte IN data:
        bit_string += IntToBits(byte, 8)
    
    zeros = Count(bit_string, '0')
    ones = Count(bit_string, '1')
    ratio = zeros / ones
    
    RETURN {zeros, ones, ratio}
```

---

## 📋 Özet Akış

```
┌─────────────────┐
│   Düz Metin     │
└────────┬────────┘
         │ UTF-8 Encode
         ▼
┌─────────────────┐
│   Byte Dizisi   │
└────────┬────────┘
         │ Collatz XOR
         ▼
┌─────────────────┐
│   XOR Sonucu    │
└────────┬────────┘
         │ Affine Encrypt
         ▼
┌─────────────────┐
│  Affine Çıktı   │
└────────┬────────┘
         │ Transpose
         ▼
┌─────────────────┐
│  Şifreli Metin  │
└─────────────────┘
```
