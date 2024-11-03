from flask import Flask, request, jsonify 
import requests
import json 

app = Flask(__name__)

@app.route('/')
def hello():
    return '{"translation":"hello"}'

@app.route('/api/chat', methods=['POST'])
def ollama_chat():
    print("request received ",  request.get_json())
    url = 'http://localhost:11434/api/chat'
    data = {
                "model": "qwen2.5-coder:7b", # 模型名称,若其他模型则需要更改
                "messages": [
                    {
                        "role": "user",
                        "content": "你同时是中译英和英译中的翻译专家，翻译如下内容: " + request.get_json().get('text'),
                    }
                ],
                "stream": False
            }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
    # 处理成功响应
        result = response.json()
        print(result)
        return jsonify({"data":result['message']['content']})
    else:
    # 处理失败响应
        print('Error:', response.status_code, response.text)
        return jsonify({"data":response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
