from flask import Flask, render_template, request, send_file,send_from_directory
from flask_socketio import SocketIO, emit
import os
from ai_crawol import generate_script

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('scrape')
def handle_scrape(data):
    url = data['url']
    def progress_callback(progress):
        emit('progress', {'progress': progress}, broadcast=True)
    # script = generate_script(url)
    script = generate_script(url, progress_callback)
    # Simulating progress for demonstration purposes
    # for progress in range(0, 101, 10):
    #     socketio.sleep(0.5)  # Simulate a delay for each step
    #     emit('progress', {'progress': progress})

    file_name = 'reddit_script.txt'
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(script)
    
    emit('completed', {'file_name': file_name})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
