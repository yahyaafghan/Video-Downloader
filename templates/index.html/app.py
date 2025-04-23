from flask import Flask, render_template, request, send_file
from pytube import YouTube
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_data = None
    error = None
    if request.method == 'POST':
        url = request.form['url']
        quality = request.form['quality']
        proxy = request.form.get('proxy', '')

        try:
            yt = YouTube(url)
            video_data = {
                'title': yt.title,
                'thumbnail': yt.thumbnail_url,
                'url': url,
                'quality': quality,
                'proxy': proxy
            }
        except Exception as e:
            error = f"Error: {e}"

    return render_template('index.html', video=video_data, error=error)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    quality = request.form['quality']
    proxy = request.form.get('proxy', '')
    temp_file = f"{uuid.uuid4()}.mp4" if quality == 'video' else f"{uuid.uuid4()}.mp3"

    ydl_opts = {
        'format': 'bestaudio' if quality == 'audio' else 'best',
        'outtmpl': temp_file,
        'quiet': True,
        'proxy': proxy if proxy else None,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(temp_file, as_attachment=True)
    except Exception as e:
        return f"Download failed: {str(e)}"
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == '__main__':
    app.run(debug=True)
