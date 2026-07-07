from zlapi import ZaloAPI
from zlapi.models import Message
import requests

from config import PHONE, PASSWORD, IMEI, SESSION_COOKIES, WEB_URL


class ShopBot(ZaloAPI):

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        text = message.strip()

        # Đăng ký User
        requests.post(
            f"{WEB_URL}/api/user",
            json={
                "telegram_id": str(author_id),
                "name": str(author_id),
                "username": ""
            }
        )

        # ===== START =====
        if text == "/start":
            self.sendMessage(
                Message(
                    text="👋 Chào mừng bạn đến Shop!\n"
                         "👉 /dat_trc\n"
                         "👉 /guima MÃ"
                ),
                thread_id,
                thread_type
            )

        # ===== THANH TOÁN =====
        elif text == "/dat_trc":
            self.sendMessage(
                Message(
                    text=f"💳 Nội dung CK:\nDonate {author_id}\n\nSau đó gửi ảnh Bill."
                ),
                thread_id,
                thread_type
            )

        # ===== GỬI MÃ =====
        elif text.startswith("/guima"):

            check = requests.get(
                f"{WEB_URL}/api/check_approve?telegram_id={author_id}"
            ).json()

            if not check["approved"]:
                self.sendMessage(
                    Message(text="❌ Bạn chưa được duyệt bill."),
                    thread_id,
                    thread_type
                )
                return

            code = text.replace("/guima", "").strip()

            if code == "":
                self.sendMessage(
                    Message(text="⚠️ Dùng /guima MÃ"),
                    thread_id,
                    thread_type
                )
                return

            requests.post(
                f"{WEB_URL}/api/code",
                json={
                    "telegram_id": str(author_id),
                    "event_code": code
                }
            )

            self.sendMessage(
                Message(text="✅ Đã gửi mã."),
                thread_id,
                thread_type
            )


bot = ShopBot(
    PHONE,
    PASSWORD,
    imei=IMEI,
    session_cookies=SESSION_COOKIES
)

bot.listen(run_forever=True)