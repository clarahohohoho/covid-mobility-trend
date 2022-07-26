from flask import Blueprint
from controllers.filterController import (
    fetch_all_data,
    fetch_filter_values,
    fetch_filtered,
    filter_traffic_number,
)

filter_bp = Blueprint("filter_bp", __name__)

filter_bp.route("/all", methods=["GET"])(fetch_all_data)
filter_bp.route("/filter", methods=["GET"])(fetch_filter_values)
filter_bp.route("/filter-values", methods=["GET", "POST"])(fetch_filtered)
filter_bp.route("/filter-traffic-number", methods=["GET", "POST"])(filter_traffic_number)
