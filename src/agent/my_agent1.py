from langchain.agents import create_agent
from agent.my_llm import llm

def send_email(to: str, subject: str, body: str) -> str:
    """发送邮件"""
    email = {
        "to": to,
        "subject": subject,
        "body": body
    }
    # ... 这里可以集成实际的邮件发送逻辑
    return f"邮件已发送到 {to}，主题：{subject}"

agent = create_agent(
    llm,
    tools=[send_email],
    system_prompt="你是一个邮件发送助手，请始终使用 send_email 工具来发送邮件。"
)