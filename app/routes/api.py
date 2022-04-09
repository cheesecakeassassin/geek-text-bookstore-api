from flask import Blueprint
from app.models import User
from app.db import get_db
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    
  return ''