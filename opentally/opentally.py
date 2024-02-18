from flask import Flask, render_template
from threading import Thread
from queue import Queue
from atem_sync_worker.atem_sync_worker import ATEMSyncHandler
import logging
import pathlib

app = Flask(__name__)

@app.route('/')
async def root():
    return render_template('index.html')



if __name__ == '__main__':
    # create the log file path if it does not already exist
    log_file_path = (pathlib.Path(__file__).parent.absolute() / pathlib.Path('logs/opentally.log'))
    log_file_path.touch(exist_ok=True)

    # create logger
    logging.basicConfig(filemode='w', filename=log_file_path, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug('hello world')

    queue = Queue()
    atem_sync_handler = ATEMSyncHandler(logger, queue)

    # initailize and start async handler on a new thread
    sync_worker_thread = Thread(target=atem_sync_handler.start_worker, daemon=True)
    sync_worker_thread.start()

    #start flask on a separate thread as well
    flask_thread = Thread(target=app.run, daemon=True)
    flask_thread.start()

    # wait for threads to end before exiting
    flask_thread.join()
    sync_worker_thread.join()