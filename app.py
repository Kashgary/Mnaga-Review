import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Managa, Review

MANGA_PER_PAGE = 10

def pagination(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * MANGA_PER_PAGE
    end = start + MANGA_PER_PAGE

    mangas = [manga.format() for manga in selection]
    pagination = mangas[start:end]

    return pagination

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  @app.after_request
  def after_request(response):
      response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type,Authorization,true')
      response.headers.add(
          'Access-Control-Allow-Methods',
          'GET,PUT,POST,DELETE,OPTIONS')
      return response
    
  @app.route('/manga_list')
  def get_categories():
      selection = Managa.query.order_by(Managa.title).all()
      paginated_mangas = pagination(request, selection)
      
      if len(paginated_mangas) == 0:
          abort(404)
      return jsonify({
          'success': True,
          'mangas': paginated_mangas,
          'total_mangas': len(selection),
      })      
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)