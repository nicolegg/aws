# services/users/project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
# from project import db
# from project.api.models import User
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    """Pruebas para el servicio de usuarios."""

    def test_users(self):
        """Asegúrese de que la ruta /ping se comporte correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(
                    {'username': 'nicolegg',
                     'email': 'estefannygarcia@upeu.edu.pe'}
                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                'estefannygarcia@upeu.edu.pe was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Asegurese de que se produzca un error
si el objeto JSON esta vacio."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Asegurese de que se produzca un error
        si el objeto JSON no tiene una clave de nombre de usuario. """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'estefannygarcia@upeu.edu.pe'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """ Asegurese de que se arroje un error
        si el correo electronico ya existe."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps(
                    {'username': 'nicolegg',
                     'email': 'estefannygarcia@upeu.edu.pe'}
                ),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps(
                    {'username': 'nicolegg',
                     'email': 'estefannygarcia@upeu.edu.pe'}
                ),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('nicolegg', 'estefannygarcia@upeu.edu.pe')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('nicolegg', data['data']['username'])
            self.assertIn('estefannygarcia@upeu.edu.pe', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Asegurese de que se produzca un error si no se proporciona un id."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Asegurese de que se produzca un error si el id no existe."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Asegurese de que todos los usuarios se comporten correctamente."""
        add_user('nicolegg', 'estefannygarcia@upeu.edu.pe')
        add_user('Noluccia', 'luciariquelme51@gmail.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('nicolegg', data['data']['users'][0]['username'])
            self.assertIn('estefannygarcia@upeu.edu.pe', data[
                'data']['users'][0]['email'])
            self.assertIn('Noluccia', data['data']['users'][1]['username'])
            self.assertIn(
                'luciariquelme51@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Asegurando que la ruta principal se comporte
        correctamente cuando no se
        hayan agregado usuarios a la base de datos."""

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """Asegurando que la ruta principal se
        comporte correctamente cuando se
        hayan agregado usuarios a la base de datos."""
        add_user('nicolegg', 'estefannygarcia@upeu.edu.pe')
        add_user('Noluccia', 'luciariquelme51@gmail.com')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'nicolegg', response.data)
            self.assertIn(b'Noluccia', response.data)

    def test_main_add_user(self):
        """
        Asegurando que se pueda agregar un nuevo usuario
        a la base de datos mediante
        una solicitud POST.
        """
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    username='normariquelme',
                    email='normariquelme@upeu.edu.pe'), follow_redirects=True
                )
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
