import socket

HOST = '10.116.0.70'         # 모든 IP에서 접속 허용
PORT = 50007      # 클라이언트와 맞춰야 함

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("서버 실행 중...")

    while True:
        conn, addr = s.accept()
        with conn:
            print('접속:', addr)
            data = conn.recv(1024).decode('utf-8')
            print('받은 데이터:', data)

            # --- 저장 부분 ---
            with open("score_result.csv", "a", encoding="utf-8") as f:
                f.write(data + "\n")
