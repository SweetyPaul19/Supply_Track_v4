from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    # Use socketio.run instead of app.run to support real-time WebSockets
    socketio.run(app, debug=True, port=5000)