import libscrc
import qrcode
import io
import base64
from typing import Optional, Union

def _format_tlv(tag: str, value: str) -> str:
    length_str = f"{len(value):02d}"
    return f"{tag}{length_str}{value}"

def calculate_crc(code_string: str) -> str:
    encoded_string = str.encode(code_string, 'ascii')
    crc_val = libscrc.ccitt_false(encoded_string)
    crc_hex_str = hex(crc_val)[2:].upper()
    return crc_hex_str.rjust(4, '0')

def generate_promptpay_qr_payload(
    mobile: Optional[str] = None,
    nid: Optional[str] = None,
    amount: Optional[Union[float, int, str]] = None,
    one_time: bool = False
) -> str:
    if not mobile and not nid:
        raise ValueError("ต้องระบุเบอร์โทรศัพท์หรือเลขบัตรประชาชน")

    payload_elements = []

    # TAG 00 + 01
    payload_elements.append(_format_tlv("00", "01"))
    payload_elements.append(_format_tlv("01", "12" if one_time else "11"))

    # TAG 29
    sub_elements = [_format_tlv("00", "A000000677010111")]

    if mobile:
        if not (len(mobile) == 10 and mobile.isdigit()):
            raise ValueError("เบอร์โทรต้องเป็น 10 หลัก")
        mobile_value = f"00TH{mobile[1:]}"
        sub_elements.append(_format_tlv("01", mobile_value))
    elif nid:
        nid_clean = nid.replace("-", "")
        if not (len(nid_clean) == 13 and nid_clean.isdigit()):
            raise ValueError("เลขบัตรประชาชนไม่ถูกต้อง")
        sub_elements.append(_format_tlv("02", nid_clean))

    payload_elements.append(_format_tlv("29", ''.join(sub_elements)))
    payload_elements.append(_format_tlv("53", "764"))

    if amount is not None:
        try:
            amount = float(amount)
            if amount > 0:
                payload_elements.append(_format_tlv("54", f"{amount:.2f}"))
        except:
            raise ValueError("จำนวนเงินไม่ถูกต้อง")

    payload_elements.append(_format_tlv("58", "TH"))

    raw = ''.join(payload_elements)
    crc_input = raw + "6304"
    crc = calculate_crc(crc_input)
    return crc_input + crc

def generate_promptpay_qr_base64(mobile: str, amount: float) -> str:
    payload = generate_promptpay_qr_payload(mobile=mobile, amount=amount, one_time=False)
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
