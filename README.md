# MusicGenerator
## Introduction
This is a web app for user to input mood and genre, and it can generate music by using MusicLM.

## Pre-require
### Package
* torch
* torchaudio
* torchvision
* einops
* vector-quantize-pytorch
* librosa
* torchlibrosa
* ftfy
* tqdm
* encodec
* gdown
* accelerate
* beartype
* joblib
* h5py
* scikit-learn
* wget
* numpy
* transformers
* flask

## How to use
You need the musicLM pretrained-model.
It can fetch on the web https://github.com/zhvng/open-musiclm/
It's a part of the checkpoint.

Put unzipped files into the folder named 'weight'.

And ```git clone https://github.com/zhvng/open-musiclm.git``` into the same folder of the folder 'weight'.

Download the 'script' folder  and then replace the folder in open-musiclm.

Now, go to ```open-musiclm/scripts```. 

Use the command   ```python infer_top_match.py  --num_samples 1 --num_top_matches 1 --duration 30 --semantic_path ..\..\weight\semantic.transformer.14000.pt --coarse_path ..\..\weight\coarse.transformer.18000.pt --fine_path ..\..\weight\fine.transformer.24000.pt --rvq_path ..\..\weight\clap.rvq.950_no_fusion.pt --kmeans_path ..\..\weight\kmeans_10s_no_fusion.joblib --model_config ..\..\weight\musiclm_large_small_context.json``` to start.

Copy the address on terminal and paste it on the browser.

Enjoy creating a new song whatever you want.

