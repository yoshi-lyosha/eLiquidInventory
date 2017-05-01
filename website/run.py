#!flask/bin/python
website_path = '/website/'
import sys
if not website_path in sys.path:
	sys.path.append(website_path)
from app import app
app.run(debug = False)
