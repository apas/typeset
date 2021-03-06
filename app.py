from flask import Flask, request, redirect, send_from_directory, url_for, after_this_request, Response
from werkzeug.utils import secure_filename
from glob import glob
import os
import shutil
import subprocess
import pypandoc

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(["md", "txt", "png", "jpg", "bib", "csl"])
app.config["UPLOAD_FOLDER"] = "uploads"
uploads = app.config["UPLOAD_FOLDER"]
os.environ.setdefault('PYPANDOC_PANDOC', '/home/linuxbrew/.linuxbrew/bin/pandoc')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', -1)[-1].lower() in ALLOWED_EXTENSIONS

def prep():
    for file in os.listdir(uploads):
        file_path = os.path.join(uploads, file)

        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Excception as e:
            print(e)

def pandoc(md_file):
    filters = ["/home/linuxbrew/.linuxbrew/bin/pandoc-crossref",
                "/home/linuxbrew/.linuxbrew/bin/pandoc-citeproc"]
    pdoc_args = ["--template=default.latex",
                "-f", "markdown+raw_tex+yaml_metadata_block",
                "-Mreference-section-title=References",
                "-Mlink-citations=true",
                "-s",
                "--pdf-engine", "/home/linuxbrew/.linuxbrew/bin/pdflatex",
                "--highlight-style", "pygments",
                "-V", "urlcolor=blue"]

    pdf = md_file.split(".", -1)[0] + ".pdf"

    output = pypandoc.convert_file(md_file, format="md", to="latex",
                                    extra_args=pdoc_args, filters=filters,
                                    outputfile=pdf)

def find_files(directory, extension):
    return glob(os.path.join(directory, "*.{}".format(extension)))

@app.route("/")
def index():
   return "And all watched over by machines of loving grace." 

@app.route("/<path:path>/")
def url(path):
    return "And all watched over by machines of loving grace."

@app.route("/md/", methods=["POST"])
def md():
    if request.method == "POST":
        if "file" not in request.files:
            return "failure"

        file = request.files["file"]

        if file and allowed_file(file.filename):
            prep()

            md_file = secure_filename(file.filename)
            if md_file.split(".", -1)[-1] == "txt":
                md_file += ".md"

            md_file = os.path.join(uploads, md_file)
            file.save(md_file)
            pandoc(md_file)
            return "success"

        return "failure"

@app.route("/pdf/")
def pdf():
    pdf = find_files(uploads, "pdf")
    pdf = pdf[0].split("/", 1)[-1]

    @after_this_request
    def clean(response):
        try:
            prep()
        except Exception as e:
            print(e)
        return response

    return send_from_directory(uploads, pdf, as_attachment=True)

@app.route("/robots.txt")
def robots():
    Disallow = lambda string: "Disallow: {0}".format(string)

    return Response("User-agent: *\n{0}\n".format("\n".join([
        Disallow("/")])))
