from main import gen_example
from flask import Flask, escape, request, jsonify, send_from_directory
import subprocess
import sys
import ctypes

app = Flask(__name__)

@app.route('/generate')
def hello():
    sentence = request.args.get("sentence", "")
    word = request.args.get("highlight", "")
    dataset = request.args.get("dataset", "COCO")
    if sentence == "":
        return f""

    with open("../data/%s/example.txt"%("birds" if dataset=="CUB" else "coco"), "w") as f_ex:
        f_ex.write(sentence)
    yml_path = "cfg/eval_bird.yml" if dataset == "CUB" else "cfg/eval_coco.yml"
    if word != "":
        highlight = sentence.split(' ').index(word)
    else:
        highlight = 0
    h = ctypes.c_size_t(hash((sentence, word, dataset))).value
    p = subprocess.Popen("python main.py --cfg %s --gpu 0 --output_file_name ../gen/%d --highlight %d"%(yml_path, h, highlight),
        cwd="/home/ubuntu/text2image/ControlGAN/code", stdout=sys.stdout, stderr=sys.stderr, shell=True).communicate()
    if word != "":
        return jsonify(
            image_url='/imgs/%d_1.jpg'%(h)
        )
    else:
        return jsonify(
            image_url="/imgs/%d_0.png"%(h)
        )

@app.route('/imgs/<path:path>')
def send_img(path):
    return send_from_directory('/home/ubuntu/text2image/ControlGAN/gen', path)

if __name__ == "__main__":
    app.run()