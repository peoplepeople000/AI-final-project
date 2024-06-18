import os
import sys

import torch
import torchaudio
from einops import rearrange
from pathlib import Path
import argparse

import yaml
import json
import numpy as np
import math
import copy
import re
from flask import Flask, request, jsonify,send_file

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from open_musiclm.config import load_model_config, create_musiclm_from_config


def flatten_input(data):
    [TYPE,MOOD] = data


    prompt='Create a '+MOOD+' song with '+TYPE+'style.'

    return prompt


def predict(prompt):
    print(f'prompt: {prompt}')

    prime_wave, prime_wave_sample_hz = None, None
    if input_audio is not None:
        prime_wave, prime_wave_sample_hz = torchaudio.load(input_audio)
        prime_wave = prime_wave.to(device)

    generated_wave, similarities = musiclm.generate_top_match(
        text=args.prompt,
        prime_wave=prime_wave,
        prime_wave_sample_hz=prime_wave_sample_hz,
        num_samples=args.num_samples,
        num_top_matches=args.num_top_matches,
        output_seconds=duration,
        semantic_window_seconds=model_config.global_cfg.semantic_audio_length_seconds,
        coarse_window_seconds=model_config.global_cfg.coarse_audio_length_seconds,
        fine_window_seconds=model_config.global_cfg.fine_audio_length_seconds,
        semantic_steps_per_second=model_config.hubert_kmeans_cfg.output_hz,
        acoustic_steps_per_second=model_config.encodec_cfg.output_hz,
        return_coarse_generated_wave=return_coarse_wave,
    )

    for i, (wave, sim) in enumerate(zip(generated_wave, similarities)):
        wave = rearrange(wave, 'b n -> b 1 n').detach().cpu()
        print(f'prompt: {prompt[i]}')
        print(f'topk similarities: {sim}')
        for j, w in enumerate(wave):
            torchaudio.save(Path(results_folder) + '\\music.wav', w, musiclm.neural_codec.sample_rate)



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

        prompt = flatten_input([genre,mood])
        print(prompt)
        predict(prompt)
        
        #回傳音樂
        path_to_wav = 'results\\1.wav'
        return send_file(path_to_wav,as_attachment=True)
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
            <button type="button" onclick="generateMusic()">GO!</button>
        </form>
        <div id="result"></div>
    </div>
    <script>
        function generateMusic() {
            var mood = document.getElementById('mood').value;
            var genre = document.getElementById('genre').value;
            fetch('/generate-music', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mood: mood, genre: genre})
            })
            .then(response => response.blob())
            .then(blob => {
                var url = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = 'music.wav';
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

parser = argparse.ArgumentParser(description='run inference on trained musiclm model')

#parser.add_argument('prompt', help='prompts to generate audio for', type=str, nargs='+')
parser.add_argument('--num_samples', default=4, type=int)
parser.add_argument('--num_top_matches', default=1, type=int)
parser.add_argument('--input_audio', default=None, type=str, help='input audio to condition on and generate continuations from')
parser.add_argument('--model_config', default='./configs/model/musiclm_small.json', help='path to model config')
parser.add_argument('--semantic_path', required=True, help='path to semantic stage checkpoint')
parser.add_argument('--coarse_path', required=True, help='path to coarse stage checkpoint')
parser.add_argument('--fine_path', required=True, help='path to fine stage checkpoint')
parser.add_argument('--rvq_path', default='./checkpoints/clap.rvq.350.pt')
parser.add_argument('--kmeans_path', default='./results/hubert_kmeans/kmeans.joblib')
parser.add_argument('--results_folder', default='./results', type=str)
parser.add_argument('--return_coarse_wave', default=False, action=argparse.BooleanOptionalAction)
parser.add_argument('--duration', default=4, type=float, help='duration of audio to generate in seconds')
parser.add_argument('--seed', default=0)

args = parser.parse_args()

model_config = load_model_config(args.model_config)

semantic_path = args.semantic_path
coarse_path = args.coarse_path
fine_path = args.fine_path
input_audio = args.input_audio
return_coarse_wave = args.return_coarse_wave
duration = args.duration
kmeans_path = args.kmeans_path
rvq_path = args.rvq_path
seed = args.seed
results_folder = args.results_folder

Path(results_folder).mkdir(parents=True, exist_ok=True)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

musiclm = create_musiclm_from_config(
    model_config=model_config,
    semantic_path=semantic_path,
    coarse_path=coarse_path,
    fine_path=fine_path,
    rvq_path=rvq_path,
    kmeans_path=kmeans_path,
    device=device)

torch.manual_seed(seed)

app.run(host='0.0.0.0', port=5000, debug=True)
