import http.client
import json

# Set the system prompt
SYSTEM_PROMPT = 'You are a concise and informative assistant. Keep responses to a few sentences, very short. seperate with newlines after each sentence.'

# Maintain conversation history as a list of strings
conversation_history = []

def stream_llm_response(natural_query):
    """Streams responses from the LLM for the given natural language query."""
    try:
        # Add the system prompt at the start if it's the first query
        if not conversation_history:
            conversation_history.append(SYSTEM_PROMPT)
        
        # Append the user's query to the conversation history
        conversation_history.append(f"User: {natural_query}")

        # Create the connection
        conn = http.client.HTTPConnection("localhost", 11434)

        # Prepare the flattened prompt
        full_prompt = "\n".join(conversation_history)

        # Prepare the JSON data
        data = json.dumps({
            "model": "llama3.1",
            "prompt": full_prompt,
            "stream": True
        })

        # Setup the headers
        headers = {"Content-Type": "application/json"}

        # Send the request
        conn.request("POST", "/api/generate", body=data, headers=headers)

        # Get the response
        response = conn.getresponse()

        # Check for success
        if response.status != 200:
            raise Exception(f"Request failed with status {response.status}: {response.reason}")
        
        # Loop through the response
        for line in response:
            if line:
                try:
                    # Decode the line to UTF-8
                    line = line.decode('utf-8')

                    # Parse the JSON
                    parsed_line = json.loads(line)

                    # If there is a response, yield it
                    if 'response' in parsed_line:
                        yield parsed_line['response']
                        
                        # Append the model's response to conversation history
                        conversation_history.append(f"Assistant: {parsed_line['response']}")
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"Error decoding line: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    # Send a test query
    for chunk in stream_llm_response("What is 25 squared?"):
        print(chunk, end='', flush=True)
