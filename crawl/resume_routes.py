from flask import Blueprint, request, jsonify, send_from_directory
from agent.resume import ResumeLoader
import os
import json
import shutil
import datetime

resume_bp = Blueprint("resume", __name__, url_prefix="/resume")


@resume_bp.route('/<user_id>', methods=['POST'])
def upload_resume(user_id):
    if 'file' not in request.files:
        return jsonify({"message": "没有文件上传"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "空文件"}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"message": "只允许PDF格式文件"}), 400

    pdf_name = os.path.splitext(file.filename)[0]
    save_dir = os.path.join("cache", user_id, "resume", pdf_name)
    if os.path.exists(save_dir):
        return jsonify({"message": "简历已存在"}), 400

    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, file.filename)
    file.save(save_path)

    with open(os.path.join(save_dir, "datetime.json"), "w") as f:
        js = {"create": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        json.dump(js, f, indent=4)

    return jsonify({"message": "上传成功", "path": save_path}), 200


@resume_bp.route('/<user_id>', methods=['GET'])
def get_resume_list(user_id):
    save_dir = os.path.join("cache", user_id, "resume")
    if not os.path.exists(save_dir):
        return jsonify({"message": "简历不存在"}), 404

    files = os.listdir(save_dir)
    files_datetime = []
    for x in files:
        meta_file = os.path.join(save_dir, x, "datetime.json")
        if os.path.exists(meta_file):
            with open(meta_file) as f:
                dt = json.load(f)["create"]
            files_datetime.append({"name": x, "datetime": dt})

    if not files_datetime:
        return jsonify({"message": "简历不存在", "files": []}), 200

    return jsonify({"message": "简历列表", "files": files_datetime}), 200

@resume_bp.route('/view', methods=['POST'])
def view_resume():
    data = request.get_json()
    user_id = str(data.get('userId'))
    if not user_id: 
        return {"code": 1, "msg": "userId 必填"}, 400
    file_name = data.get('file', '')
    file_dir = os.path.join("cache", user_id, "resume", file_name)
    file_path = os.path.join(file_dir, file_name + ".pdf")
    if not os.path.exists(file_path):
        return {"code": 1, "msg": "文件不存在"}, 404
    preview_url = f"/crawl/resume/{user_id}/{file_name}.pdf"
    return {"code": 0, "url": preview_url}

@resume_bp.route('/delete', methods=['POST'])
def delete_resume():
    data = request.get_json()
    user_id = data.get('userId')
    file_name = data.get('file', '')
    if not user_id or not file_name:
        return jsonify({"message": "参数不完整"}), 400

    save_dir = os.path.join("cache", user_id, "resume", file_name)
    if not os.path.exists(save_dir):
        return jsonify({"message": "简历不存在"}), 404

    shutil.rmtree(save_dir)
    return jsonify({"message": "删除成功"}), 200


@resume_bp.route('/<user_id>/<file_name>.pdf')
def preview_resume(user_id, file_name):
    file_dir = os.path.join("cache", user_id, "resume", file_name)
    return send_from_directory(file_dir, file_name + ".pdf")


def get_datetime(file_dir, key):
    with open(os.path.join(file_dir, "datetime.json"), "r") as f:
        js = json.load(f)
        return js.get(key, "")


@resume_bp.route('/parse/content', methods=['GET'])
def parse_resume_content():
    user_id = request.args.get('userId')
    file_name = request.args.get('file')
    if not user_id or not file_name:
        return jsonify({"message": "参数不完整"}), 400

    file_dir = os.path.join("cache", user_id, "resume", file_name)
    file_path = os.path.join(file_dir, file_name + ".pdf")
    if not os.path.exists(file_path):
        return jsonify({"message": "文件不存在"}), 404

    resume = ResumeLoader(file_path)
    resume.content
    return {"code": 0, "step": 1, "datetime": get_datetime(file_dir, "content")}


@resume_bp.route('/parse/summary', methods=['GET'])
def parse_resume_summary():
    user_id = request.args.get('userId')
    file_name = request.args.get('file')
    if not user_id or not file_name:
        return jsonify({"message": "参数不完整"}), 400

    file_dir = os.path.join("cache", user_id, "resume", file_name)
    file_path = os.path.join(file_dir, file_name + ".pdf")
    if not os.path.exists(file_path):
        return jsonify({"message": "文件不存在"}), 404

    resume = ResumeLoader(file_path)
    resume.summary
    return {"code": 0, "step": 2, "datetime": get_datetime(file_dir, "summary")}


@resume_bp.route('/parse/picture', methods=['GET'])
def parse_resume_picture():
    user_id = request.args.get('userId')
    file_name = request.args.get('file')
    if not user_id or not file_name:
        return jsonify({"message": "参数不完整"}), 400

    file_dir = os.path.join("cache", user_id, "resume", file_name)
    file_path = os.path.join(file_dir, file_name + ".pdf")
    if not os.path.exists(file_path):
        return jsonify({"message": "文件不存在"}), 404

    resume = ResumeLoader(file_path)
    resume.picture_path
    return {"code": 0, "step": 3, "datetime": get_datetime(file_dir, "picture")}
