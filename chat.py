from gemini.chat_session import ChatSession

def main():
    # Initialize the chat session with the desired model
    chat_session = ChatSession(model_name="gemini-pro")

    # Start the chat session explicitly (optional, as sending a message would auto-start it)
    chat_session.start_chat()

    # Send a greeting message synchronously and print the response
    response = chat_session.send_message("Hello")
    print(f"Response: {response.text}")

    # Demonstrate sending another message
    response = chat_session.send_message("Can you explain the concept of machine learning?")
    print(f"Response: {response.text}")

    # Rewind the last message if needed
    print("Rewinding the last message.")
    chat_session.rewind()

    # Send a message asynchronously
    print("Sending a message asynchronously:")
    async_response = chat_session.send_message_async("Tell me a joke.")
    print(f"Async Response: {async_response.text}")

    # Note: The asynchronous call here is made synchronous for simplicity by calling result()
    # In a real-world scenario, async operations would be handled differently.

if __name__ == "__main__":
    main()
