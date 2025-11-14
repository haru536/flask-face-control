from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# === 1. 表示用HTML ===　27行目はリモコン用HTMLの通常の顔と同じにする
display_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Display</title>
    <style>
      body {
        background-color: white;       /* 背景を白に */
        color: black;                  /* 絵文字の色（背景と対比） */
        display: flex;                 /* 中央配置用 */
        justify-content: center;       /* 横方向の中央揃え */
        align-items: center;           /* 縦方向の中央揃え */
        height: 100vh;                 /* 画面全体を使う */
        margin: 0;                     /* 余白なし */
        font-size: 40vh;               /* 顔を大きく！ */
      }
    </style>
  </head>
  </body>
    <div id="status">•＿•</div>

    <script src="https://cdn.socket.io/4.3.2/socket.io.min.js"></script>
    <script>
      const socket = io();
      let currentFace = "•＿•"; // 現在の表情を保持
      const faceElem = document.getElementById("status");
      let resetTimer = null;   // 戻す用のタイマーを記録

      // Flaskから表情が送られてきたとき
      socket.on('update', (msg) => {
        currentFace = msg;
        faceElem.innerText = currentFace;

        // === 通常以外の表情なら7秒後に戻す ===
        if (currentFace !== "•＿•") {
          // すでにタイマーが動いていたらリセット
          if (resetTimer) clearTimeout(resetTimer);

          resetTimer = setTimeout(() => {
            currentFace = "•＿•";
            faceElem.innerText = currentFace;
          }, 7000); // 7秒後に戻す
        }
      });

      // === 瞬き機能 ===
      function blink() {
        // 通常の顔のときだけ瞬き
        if (currentFace === "•＿•") {
         const blinkFace = "-＿-"; // ← 瞬き中の顔
         faceElem.innerText = blinkFace;
         setTimeout(() => {
           faceElem.innerText = currentFace;
         }, 100); // 0.1秒後に元の顔に戻す
        }
      }

      // 3秒ごとに瞬きする
      setInterval(blink, 3000);
    </script>
  </body>
</html>
"""

# === 2. リモコン用HTML ===　顔文字にすることもできる
remote_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Face Controler</title>
  </head>
  <body>
    <h1>Face Controller</h1>
    <button onclick="sendCommand('＾◡＾')">笑顔</button>
    <button onclick="sendCommand('≧ ◡ ≦')">照れ</button>
    <button onclick="sendCommand('>﹏<')">悲しい</button>
    <button onclick="sendCommand('-`ω´-')">キリっと</button>
    <button onclick="sendCommand('•＿•')">通常</button>
    <script src="https://cdn.socket.io/4.3.2/socket.io.min.js"></script>
    <script>
      const socket = io();
      function sendCommand(cmd) {
        socket.emit('control', cmd);
      }
    </script>
  </body>
</html>
"""

# === 3. Flaskルーティング ===
@app.route('/')
def display():
    return display_html

@app.route('/remote')
def remote():
    return remote_html

# === 4. Socket通信 ===
@socketio.on('control')
def handle_control(cmd):
    socketio.emit('update', cmd)

# === 5. 実行部 ===
if __name__ == '__main__':
    print("✅ サーバーを起動中... http://127.0.0.1:5000")
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)



