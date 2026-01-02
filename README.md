# Collatz-Based Cryptographic Algorithm

A custom cryptographic algorithm leveraging the **Collatz Conjecture** for key stream generation, combined with **Affine Cipher** and **Transposition Cipher** for multi-layer encryption.

> **Course Project:** CS64 - Computer Security / Cryptography

---

## Table of Contents

1. [Overview](#overview)
2. [Algorithm Description](#algorithm-description)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Documentation](#documentation)
7. [Statistical Tests](#statistical-tests)
8. [License](#license)

---

## Overview

This project implements a symmetric encryption algorithm that combines three cryptographic techniques:

| Component | Description |
|-----------|-------------|
| **Collatz Conjecture** | Generates pseudo-random bit stream (even→0, odd→1) |
| **Affine Cipher** | Mathematical transformation: `E(x) = (ax + b) mod 256` |
| **Transposition Cipher** | Positional permutation based on key |

### Key Features

- Multi-layer encryption for enhanced security
- Configurable key parameters
- Statistical randomness validation
- Complete documentation with pseudocode and flowcharts

---

## Algorithm Description

### Encryption Flow

```
Plaintext → UTF-8 Encode → Collatz XOR → Affine Cipher → Transposition → Ciphertext (Hex)
```

### Decryption Flow

```
Ciphertext (Hex) → Transposition (Reverse) → Affine Cipher (Reverse) → Collatz XOR → UTF-8 Decode → Plaintext
```

### Key Structure

The complete key consists of four components:

```
SEED:AFFINE_A:AFFINE_B:TRANS_KEY
Example: 27:5:8:3142
```

| Parameter | Description | Constraints |
|-----------|-------------|-------------|
| `SEED` | Collatz starting value | 10-1000 (recommended) |
| `AFFINE_A` | Affine multiplier | gcd(a, 256) = 1 |
| `AFFINE_B` | Affine offset | 0-255 |
| `TRANS_KEY` | Transposition permutation | e.g., "3142" |

---

## Installation

### Requirements

- Python 3.8 or higher
- NumPy
- SciPy (for statistical tests)

### Setup

```bash
# Clone the repository
git clone https://github.com/saitddundar/cs64-collatz.git
cd cs64-collatz

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Encryption

```bash
python collatz_crypto.py encrypt "Hello World" --seed 27 --affine-a 5 --affine-b 8 --trans-key "3142"
```

### Decryption

```bash
python collatz_crypto.py decrypt "fde1a9e05ae12fd7dc0018e9" --seed 27 --affine-a 5 --affine-b 8 --trans-key "3142" --original-length 11
```

### Generate Random Keys

```bash
python key_generator.py
```

### Run Statistical Tests

```bash
python run_statistical_tests.py
```

### Python API

```python
from collatz_crypto import CollatzCrypto

# Initialize with key parameters
crypto = CollatzCrypto(seed=27, affine_a=5, affine_b=8, trans_key="3142")

# Encrypt
ciphertext, metadata = crypto.encrypt("Secret Message")
print(f"Encrypted: {ciphertext}")
print(f"Original length: {metadata['original_length']}")

# Decrypt
plaintext = crypto.decrypt(ciphertext, metadata['original_length'])
print(f"Decrypted: {plaintext}")
```

---

## Project Structure

```
cs64-collatz/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── collatz_crypto.py            # Main encryption algorithm
├── key_generator.py             # Key generation module
├── statistical_tests.py         # Statistical test module
├── run_statistical_tests.py     # Test runner script
├── generate_examples.py         # Example generator
│
├── docs/
│   ├── PSEUDOCODE.md            # Algorithm pseudocode
│   ├── FLOWCHART.md             # Flowcharts (ASCII + Mermaid)
│   └── ALGORITHM_EXPLANATION.md # Detailed algorithm explanation
│
└── examples/
    ├── sample_outputs.txt       # Sample encryption outputs
    └── statistical_test_results.txt  # Test results
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [PSEUDOCODE.md](docs/PSEUDOCODE.md) | Step-by-step pseudocode for all functions |
| [FLOWCHART.md](docs/FLOWCHART.md) | Visual flowcharts in ASCII and Mermaid format |
| [ALGORITHM_EXPLANATION.md](docs/ALGORITHM_EXPLANATION.md) | Detailed explanation of the algorithm logic |

---

## Statistical Tests

The algorithm's randomness quality is validated using the following tests:

| Test | Purpose | Status |
|------|---------|--------|
| **Monobit Test** | Checks 0/1 frequency distribution | PASS |
| **Chi-Square Test** | Validates block-level randomness | PASS |
| **Runs Test** | Analyzes consecutive bit patterns | PASS |
| **Byte Frequency Analysis** | Checks byte distribution uniformity | PARTIAL |

### Sample Results

```
Test: "Hello World"
Bits: 96, Zeros: 47, Ones: 49
Balance Ratio: 0.9592 (ideal: 1.0)
All core tests: PASSED
```

For detailed results, see [statistical_test_results.txt](examples/statistical_test_results.txt).

---

## Security Notice

This algorithm is designed for **educational purposes** to demonstrate cryptographic concepts. For production applications, use industry-standard algorithms such as:

- AES (Advanced Encryption Standard)
- ChaCha20
- RSA (for asymmetric encryption)

---

## License

MIT License

---

## Author

**Sait D. Dundar**

Computer Security Course Project - 2026
