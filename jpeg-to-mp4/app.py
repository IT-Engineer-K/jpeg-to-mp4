from flask import Flask, render_template, send_file
import flask
import os
import cv2
import shutil
app = Flask(__name__, static_url_path='/static')


UPLOAD_FOLDER = 'templates/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def aaa():
    return '''
    <html>
<body>
<form action = "/upload" method = "POST" enctype = "multipart/form-data">
    <input type = "file" name = "file" multiple=""/>
    <input type = "submit"/>
</form>
</body>
</html>
'''
def mp4():
    directory_name = "templates/images"
    date_directories = os.listdir(directory_name)
    img = cv2.imread(directory_name+"/"+date_directories[0])
    height, width = img.shape[:2]
    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
    video  = cv2.VideoWriter("templates/video.mp4", fourcc, 30, (width, height))
    for dir in sorted(date_directories):
        filename = os.path.join(directory_name, dir)
        print(filename)
        img = cv2.imread(filename)
        video.write(img)
    video.release()

@app.route('/upload', methods=['GET','POST'])
def upload():
    shutil.rmtree(UPLOAD_FOLDER)
    os.mkdir(UPLOAD_FOLDER)
    if flask.request.method == "POST":
        fileNumber = 0
        files = flask.request.files.getlist("file")
        for file in files:
            file.filename = s = '{0:04}'.format(fileNumber) + ".jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            fileNumber += 1
        mp4()
    return render_template("extend.html", title="Flask")

@app.route('/download')
def download_file():
    p = 'video.mp4'
    return send_file(p,as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)