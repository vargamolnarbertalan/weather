from flask import Flask, request, jsonify
import os
import json
from flask_cors import CORS
from playwright.sync_api import sync_playwright
from flask import Response

app = Flask(__name__)
CORS(app)
DATA_FILE = 'data.json'


@app.route('/getData', methods=['GET'])
def get_data():
    if not os.path.exists(DATA_FILE):
        return jsonify({'status': 'error', 'message': 'No data found'}), 404

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Return proper UTF-8 characters, not escaped ones
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        content_type='application/json; charset=utf-8'
    )


@app.route('/scrapeMet', methods=['GET'])
def scrape_met():
    try:
        with sync_playwright() as p:
            data = []
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://www.met.hu/idojaras/tavaink/balaton/mert_adatok/main.php")

            page.wait_for_selector("body > table.tbl-def1")

            for x in range(15):
                place = page.query_selector(
                    f"body > table.tbl-def1 > tbody > tr:nth-child({x+1}) > th > a")
                windDir = page.query_selector(
                    f"body > table.tbl-def1 > tbody > tr:nth-child({x+1}) > td:nth-child(3)")
                windSpeed = page.query_selector(
                    f"body > table.tbl-def1 > tbody > tr:nth-child({x+1}) > td:nth-child(4)")
                beaufort = page.query_selector(
                    f"body > table.tbl-def1 > tbody > tr:nth-child({x+1}) > td:nth-child(5)")
                avgWindDir = page.query_selector(
                    f"body > table.tbl-def1 > tbody > tr:nth-child({x+1}) > td:nth-child(7)")
                avgWindSpeed = page.query_selector(
                    f"body > table.tbl-def1 > tbody > tr:nth-child({x+1}) > td:nth-child(8)")
                avgBeaufort = page.query_selector(
                    f"body > table.tbl-def1 > tbody > tr:nth-child({x+1}) > td:nth-child(9)")
                # print(place,windDir,windSpeed,beaufort,avgWindDir,avgWindSpeed,avgBeaufort)
                data.append({
                    "place" : place.inner_text(),
                    "windDir": windDir.inner_text(),
                    "windSpeed": windSpeed.inner_text(),
                    "beaufort": beaufort.inner_text(),
                    "avgWindDir": avgWindDir.inner_text(),
                    "avgWindSpeed": avgWindSpeed.inner_text(),
                    "avgBeaufort": avgBeaufort.inner_text()
                })

            browser.close()

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


        return jsonify({'status': 'success', 'message': 'Scraped and saved data', 'items': len(data)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7123)