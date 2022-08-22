import logging
import os
from pykit.protoc_gen_http.main import gen_http


pwd = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=os.path.join(pwd, 'proto-python-http.log'),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


logger = logging.getLogger('proto-python-http')
logging.info("Running Urban Planning")


def main():
    gen_http()


if __name__ == '__main__':
    main()
