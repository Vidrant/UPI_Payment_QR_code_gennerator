import qrcode

#Taking UPI ID as a input
upi_id = input("Enter your UPI ID = ")
amt = input("Enter the amount to enter = ")

#upi://pay?pa=UPI_ID&pn=NAME&am=Amount&cu=CURRENCY&tn=MESSAGE

#Defining the payment URL based on the UPI ID and the payment app
Google_pay_url = f'upi://pay?pa={upi_id}&pn=Recipient%20Name&am={amt}'
Paytm_url = f'upi://pay?pa={upi_id}&pn=Recipient%20Name&am={amt}'

#Create QR Codes for each app(not necessary for each app)
Google_pay_qr = qrcode.make(Google_pay_url)
Paytm_qr = qrcode.make(Paytm_url)

#Save the QR code to image file(optional)
Google_pay_qr.save('google_pay_qr.png')
Paytm_qr.save('Paytm_qr.png')

#Display the QR code (thus use of pillow library)
Google_pay_qr.show()
Paytm_qr.show()


