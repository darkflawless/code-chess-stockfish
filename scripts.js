async function makeMove(source, target) {
    const move = source + target; // Nước đi dạng UCI (vd: "e2e4")

    try {
        // Gửi yêu cầu POST đến server Python
        const response = await fetch('http://127.0.0.1:5000/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ move: move }),
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error); // Thông báo lỗi
            return 'snapback';
        }

        board.position(data.fen, true);
        game.load(data.fen);
        updateStatus(); // Cập nhật trạng thái
        // Cập nhật bàn cờ với nước đi của AI


    } catch (err) {
        console.error('Lỗi khi giao tiếp với server:', err);
        alert('Không thể kết nối với server.');
        return 'snapback';
    }
}

async function newgame() {
    try {
        // Gửi yêu cầu POST đến server Python
        const response = await fetch('http://127.0.0.1:5000/newgame',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });


    const data = await response.json();
    console.log("New game response:", data);  // Thêm logging để kiểm tra phản hồi từ server
    board.position(data.fen, true);
    game.load(data.fen);
    updateStatus(); // Cập nhật trạng thái
    
    } catch (err) {
        console.error('Lỗi khi giao tiếp với server:', err);
        alert('Không thể kết nối với server.');
        return 'snapback';
    }
}