from dataclasses import asdict, dataclass, fields
from email.message import EmailMessage
import re
import smtplib


@dataclass
class EmailConfig:
    host: str
    port: int
    sender_address: str
    sender_password: str
    subject: str
    message_template: str

    def __post_init__(self):
        valid_formatting_keywords = {f.name for f in fields(MessageVariables)}
        pattern = re.compile('\{(<?P>.*)}')
        invalid_keywords = set()
        for match in pattern.findall(self.message_template):
            if keyword := match.group(0) not in valid_formatting_keywords:
                invalid_keywords.add(keyword)

        if invalid_keywords:
            raise ValueError(
                f"Message template may only contain these formatting keywords: "
                f"{valid_formatting_keywords}. Found these though: {invalid_keywords}."
            )


@dataclass
class MessageVariables:
    taker: str


class EmailSender:
    def __init__(self, config: EmailConfig):
        self.config = config

    def send(self, to: str, message_vars: MessageVariables):
        config = self.config
        with smtplib.SMTP_SSL(config.host, config.port) as smtp:
            smtp.login(config.sender_address, config.sender_password)
            msg = EmailMessage()
            msg['Subject'] = config.subject
            msg['From'] = config.sender_address
            msg['To'] = to
            msg.set_content(config.message_template.format(**asdict(message_vars)))
            smtp.send_message(msg)
