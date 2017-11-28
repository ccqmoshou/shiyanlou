#!/usr/bin/python3
# -*- coding:utf-8 -*-


import os.path
import json
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


class Files(object):
    #    directory = '/home/shiyanlou/files'
    directory = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'files')

    def __init__(self):
        self._files = self._load_all_files()

    def _load_all_files(self):
        result = {}
        for filename in os.listdir(self.directory):
            filepath = os.path.join(self.directory, filename)
            with open(filepath) as f:
                result[filename[:-5]] = json.loads(f.read())
        return result

    def get_title(self):
        _title_list = []
        for key in self._files:
            _title = self._files[key]['title']
#        for item in self._files.values():
#            _title = item['title']
            _title_list.append(_title)
        return _title_list

    def get_content(self, filename):
        _content = self._files.get(filename)
        return _content


files = Files()


@app.route('/')
def index():
    title_list = files.get_title()
    return render_template('index.html', title_list=title_list)


@app.route('/files/<filename>')
def file(filename):
    file_content = files.get_content(filename)
    if not file_content:
        abort(404)
    return render_template('file.html', file_content=file_content)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
