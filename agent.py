from datetime import datetime
from uuid import uuid4
from collections import defaultdict

from openai import OpenAI
from uagents import Agent, Protocol, Context
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)

# --------------------------------------
# Static helpline database by state
# --------------------------------------
helplines_by_state = {
    "tamil nadu": {
        "Women Helpline": "1091",
        "Police Emergency": "100",
        "Tamil Nadu Legal Services": "044-2534-0345",
        "Childline": "1098",
        "Local NGO - PCVC": "+91-44-2615-4883"
    },
    "maharashtra": {
        "Women Helpline": "103",
        "Mumbai Police": "100",
        "Legal Aid Mumbai": "022-2262-2213",
        "Sneha NGO (Domestic Abuse)": "022-2431-2828"
    },
    "karnataka": {
        "Women Helpline": "1091",
        "Bangalore Police": "100",
        "Karnataka Legal Services": "080-2238-7979",
        "Vanitha Sahayavani NGO": "080-2294-3450"
    },
    "delhi": {
        "Women Helpline": "181",
        "Delhi Police": "100",
        "Delhi Legal Services": "011-2338-7376",
        "DCW Helpline": "011-2337-1762"
    }
}

# Memory for user chat history (per sender)
conversation_history = defaultdict(list)
MAX_HISTORY_LENGTH = 10  # Only keep last 10 messages

# --------------------------------------
# Create the agent
# --------------------------------------
agent = Agent(
    name="daya_clone",
    port=8001,
    seed="daya_clone_secret_phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
    description="Daya Clone Agent - Assisting women with safety, legal, and emotional needs"
)

# ASI model client
client = OpenAI(
    base_url='https://api.asi1.ai/v1',
    api_key='sk_e5fdf90812a84b459a13057355d48c9f7c045cec08df48e286c70198d16102dc',
)

# Protocol
protocol = Protocol(spec=chat_protocol_spec)

@protocol.on_message(ChatMessage)
async def handle_user_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))

    user_input = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            user_input += item.text

    # Update conversation history
    conversation_history[sender].append({"role": "user", "content": user_input})
    if len(conversation_history[sender]) > MAX_HISTORY_LENGTH:
        conversation_history[sender] = conversation_history[sender][-MAX_HISTORY_LENGTH:]

    # Detect emergency and location
    detected_location = None
    for state in helplines_by_state:
        if state in user_input.lower():
            detected_location = state
            break

    emergency_keywords = ["help", "emergency", "unsafe", "harassment", "abuse", "violence", "danger", "assault"]
    is_emergency = any(k in user_input.lower() for k in emergency_keywords)

    if detected_location and is_emergency:
        response = f"🛡️ I'm here to support you. Here are trusted helplines in {detected_location.title()}:\n"
        for service, number in helplines_by_state[detected_location].items():
            response += f"- {service}: {number}\n"

        # Add assistant message to history
        conversation_history[sender].append({"role": "assistant", "content": response})
    else:
        try:
            r = client.chat.completions.create(
                model="asi1-mini",
                messages=[
                    {"role": "system", "content": """
You are Daya, a smart, kind, and supportive AI assistant built for women. 
You help with health, safety, legal awareness, motivation, and daily emotional needs.

Always maintain a helpful, friendly tone and remember prior conversations.
"""},
                ] + conversation_history[sender],
                max_tokens=2048,
            )
            response = r.choices[0].message.content.strip()
            conversation_history[sender].append({"role": "assistant", "content": response})
        except Exception as e:
            ctx.logger.exception("Error from ASI")
            response = f"⚠️ Unable to process your request right now. Error: {e}"

    await ctx.send(sender, ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=response)],
    ))

@protocol.on_message(ChatAcknowledgement)
async def ack_handler(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
