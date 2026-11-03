"""测试报告邮件：读取 Allure 结果，生成 HTML 正文并发送。

配置全部来自 config/.env（SMTP_HOST / SMTP_PORT / SMTP_USER /
SMTP_PASSWORD / MAIL_TO / MAIL_SUBJECT_PREFIX / PAGES_URL）。
"""

import glob
import json
import os
import smtplib
import ssl
import sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "config" / ".env")

RESULTS_DIR = ROOT / "reports" / "allure-results"

ICON = {
    "passed": "✅",
    "failed": "❌",
    "broken": "💥",
    "skipped": "⏭️",
    "unknown": "❓",
}


def _config() -> dict:
    """从环境变量读取邮件配置。"""
    return {
        "host": os.getenv("SMTP_HOST", "smtp.126.com"),
        "port": int(os.getenv("SMTP_PORT", "465")),
        "user": os.getenv("SMTP_USER", ""),
        "password": os.getenv("SMTP_PASSWORD", ""),
        "to": [x.strip() for x in os.getenv("MAIL_TO", "").split(",") if x.strip()],
        "cc": [x.strip() for x in os.getenv("MAIL_CC", "").split(",") if x.strip()],
        "prefix": os.getenv("MAIL_SUBJECT_PREFIX", "[AutoTest]"),
        "pages_url": os.getenv("PAGES_URL", ""),
    }


def _parse() -> tuple[list, dict]:
    """解析 allure-results，返回用例列表和统计信息。"""
    cases = []
    passed = failed = 0

    for path in glob.glob(str(RESULTS_DIR / "*-result.json")):
        with open(path, encoding="utf-8") as fp:
            data = json.load(fp)

        status = data.get("status", "unknown")
        message = data.get("statusDetails", {}).get("message", "")

        if status == "passed":
            passed += 1
        if status in ("failed", "broken"):
            failed += 1

        cases.append(
            {
                "name": data.get("name", ""),
                "status": status,
                "feature": data.get("testCaseId") or "",
                "msg": message[:200],
            }
        )

    total = len(cases)
    summary = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "rate": (passed / total * 100) if total else 0,
    }
    return cases, summary


def _html(cases: list, summary: dict, url: str) -> str:
    """生成邮件正文（HTML）。"""
    ok = summary["failed"] == 0
    color = "#28a745" if ok else "#dc3545"
    title = "✅ All tests passed" if ok else f"❌ {summary['failed']} test(s) failed"

    rows = "".join(
        f"<tr><td>{ICON.get(c['status'], '❓')}</td>"
        f"<td>{c['name']}</td>"
        f"<td>{c['status']}</td>"
        f"<td style='color:#888'>{c['msg'].replace(chr(10), ' ')[:120]}</td></tr>"
        for c in sorted(cases, key=lambda x: x["status"] != "failed")
    )

    link = f"<p>👉 <a href='{url}'>View the full Allure report</a></p>" if url else ""

    return f"""<div style='font-family:Segoe UI,Arial,sans-serif;max-width:760px;margin:auto'>
      <div style='background:{color};color:#fff;padding:16px 20px;border-radius:8px 8px 0 0'>
        <h2 style='margin:0'>{title}</h2>
        <p style='margin:6px 0 0'>Pass rate {summary['rate']:.1f}%
        ({summary['passed']} passed / {summary['total']} total)</p></div>
      <div style='border:1px solid #eee;border-top:0;padding:16px 20px;border-radius:0 0 8px 8px'>
        {link}
        <table width='100%' cellpadding='6' style='border-collapse:collapse;font-size:13px'>
          <tr style='background:#f6f8fa'><th>Status</th><th>Test case</th><th>Result</th><th>Details</th></tr>
          {rows}</table>
        <p style='color:#999;font-size:12px'>This email was generated automatically by the UI automation project.</p></div></div>"""


def send_report_mail(dry_run: bool = False) -> None:
    """发送测试报告邮件；dry_run=True 只打印预览，不实际发送。"""
    cfg = _config()
    if not cfg["user"] or not cfg["password"]:
        print("缺少 SMTP_USER / SMTP_PASSWORD，跳过发送。")
        return

    cases, summary = _parse()
    if summary["total"] == 0:
        print("无测试结果，跳过发送。")
        return

    ok = summary["failed"] == 0
    subject = (
        f"{cfg['prefix']} {'✅ PASSED' if ok else '❌ FAILED'} "
        f"| Pass Rate {summary['rate']:.0f}%"
    )

    msg = MIMEMultipart("related")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = formataddr(("AutoTest Bot", cfg["user"]))
    msg["To"] = ", ".join(cfg["to"])
    if cfg["cc"]:
        msg["Cc"] = ", ".join(cfg["cc"])
    msg.attach(MIMEText(_html(cases, summary, cfg["pages_url"]), "html", "utf-8"))

    recipients = cfg["to"] + cfg["cc"]

    if dry_run:
        print(f"[DRY-RUN] 主题: {subject}")
        print(f"[DRY-RUN] 发件人: {msg['From']}  收件人({len(recipients)}): {recipients}")
        print(
            f"[DRY-RUN] 统计: 共{summary['total']}条 "
            f"通过{summary['passed']} 失败{summary['failed']} "
            f"通过率{summary['rate']:.0f}%"
        )
        print("[DRY-RUN] 未实际发送")
        return

    if cfg["port"] == 465:
        server = smtplib.SMTP_SSL(
            cfg["host"], cfg["port"], context=ssl.create_default_context()
        )
    else:
        server = smtplib.SMTP(cfg["host"], cfg["port"])
        server.starttls(context=ssl.create_default_context())

    server.login(cfg["user"], cfg["password"])
    server.sendmail(cfg["user"], recipients, msg.as_string())
    server.quit()
    print(f"📧 已发送给 {len(recipients)} 人: {recipients}")


if __name__ == "__main__":
    send_report_mail(dry_run="--dry-run" in sys.argv)
