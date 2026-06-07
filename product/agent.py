"""
AgentDesk — Core AI Support Agent
Phase 2: FAQ knowledge + conversation memory + escalation
"""

import os
import anthropic

# Load FAQ file
def load_faq(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"FAQ file not found: {filepath}")
        exit(1)

# Build system prompt
def build_system_prompt(business_name, agent_name, faq_content):
    return f"""
You are {agent_name}, the AI support assistant for {business_name}.

RULES:
- Answer ONLY from the knowledge base below. Never guess.
- Be warm, friendly and concise.
- If you cannot find the answer, say:
  "Let me connect you to our team."
  Then give the escalation contact from the knowledge base.

KNOWLEDGE BASE:
{faq_content}
"""

# Main chat loop
def run_agent():
    BUSINESS_NAME = "Omega Insurance Brokers LLC"
    AGENT_NAME    = "Aria"
    FAQ_PATH      = "knowledge/test_clients/omega_insurance_faq.txt"

    faq_content   = load_faq(FAQ_PATH)
    system_prompt = build_system_prompt(BUSINESS_NAME, AGENT_NAME, faq_content)
    client        = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    conversation_history = []

    print("\n" + "="*50)
    print(f"  AgentDesk — {BUSINESS_NAME}")
    print("="*50)
    print("  Type 'quit' to exit | 'reset' to restart")
    print("="*50 + "\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ["quit", "exit"]:
            print(f"\n{AGENT_NAME}: Thanks for reaching out! Have a great day!")
            break
        if user_input.lower() == "reset":
            conversation_history = []
            print("\n[Conversation reset]\n")
            continue

        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                system=system_prompt,
                messages=conversation_history
            )

            reply = response.content[0].text

            conversation_history.append({
                "role": "assistant",
                "content": reply
            })

            print(f"\n{AGENT_NAME}: {reply}\n")

        except anthropic.AuthenticationError:
            print("\nAPI key missing. Run: export ANTHROPIC_API_KEY=your_key\n")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            break

if __name__ == "__main__":
    run_agent()