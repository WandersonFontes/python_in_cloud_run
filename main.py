from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/event', methods=['POST'])
def handle_event():
    try:
        event = request.get_json()
        if not event:
            return jsonify({"error": "Invalid event format"}), 400

        # Print the received event
        print("Received event:", event)

        # Optionally, return a response
        return jsonify({"message": "Event received successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)