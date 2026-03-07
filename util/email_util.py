"""
email_util.py — Gmail SMTP email notifications for test failures/summary.
"""
import os, smtplib, logging
from email.message import EmailMessage
from config.config_loader import CFG

log = logging.getLogger(__name__)

def _smtp():
    s = smtplib.SMTP_SSL(CFG.smtp_host, CFG.smtp_port)
    s.login(CFG.email_sender, CFG.email_password)
    return s

def send_failure_email(test_name: str, log_file: str = None):
    if not CFG.email_enabled: return
    msg = EmailMessage()
    msg["Subject"] = f"❌ FAILED: {test_name}"
    msg["From"]    = CFG.email_sender
    msg["To"]      = ", ".join(CFG.email_receivers)
    msg.set_content(
        f"Test '{test_name}' FAILED.\n\nEnv: {CFG._env}\nURL: {CFG.base_url}\n"
    )
    if log_file and os.path.exists(log_file):
        with open(log_file, "rb") as f:
            msg.add_attachment(f.read(), maintype="text", subtype="plain",
                               filename=os.path.basename(log_file))
    try:
        with _smtp() as s: s.send_message(msg)
        log.info(f"[Email] Failure email sent: {test_name}")
    except Exception as e:
        log.warning(f"[Email] Send failed: {e}")

def send_summary_email(total, passed, failed, failed_tests):
    if not CFG.email_enabled: return
    status = "✅ ALL PASSED" if failed == 0 else f"❌ {failed} FAILED"
    msg = EmailMessage()
    msg["Subject"] = f"[QA Report] {status} | {passed}/{total}"
    msg["From"]    = CFG.email_sender
    msg["To"]      = ", ".join(CFG.email_receivers)
    rows = "\n".join(f"  • {t['test']}" for t in failed_tests)
    msg.set_content(
        f"Test Run Summary\nEnv: {CFG._env}\nTotal:{total} Passed:{passed} Failed:{failed}\n\n{rows}"
    )
    try:
        with _smtp() as s: s.send_message(msg)
        log.info("[Email] Summary email sent.")
    except Exception as e:
        log.warning(f"[Email] Summary send failed: {e}")
