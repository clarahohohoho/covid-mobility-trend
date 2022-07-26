from flask import Blueprint
from controllers.fileController import download_file, upload_file, lock_filter_data

file_bp = Blueprint("file_bp", __name__)

file_bp.route("/download", methods=["GET"])(download_file)
file_bp.route("/upload", methods=["GET", "POST"])(upload_file)
file_bp.route("/lock-data", methods=["GET", "POST"])(lock_filter_data)