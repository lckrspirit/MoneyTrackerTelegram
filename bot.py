#!/bin/python3

import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('TEST'))
