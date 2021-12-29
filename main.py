from flask import Flask, render_template, request, send_file
import sys
from flask.helpers import flash, url_for
import pytube
import logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)



app = Flask(__name__)
app.secret_key='mysecretkey'

@app.route('/', methods=['POST','GET'])
def downloader():
    
    if request.method == 'POST':
        try:
            
            video_url = request.form['url']
            format = request.form.get('select')
            print(format)
            if format == 'audio':
                
                yt = pytube.YouTube(video_url)
                
                audio = yt.streams.filter(only_audio=True,).order_by('abr').first().download()
                    
                fname = audio.split('//')[-1]
                
                return send_file(fname, as_attachment=True)

            elif format == 'video':
                
                yt = pytube.YouTube(video_url)
                    
                video = yt.streams.filter(progressive=True, res='720p').first().download()
                
                fname = video.split('//')[-1]

                return send_file(fname, as_attachment=True)

            else:
                flash('Selecciona un formato')

        except:
            flash('URL incorrecto')
    return render_template('home.html')






if __name__=='__main__':
    app.run(debug=True)
