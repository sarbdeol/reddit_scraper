from flask import Flask, render_template, request, send_file,send_from_directory
from flask_socketio import SocketIO, emit
import os
from ai_api import generate_script

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
    script = generate_script(url)

    file_name = 'reddit_script.txt'
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(script)
    
    emit('completed', {'file_name': file_name})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    socketio.run(app,debug=True,host='0.0.0.0', port=5000)

