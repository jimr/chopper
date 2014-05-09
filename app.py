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
        out_path, pages, angle=25, zoom=1.15, reverse=True, affine=True,
        offset=(20, 0), spacing=(47, 0),
    )

    with open(file_path) as f:
        response = make_response(f.read())
        response.headers['Content-Type'] = 'image/png'
        return response


if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host='0.0.0.0', port=6000)
