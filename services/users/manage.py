import sys
import unittest
import coverage

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

from flask.cli import FlaskGroup

from project import create_app, db  # new
from project.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

# new
@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """Ejecuta las pruebas sin cobertura de código"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)

@cli.command('seed_db')
def seed_db():
    """Sembrar la base de datos"""
    db.session.add(User(               # nuevo
        username='abel.huanca',
        email='abel.huanca@upeu.edu.pe',
        password='greaterthaneight')
    )
    db.session.add(User(               # nuevo
        username='fredy',
        email='abelthf@gmail.com',
        password='greaterthaneight')
    )
    db.session.commit()

@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con cobertura."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)

if __name__ == '__main__':
    cli()
