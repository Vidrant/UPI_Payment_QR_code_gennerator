"""
UPI Payment QR Code Generator
------------------------------
Generates a scannable QR code for UPI (Unified Payments Interface) payments.

Any UPI-enabled app (Google Pay, PhonePe, Paytm, BHIM, etc.) can scan a single
QR code built from the standard `upi://pay` deep link -- there is no need to
generate a separate code per app, since they all speak the same protocol.

UPI deep link reference:
    upi://pay?pa=<PAYEE_UPI_ID>&pn=<PAYEE_NAME>&am=<AMOUNT>&cu=<CURRENCY>&tn=<NOTE>

    pa  -> Payee address (the UPI ID / VPA)
    pn  -> Payee name (shown to the payer during confirmation)
    am  -> Amount to be paid
    cu  -> Currency code (INR for India)
    tn  -> Transaction note / message (optional, shown to payer)
"""

import re
from datetime import datetime

import qrcode

UPI_ID_PATTERN = re.compile(r"^[\w.\-]{2,256}@[a-zA-Z]{2,64}$")


def get_upi_id() -> str:
    """Prompt the user for a UPI ID and validate its basic format."""
    while True:
        upi_id = input("Enter your UPI ID (e.g. name@bank): ").strip()
        if UPI_ID_PATTERN.match(upi_id):
            return upi_id
        print("That doesn't look like a valid UPI ID. Format should be like 'yourname@bankname'.")


def get_amount() -> str:
    """Prompt the user for a payment amount and validate it's a positive number."""
    while True:
        raw_amt = input("Enter the amount to receive (in INR): ").strip()
        try:
            amt = float(raw_amt)
            if amt <= 0:
                print("Amount must be greater than zero.")
                continue
            # Format cleanly: whole numbers without decimals, else 2 decimal places
            return f"{amt:.2f}" if amt % 1 else f"{int(amt)}"
        except ValueError:
            print("Please enter a valid number, e.g. 250 or 99.50")


def get_optional(prompt: str, default: str) -> str:
    """Prompt for an optional field, falling back to a default if left blank."""
    value = input(f"{prompt} [default: {default}]: ").strip()
    return value if value else default


def build_upi_url(upi_id: str, amount: str, payee_name: str, note: str, currency: str = "INR") -> str:
    """Construct the UPI deep link URL from payment details."""
    payee_name_enc = payee_name.replace(" ", "%20")
    note_enc = note.replace(" ", "%20")
    return (
        f"upi://pay?pa={upi_id}&pn={payee_name_enc}"
        f"&am={amount}&cu={currency}&tn={note_enc}"
    )


def generate_qr(data: str, filename: str) -> None:
    """Generate and save a QR code image for the given data string."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR code saved as '{filename}'")


def main():
    print("=== UPI Payment QR Code Generator ===\n")

    upi_id = get_upi_id()
    amount = get_amount()
    payee_name = get_optional("Enter recipient's display name", "Recipient")
    note = get_optional("Enter a payment note/message", "Payment")

    upi_url = build_upi_url(upi_id, amount, payee_name, note)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"upi_qr_{timestamp}.png"

    try:
        generate_qr(upi_url, filename)
    except Exception as exc:
        print(f"Failed to generate QR code: {exc}")
        return

    print(f"\nPayment link encoded: {upi_url}")
    print("Scan this QR code with any UPI app (Google Pay, PhonePe, Paytm, BHIM, etc.) to pay.")

    show = input("\nOpen the QR code image now? (y/n): ").strip().lower()
    if show == "y":
        try:
            from PIL import Image
            Image.open(filename).show()
        except Exception as exc:
            print(f"Could not open image viewer automatically: {exc}")
            print(f"You can open '{filename}' manually.")


if __name__ == "__main__":
    main()
