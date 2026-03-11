# Pastella Wallet Generator GUI

A modern, feature-rich desktop wallet generator for the **[Pastella (PAS)](https://pastella.org/)** cryptocurrency network. Built in Python with a sleek dark-theme GUI inspired by the Pastella brand.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

| Tab | Description |
|-----|-------------|
| **Generate** | Create a brand-new Pastella wallet with a cryptographically secure random seed |
| **Recover**  | Reconstruct a wallet from an existing 25-word mnemonic phrase |
| **Vanity**   | Search for a wallet address that starts with (or contains) a custom pattern |
| **Mining**   | Launch and monitor XMRig directly from the GUI to mine PAS |

### Key highlights

- **Pure Python cryptography** — Ed25519 key derivation and CryptoNote-style Base58 encoding implemented from scratch (no external crypto library except `pycryptodome` for Keccak-256)
- **25-word mnemonic** — custom wordlist of 1,626 words with CRC-32 checksum word (word 25)
- **One-click copy** — every field has a dedicated copy button
- **Live vanity search** — real-time attempt counter, speed (wallets/sec), elapsed time, and progress bar
- **Integrated XMRig launcher** — start/stop mining with a built-in terminal output view
- **Modern dark UI** — Pastella-branded color scheme (deep dark background, magenta/pink accent `#ff8afb`)

---

## Screenshots

> *GUI uses a dark theme with the Pastella pink/magenta accent. Tabs: Generate, Recover, Vanity, Mining.*

---

## Requirements

- Python **3.8** or higher
- [`pycryptodome`](https://pycryptodome.readthedocs.io/) — for Keccak-256 hashing

```
pip install pycryptodome
```

> **Note:** `tkinter` is included in the standard Python distribution on Windows. On Linux you may need to install it separately:
> ```
> sudo apt install python3-tk
> ```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/pastella-wallet-generator.git
cd pastella-wallet-generator

# 2. Install dependencies
pip install pycryptodome

# 3. Run the application
python pastella_wallet_generator_gui.pyw
```

On Windows you can double-click the `.pyw` file to launch it without a console window.

---

## Usage

### Generate a new wallet

1. Open the **Generate** tab.
2. Click **✦ Generate New Wallet**.
3. Your 25-word mnemonic, wallet address, private key (seed hex), and public key are displayed.
4. Use the **⎘** copy buttons or **Copy all 25 words** to save your credentials.

> ⚠️ **Security warning:** Store your mnemonic offline. Anyone who has it can access your funds.

### Recover an existing wallet

1. Open the **Recover** tab.
2. Paste your 25-word mnemonic into the text box (space-separated).
3. Click **↺ Recover Wallet**.
4. The tool validates the checksum (word 25) and derives your address and keys.

### Vanity address search

1. Open the **Vanity** tab.
2. Enter a **pattern** in Base58 characters (the pattern is matched *after* the `PAS` prefix).
3. Set the maximum number of trials and whether matching is case-sensitive.
4. Choose whether the pattern must appear at the **start** of the address or **anywhere**.
5. Click **◈ Start Search** — live statistics update in real time.
6. When a match is found, the full wallet details are displayed automatically.

### Mining (XMRig)

1. Place `xmrig.exe` (Windows) in the **same folder** as this script.
2. Open the **Mining** tab.
3. Fill in the pool URL, port, your wallet address, worker name, and thread count.
4. Click **⛏ Start Mining** — output streams live in the terminal panel.
5. Click **◼ Stop Mining** to terminate the miner.

---

## How it works

### Key derivation

| Step | Detail |
|------|--------|
| Random seed | 64 cryptographically random bytes reduced modulo the Ed25519 group order `L` |
| Public key | Scalar multiplication on the Ed25519 curve (extended coordinates) |
| Address | `PAS_PREFIX (3 bytes)` + `pubkey (32 bytes)` + `Keccak-256 checksum (4 bytes)`, encoded in CryptoNote Base58 |

### Mnemonic encoding

- The 32-byte seed is split into 8 × 4-byte little-endian integers.
- Each integer encodes 3 words from the 1,626-word wordlist.
- A 25th checksum word is derived from a CRC-32 of the first 3 characters of each of the 24 words.

---

## File structure

```
pastella-wallet-generator/
├── pastella_wallet_generator_gui.pyw   # Main application (GUI + crypto)
├── README.md                           # This file
└── xmrig.exe                           # (optional) Place here to enable mining
```

---

## Security considerations

- **Never share your private key or mnemonic** with anyone.
- This tool generates wallets entirely **offline** — no data is sent over the network.
- The random seed uses `os.urandom(64)`, which sources entropy from the operating system's CSPRNG.
- Verify the source code before use if you downloaded it from an untrusted source.

---

## Dependencies

| Library | Purpose | Install |
|---------|---------|---------|
| `tkinter` | GUI framework | Bundled with Python |
| `pycryptodome` | Keccak-256 hash | `pip install pycryptodome` |

All other cryptographic primitives (Ed25519, Base58, mnemonic) are implemented directly in the script.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## Disclaimer

This software is provided **as-is** for educational and personal use. The author is not responsible for any loss of funds. Always back up your mnemonic phrase securely.

---

## Credits

- Built by **syabiz**
- Pastella network: [pastella.org](https://pastella.org/)
