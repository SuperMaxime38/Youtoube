#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:31:29 2024

@author: theo.polica
"""
import os, secrets

from Projet import app
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True
    app.config['UPLOAD_FOLDER'] = os.getcwd() + '\\Projet\\static\\videos'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024 # 16 Go
    app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'mkv'}
    app.config['SECRET_KEY'] = secrets.token_hex()

    app.run(debug = True)