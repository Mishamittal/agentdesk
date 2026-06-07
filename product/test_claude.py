import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=256,
    messages=[{"role": "user", "content": "Say hello and confirm you're working!"}]
)
print(message.content[0].text)
