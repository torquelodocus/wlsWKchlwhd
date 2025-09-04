from flask import Flask, jsonify, send_from_directory
import csv
import re

app = Flask(__name__, template_folder='templates', static_folder='templates/static')

def parse_time(t):
    m = re.match(r"(\d+)'(\d+\.\d+)", t)
    if m:
        minutes = int(m.group(1))
        seconds = float(m.group(2))
        return minutes * 60 + seconds
    else:
        return 0.0

def parse_student_id(s):
    # 숫자+이름 형태면 전체 반환, 숫자만 있으면 숫자만 반환
    m = re.match(r"^(\d+)(.*)", s)
    if m:
        num = m.group(1)
        name = m.group(2).strip()
        if name:
            return num + name
        else:
            return num
    else:
        return s

from flask import render_template

@app.route('/')
def index():
    return render_template('live_results.html')

@app.route('/api/results')
def get_results():
    results = []
    try:
        with open('score_result.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 5:
                    # 자동차 기록
                    student_id = parse_student_id(row[0])
                    try:
                        lap1 = parse_time(row[1])
                        lap2 = parse_time(row[2])
                        lap3 = parse_time(row[3])
                        total = parse_time(row[4])
                        results.append({
                            'studentId': student_id,
                            'lap1': lap1,
                            'lap2': lap2,
                            'lap3': lap3,
                            'total': total,
                            'type': 'race'
                        })
                    except:
                        continue
                elif len(row) == 3 and row[1] == 'plane':
                    # 비행기 기록
                    student_id = parse_student_id(row[0])
                    try:
                        score = int(row[2])
                        results.append({
                            'studentId': student_id,
                            'score': score,
                            'type': 'plane'
                        })
                    except:
                        continue
    except FileNotFoundError:
        pass
    # 자동차는 시간 오름차순, 비행기는 점수 내림차순
    race_results = [r for r in results if r.get('type') == 'race']
    plane_results = [r for r in results if r.get('type') == 'plane']
    race_results.sort(key=lambda x: x['total'])
    plane_results.sort(key=lambda x: -x['score'])
    return jsonify(race_results + plane_results)


if __name__ == '__main__':
    app.run(debug=True)

