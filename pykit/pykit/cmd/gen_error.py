import logging
import os
from pykit.protoc_gen_error.main import gen_error


pwd = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=os.path.join(pwd, 'proto-python-error.log'),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


logger = logging.getLogger('proto-python-error')
logging.info("Running Urban Planning")


def main():
    gen_error()


if __name__ == '__main__':
    main()
