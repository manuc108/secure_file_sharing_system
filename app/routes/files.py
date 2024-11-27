import os
from flask import Blueprint, request, jsonify, send_file, current_app
from app.services.files import upload_file, list_files, generate_download_link, download_file
from app.utils.decorators import token_required

bp = Blueprint('files', __name__)

@bp.route('/upload', methods=['POST'])
@token_required
def upload(current_user):
    # Handle file upload
    if current_user['role'] != 'ops':
        return jsonify(message='Permission denied. You are not allowed to upload files.'), 403

    file = request.files.get('file')
    if not file:
        return jsonify(message="No file provided."), 400

    result, status_code = upload_file(file, current_user)
    return jsonify(result), status_code

@bp.route('/files', methods=['GET'])
@token_required
def list_all_files(current_user):
    # List all available files
    result = list_files()
    return jsonify(result), 200

@bp.route('/download/<file_id>', methods=['GET'])
@token_required
def download(current_user, file_id):
    # Generate download link for a file
    result, status_code = generate_download_link(file_id, current_user)
    return jsonify(result), status_code

@bp.route('/secure-download/<token>', methods=['GET'])
@token_required
def secure_download(current_user, token):
    # Securely download a file using a token
    result, status_code = download_file(token, current_user)

    # If the result contains a message, it means there was an error (e.g., invalid token)
    if result.get('message'):
        return jsonify(result), status_code

    file_path = os.path.join(current_app.config['ROOT_DIR'], result['path'])
    return send_file(file_path, as_attachment=True, download_name=result['filename'])
