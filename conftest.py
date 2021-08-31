import logging


logging.basicConfig(filename='test.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s - [%(name)s] - [%(levelname)4s] - %(message)s - (%(filename)s:%(lineno)s)')
                    # format='%(levelname)s: %(message)s')
logging.getLogger("urllib3").setLevel(logging.DEBUG)