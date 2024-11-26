

from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import chess.engine
import random

app = Flask(__name__)
CORS(app)

# Khởi tạo trò chơi cờ vua
board = chess.Board()

@app.route('/move', methods=['POST'])
def get_ai_move():
    global board

    # Lấy nước đi từ request của client
    data = request.json
    move = data.get('move')
    if move:
        try:
            # Áp dụng nước đi của người chơi
            board.push_uci(move)
        except ValueError:
            return jsonify({"error": "Invalid move"}), 400

    # Sử dụng AI để tính nước đi
    with chess.engine.SimpleEngine.popen_uci(r"C:\Users\dotha\OneDrive\Desktop\CHESS\stockfish\stockfish") as engine:
        # Phân tích các nước đi với giới hạn thời gian 1 giây
        info = engine.analyse(board, chess.engine.Limit(time=1.0), multipv=5)  # multipv=5 để lấy top 5 nước đi

        # Lấy danh sách các nước đi
        possible_moves = [entry["pv"][0] for entry in info]  # Lấy nước đi đầu tiên trong mỗi dòng PV

        # Chọn ngẫu nhiên một nước đi
        ai_move = random.choice(possible_moves)

        # Thực hiện nước đi
        board.push(ai_move)

    return jsonify({"move": ai_move.uci(), "fen": board.fen()})


@app.route('/newgame', methods=['POST'])
def new_game():
    global board
    board.reset()
    print("Board reset to initial position:", board.fen())  # Thêm logging để kiểm tra trạng thái của board
    return jsonify({"fen": board.fen()})

if __name__ == '__main__':
    app.run(debug=True)