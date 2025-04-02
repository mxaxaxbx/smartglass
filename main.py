from flask import request
from dotenv import load_dotenv

load_dotenv()

from app import app, db

from signal import signal, SIGINT, SIGTERM
from os import getenv
import logging as log

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.before_request
def validate_options_request():
  if request.method == 'OPTIONS':
    return '', 204

def main():
  def handle_exit(signum, frame):
    try:
      db.session.close()
      db.engine.dispose()
    except Exception as e:
      log.error(f'Error closing database connection: {e}')
      exit(1)

    log.info('Exiting...')
    exit(0)

  signal(SIGINT, handle_exit)
  signal(SIGTERM, handle_exit)

  debug = True if getenv('FLASK_DEBUG') == '1' else False

  app.run(debug=debug, port=8080)

if __name__ == '__main__':
  main()
