import platform
from website.app import app

if platform.system() == 'Windows':
    app.run()
else:
    app.run()
