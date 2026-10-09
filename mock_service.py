import time

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/external/status", methods=["GET"])
def external_status():
    mode = request.args.get("mode", "normal")

    if mode == "error":
        return jsonify({
            "status": "error",
            "message": "Simulated external service failure"
        }), 500

    if mode == "timeout":
        time.sleep(5)

    return jsonify({
        "status": "ok",
        "source": "mock_external_service"
    }), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )
    