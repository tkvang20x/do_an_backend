import base64
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from starlette import status

from app.src.base.base_exception import gen_exception_service, BusinessException
from app.src.base.base_service import Singleton
from app.src.repository.manager_repository import ManagerRepository
from app.src.repository.user_repository import UserRepository


class ChangePasswordService(metaclass=Singleton):
    def __init__(self):
        self.user_repo = UserRepository()
        self.manager_repo = ManagerRepository()

    def change_password_service(self, new_pass: str, old_pass: str, username: str, role: str):
        try:
            if len(new_pass.strip()) == 0:
                raise BusinessException(message=f'Password must not blank!',
                                        http_code=status.HTTP_400_BAD_REQUEST)
            if role == "USER":
                user_result = self.user_repo.check_exist_value_in_db(field="user_name", value=username.strip())
                check_password = self.check_password(pass_input=old_pass,
                                                     old_pass=base64.b64decode(user_result.password).decode('utf-8'))
                if not check_password:
                    return False
                    # raise BusinessException(message=f'Password wrong!',
                    #                         http_code=status.HTTP_400_BAD_REQUEST)
                update_pass = self.user_repo.update_password_user(code=user_result.code, new_pass=new_pass)
            else:
                manager_result = self.manager_repo.check_user_name_manager(user_name=username.strip())
                check_password = self.check_password(pass_input=old_pass,
                                                     old_pass=base64.b64decode(manager_result.password).decode('utf-8'))
                if not check_password:
                    # raise BusinessException(message=f'Password wrong!',
                    #                         http_code=status.HTTP_400_BAD_REQUEST)
                    return False
                update_pass = self.manager_repo.update_password_manager(code=manager_result.code, new_pass=new_pass)
            return update_pass
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def forgot_password_service(self, email: str, role: str):
        try:
            if role != "MANAGER":
                user_result = self.user_repo.check_exist_value_in_db(field="email", value=email)
                if user_result:
                    code = self.send_email_service(email=email)
                    self.user_repo.update_password_user(code=user_result.code, new_pass=code)
                    return True
                return False
            else:
                manager_result = self.manager_repo.check_email_manager(email=email)
                if manager_result:
                    code = self.send_email_service(email=email)
                    self.manager_repo.update_password_manager(code=manager_result.code, new_pass=code)
                    return True
                return False
        except Exception as e:
            http_status, error_message = gen_exception_service(e)
            raise BusinessException(message=error_message, http_code=http_status)

    def check_password(self, pass_input: str, old_pass: str):
        if pass_input.strip() == old_pass.strip():
            return True
        return False

    def send_email_service(self, email: str):
        message = MIMEMultipart()
        message['From'] = 'kienlt20072000@gmail.com'
        message['To'] = email
        message['Subject'] = 'Mã xác nhận quên mật khẩu'

        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        text = f'Mã xác nhận của bạn là: {code} (Lưu ý tuyệt đối không được chia sẻ mật khẩu mới này của bạn cho bất kỳ ai!)'
        message.attach(MIMEText(text))

        # Gửi email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("kienlt20072000@gmail.com", "dlztgrdtpbbrsydp")
            smtp.sendmail('kienlt20072000@gmail.com', email, message.as_string())
            smtp.quit()
        # s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # s.login("kienlt20072000@gmail.com", "dlztgrdtpbbrsydp")
        # s.sendmail('kienlt20072000@gmail.com', email, message.as_string())
        # s.quit()

        # Trả về mã xác nhận để sử dụng ở hàm khác
        return code

    def send_email_message_expired(self, email: str, voucher_id: str):
        message = MIMEMultipart()
        message['From'] = 'kienlt20072000@gmail.com'
        message['To'] = email
        message['Subject'] = 'Thông báo v/v hết hạn phiếu mượn Thư viện HV KT Mật Mã'

        # code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        text = f'Bạn có phiếu mượn sách có mã là {voucher_id} của thư viện HV KT Mật Mã đã đến hạn trả, vui lòng đăng nhập để xem thông tin ' \
               f'chi tiết phiếu mượn đến hạn trả và trả sách vào thời gian sớm nhất cho thư viện'
        message.attach(MIMEText(text))

        # Gửi email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("kienlt20072000@gmail.com", "dlztgrdtpbbrsydp")
            smtp.sendmail('kienlt20072000@gmail.com', email, message.as_string())
            smtp.quit()

        # Trả về mã xác nhận để sử dụng ở hàm khác
        return True