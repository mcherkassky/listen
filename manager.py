from flask.ext.script import Manager, Shell

from youtube import app
from youtube import models

manager = Manager(app)

def _make_context():
	return {'app': app, 'models': models}

@manager.command
def hello():
	print "hello"

if __name__ == "__main__":
	manager.add_command('shell', Shell(make_context=_make_context))
	manager.run()




