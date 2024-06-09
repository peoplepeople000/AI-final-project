import os
import sys
sys.path.append("../")
import yaml
import json
import numpy as np
import torch
import math
import copy
import re
from transformers import AutoModel, AutoTokenizer
from finetune.utils import gen_midi
from flask import Flask, request, jsonify, send_from_directory



def flatten_input(data):
	#use gpt generating lyric from input
	#data format should be:
	#	"type:pop;mood:happy;lyric:"
	[TYPE,MOOD,LYRIC] = data
 
	if LYRIC == "":
		prompt='Create a '+TYPE+' song on '+MOOD+'.'
	else:
		prompt='Create a '+TYPE+' song on '+MOOD+' and the word ['+LYRIC+'] should be in the lyric.'

	return prompt


def predict(prompt):
	tokenizer = AutoTokenizer.from_pretrained("Mar2Ding/songcomposer_sft", trust_remote_code=True)
	model = AutoModel.from_pretrained("Mar2Ding/songcomposer_sft", trust_remote_code=True).cuda().half()

	
	song=model.inference(prompt, tokenizer) #need to re-write inference_pretrain function in modeling_internlm2.py?　For getting the data


	## get song.mid song.txt in this folder
	gen_midi(song, 'song')



app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')

#@app.route('/')
#def serve():
#    return send_from_directory(app.static_folder, 'index.html')

@app.route('/generate-music/', methods=['POST'])
def generate_music():
    try:
        data = request.json
        mood = data.get('mood')
        genre = data.get('genre')
        lyrics = data.get('lyrics')

        prompt = flatten_input([genre,mood,lyrics])
        print(prompt)
        predict(prompt)
        
        #回傳歌詞
        file = open("song.txt", 'rb')
        return send_file(file,as_attachment=True, attachment_filename='lyric.txt')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Music Generator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to right, #74ebd5, #acb6e5);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        h1 {
            text-align: center;
            color: #ffffff;
        }
        form {
            background: rgba(255, 255, 255, 0.8);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 300px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        input, textarea, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
            font-size: 16px;
        }
        button {
            background-color: #0056b3;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #003974;
        }
        #result {
            margin-top: 20px;
            text-align: center;
            color: #333;
        }
        /* 添加一些裝飾性背景圖案 */
        body::after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('https://www.transparenttextures.com/patterns/asfalt-light.png');
            opacity: 0.1;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <div>
        <h1>Music Generator</h1>
        <form id="musicForm">
            <label for="mood">Mood:</label>
            <input type="text" id="mood" placeholder="Input your mood">
            <label for="genre">Genre:</label>
            <input type="text" id="genre" placeholder="Input the song genre">
            <label for="lyrics">Lyrics:</label>
            <textarea id="lyrics" placeholder="Input the lyrics"></textarea>
            <button type="button" onclick="generateMusic()">GO!</button>
        </form>
        <div id="result"></div>
    </div>
    <script>
        function generateMusic() {
            var mood = document.getElementById('mood').value;
            var genre = document.getElementById('genre').value;
            var lyrics = document.getElementById('lyrics').value;
            fetch('/generate-music', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mood: mood, genre: genre, lyrics: lyrics })
            })
            .then(response => response.blob())
            .then(blob => {
                var url = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = 'generated_music.mp3';
                a.click();
                document.getElementById('result').innerHTML = '音樂已生成並下載。';
            })
            .catch(error => {
                document.getElementById('result').innerHTML = '生成音樂時出錯: ' + error;
            });
        }
    </script>
</body>
</html>

'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)