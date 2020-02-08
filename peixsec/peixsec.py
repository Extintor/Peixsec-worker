import subprocess
import logging
import datetime
import os

import pika
from pymongo import MongoClient


logging.basicConfig(filename='peixsec.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


def _get_db_credentials() -> (str, str):
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    return user, password


def _write_stdin(process: subprocess.Popen, command: str):
    process.stdin.write('{}\n'.format(command))
    process.stdin.flush()


def _get_best_move(process: subprocess.Popen) -> str:
    for line in process.stdout:
        if 'bestmove' in line:
            return line.split(" ")[1]


def process_position(fen_position: str, stockfish: subprocess.Popen, positions) -> None:
    logger.info("Received {}".format(fen_position))
    _write_stdin(stockfish, 'position fen {}'.format(fen_position))
    _write_stdin(stockfish, 'go movetime 10000')
    best_move = _get_best_move(stockfish)
    logger.info("Output received from stockfish {}".format(best_move))
    position_object = {"fen": fen_position,
                       "best_move": best_move,
                       "tags": ["position"],
                       "date": datetime.datetime.utcnow()}
    logger.info("Inserted {}".format(positions.insert_one(position_object)))


def main() -> None:
    logger.info([os.environ.get('DB_USER')])
    logger.info([os.environ.get('DB_PASSWORD')])

    stockfish = subprocess.Popen(
        'stockfish', universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1,
    )
    _write_stdin(stockfish, 'uci')
    logger.info("Stockfish initialized successfully.")

    # TODO pass database domain name as an env variable
    db_user, db_password = _get_db_credentials()
    client = MongoClient('database',
                         username=db_user,
                         password=db_password,
                         authSource='training',
                         authMechanism='SCRAM-SHA-256')
    db = client.training
    positions = db.positions
    logger.info("MongoDB initialized successfully.")

    # TODO pass rabbitmq domain name as an env variable
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-service'))
    channel = connection.channel()
    # TODO pass queue name as an env variable
    channel.queue_declare(queue='position_request', durable=True, exclusive=False, auto_delete=False)
    channel.basic_consume(
        queue='position_request',
        auto_ack=True,
        on_message_callback=lambda ch, method, properties, body: process_position(body.decode('utf-8'),
                                                                                  stockfish,
                                                                                  positions,
                                                                                  )
    )
    channel.start_consuming()


if __name__ == "__main__":
    main()
