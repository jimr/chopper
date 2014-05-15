#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile

from bocho import bocho
from flask import Flask, make_response, request, render_template
from werkzeug import secure_filename


app = Flask(__name__)

DEBUG = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/chop', methods=['POST'])
def chop():
    pages = request.args.get('pages')
    if pages:
        pages = pages.split(',')

    f = request.files['file']
    fd, out_path = tempfile.mkstemp(
        suffix=secure_filename(f.filename),
        dir='upload',
    )
    os.close(fd)
    f.save(out_path)

    file_path = bocho(
        out_path, pages=pages, angle=25, zoom=1.35, reverse=True, affine=True,
        offset=(14, -5), spacing=(40, 0), border=4, use_convert=True,
    )

    with open(file_path) as f:
        response = make_response(f.read())
        response.headers['Content-Type'] = 'image/png'
        return response


if __name__ == '__main__':
    app.debug = DEBUG
    app.run(port=6000)
