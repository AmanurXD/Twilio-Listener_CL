from flask import Flask, request, jsonify

app = Flask(__name__)

# A simple in-memory dictionary to store messages.
# The key will be the Twilio phone number, the value will be the SMS body.
# This is fine for this use case as Render's free tier may restart,
# but a new number is purchased each time anyway.
MESSAGES_RECEIVED = {}

@app.route('/sms', methods=['POST'])
def receive_sms():
    """Endpoint for Twilio to send SMS data to."""
    try:
        to_number = request.form.get('To')
        message_body = request.form.get('Body')
        
        if not to_number or not message_body:
            return "Missing data", 400
        
        # Store the message body, keyed by the recipient number
        MESSAGES_RECEIVED[to_number] = message_body
        
        print(f"Received message for {to_number}: '{message_body}'")
        return "<Response></Response>", 200
    except Exception as e:
        print(f"Error in /sms: {e}")
        return "Server Error", 500

@app.route('/get-message/<phone_number>', methods=['GET'])
def get_message(phone_number):
    """Endpoint for the local client to poll for a message."""
    # Check if a message for this number has been received
    if phone_number in MESSAGES_RECEIVED:
        # Retrieve the message
        message = MESSAGES_RECEIVED[phone_number]
        # Important: Delete the message after retrieving it so it's not fetched again
        del MESSAGES_RECEIVED[phone_number]
        return jsonify({"status": "found", "body": message})
    else:
        return jsonify({"status": "not_found"})

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint for Render."""
    return "OK", 200

if __name__ == '__main__':
    # This part is for local testing only. Gunicorn will run the app on Render.
    app.run(port=5000)
