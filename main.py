from flask import Request, jsonify

def handle_event(request: Request):
    try:
        # Parse JSON request body
        event = request.get_json()
        if not event:
            return jsonify({"error": "Invalid event format"}), 400

        # Print the received event
        print("Received event:", event)

        # Return a success response
        return jsonify({"message": "Event received successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500