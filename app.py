import os
from flask import Flask, render_template, send_file
from qr import get_local_ip, make_qr_image

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))

def get_public_url():
    # Render.com では環境変数 RENDER_EXTERNAL_URL が自動セットされる
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    if render_url:
        return render_url
    # ローカル実行時はLAN IPを使う
    ip = get_local_ip()
    return f"http://{ip}:{PORT}"

@app.route("/")
def index():
    url = get_public_url()
    return render_template("index.html", qr_url=url)

@app.route("/qr.png")
def qr_image():
    url = get_public_url()
    buf = make_qr_image(url)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    ip = get_local_ip()
    print(f"\n  アプリURL: http://{ip}:{PORT}")
    print(f"  QRコード: http://{ip}:{PORT}/qr.png\n")
    app.run(debug=True, host="0.0.0.0", port=PORT)
