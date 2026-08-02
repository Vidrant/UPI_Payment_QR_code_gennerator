# UPI Payment QR Code Generator

A small Python tool that generates a scannable QR code for **UPI (Unified Payments Interface)** payments — India's real-time payment network. Point any UPI-enabled app's scanner at the generated code, and it opens a pre-filled payment screen.

## How it works

UPI apps recognize a standard deep-link format:

```
upi://pay?pa=<UPI_ID>&pn=<NAME>&am=<AMOUNT>&cu=<CURRENCY>&tn=<NOTE>
```

| Parameter | Meaning                                  |
|-----------|-------------------------------------------|
| `pa`      | Payee address — the receiver's UPI ID     |
| `pn`      | Payee name — shown to the payer           |
| `am`      | Amount to be paid                          |
| `cu`      | Currency code (`INR`)                      |
| `tn`      | Transaction note / message                 |

Since every UPI app (Google Pay, PhonePe, Paytm, BHIM, etc.) reads this same link format, **one QR code works across all of them** — there's no need to generate an app-specific code.

This script builds that link from user input, encodes it into a QR code image using the `qrcode` library, and saves it as a PNG.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python upi_qr_generator.py
```

You'll be prompted for:
- Your UPI ID (validated against a basic `name@bank` pattern)
- The amount to receive (validated as a positive number)
- An optional display name and payment note

The script then saves a PNG (e.g. `upi_qr_20260803_141200.png`) and optionally opens it for you.

## Possible future enhancements

- A simple GUI (Tkinter) or web interface (Streamlit/Flask) instead of CLI prompts
- QR code with an embedded logo for branding
- Batch generation for multiple payees from a CSV
- Unit tests for input validation and URL building
