# 🔐 Collatz-Based Cryptographic Algorithm

## CS64 - Kriptoloji Projesi

Bu proje, **Collatz Sanısı** üzerine kurulu, **Affine Cipher** ve **Transposition (Yer Değiştirme)** şifreleme yöntemlerini kullanan özgün bir kriptografik algoritma içermektedir.

---

## 📖 İçindekiler

1. [Algoritma Mantığı](#algoritma-mantığı)
2. [Kurulum](#kurulum)
3. [Kullanım](#kullanım)
4. [Dosya Yapısı](#dosya-yapısı)
5. [İstatistiksel Testler](#istatistiksel-testler)
6. [Örnek Çıktılar](#örnek-çıktılar)

---

## 🧮 Algoritma Mantığı

### Collatz Sanısı Nedir?
Collatz sanısı, herhangi bir pozitif tam sayı için:
- Sayı **çift** ise → `n / 2`
- Sayı **tek** ise → `3n + 1`

işlemlerini tekrarlayarak sonunda 1'e ulaşılacağını öne sürer.

### Şifreleme Yaklaşımı

Bu algoritmada Collatz dizisi üzerinden **iki farklı çıktı** üretilir:
- **Çift adım** → `0` biti
- **Tek adım** → `1` biti

Bu bitler, eşit sayıda 0 ve 1 içerecek şekilde dengelenir, ardından iki katmanlı şifreleme uygulanır:

1. **Affine Cipher**: `E(x) = (a × x + b) mod m`
2. **Transposition**: Belirli bir anahtar ile bit/karakter sıralaması değiştirilir

---

## 🚀 Kurulum

```bash
# Python 3.8+ gereklidir
pip install -r requirements.txt
```

---

## 🔧 Kullanım

### Şifreleme
```bash
python collatz_crypto.py encrypt "Merhaba Dünya" --seed 27 --affine-a 5 --affine-b 8 --trans-key "3142"
```

### Şifre Çözme
```bash
python collatz_crypto.py decrypt "ENCRYPTED_TEXT" --seed 27 --affine-a 5 --affine-b 8 --trans-key "3142"
```

---

## 📁 Dosya Yapısı

```
cs64-collatz/
├── README.md                    # Bu dosya
├── requirements.txt             # Python bağımlılıkları
├── collatz_crypto.py            # Ana algoritma kodu
├── key_generator.py             # Anahtar üreteci
├── statistical_tests.py         # Ki-kare ve diğer testler
├── docs/
│   ├── PSEUDOCODE.md            # Sözde kod
│   ├── ALGORITHM_EXPLANATION.md # Algoritma açıklaması
│   └── flowchart.png            # Akış şeması
└── examples/
    └── sample_outputs.txt       # Örnek çıktılar
```

---

## 📊 İstatistiksel Testler

Algoritmanın rastgelelik kalitesini doğrulamak için:
- **Ki-Kare (Chi-Square) Testi**
- **Monobit Testi**
- **Runs Testi**
- **Frekans Analizi**

Detaylı sonuçlar için `statistical_tests.py` çalıştırılabilir.

---

## 👥 Katkıda Bulunanlar

- **Sait D. Dündar** - Proje Geliştirici

---

## 📄 Lisans

MIT License
