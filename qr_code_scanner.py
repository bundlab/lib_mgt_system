import cv2
import qrcode

# Try importing pyzbar safely
try:
    from pyzbar.pyzbar import decode
    ZBAR_AVAILABLE = True
except ImportError:
    ZBAR_AVAILABLE = False


def generate_book_qr(book_id, title):
    data = f"BOOK:{book_id}:{title}"
    qr = qrcode.make(data)
    qr.save(f"assets/qr_codes/book_{book_id}.png")


def scan_qr_code():
    if not ZBAR_AVAILABLE:
        raise RuntimeError(
            "QR scanning is not available.\n"
            "Please install zbar:\n\n"
            "sudo apt install libzbar0"
        )

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        for qr in decode(frame):
            data = qr.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            return data

        cv2.imshow("QR Scanner - Press Q to exit", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
