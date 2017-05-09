import platform
from website.app import app

if platform.system() == 'Windows':
    app.run()
else:
    app.run(host='0.0.0.0', port=5000)
