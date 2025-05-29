from decimal import Decimal
import crcmod.predefined

def format_amount(amount: Decimal) -> str:
    return '{:.2f}'.format(amount)

def qr_code(receiver: str, amount: Decimal = None) -> str:
    payload = '00020101021129370016A0000006770101110113'
    receiver = receiver.replace('-', '')
    payload += f'0066{len(receiver):02}{receiver}'
    payload += '0208QR*12345678'
    payload += '5303764'
    if amount:
        amt_str = format_amount(amount)
        payload += f'54{len(amt_str):02}{amt_str}'
    payload += '5802TH6304'

    crc16 = crcmod.predefined.mkCrcFun('crc-ccitt-false')
    checksum = format(crc16(payload.encode()), '04X')
    payload += checksum
    return payload
