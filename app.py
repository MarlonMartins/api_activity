from flask import Flask, request
from flask_restful import Resource, Api
from models import People, Activities, Users
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

@auth.verify_password
def password_verification(login, password):
    print('Validating user')
    if not (login, password):
        return False
    return Users.query.filter_by(login=login,password=password).first()

class Person(Resource):
    @auth.login_required
    def get(self, name):
        person = People.query.filter_by(name=name).first()
        print(person)

        try:
            response = {
                'name': person.name,
                'age': person.age,
                'id': person.id,
            }
        except AttributeError:
            response = {'status': 'error', 'message': 'Person not found'}
        return response

    def put(self, name):
        person = People.query.filter_by(name=name).first()
        data = request.json
        try:
            if 'name' in data:
                person.name = data['name']
            if 'age' in data:
                person.age = data['age']
            person.save()

            response = {
                'id': person.id,
                'name': person.name,
                'age': person.age
            }

        except AttributeError:
            response = {'status': 'error', 'message': 'Person not found'}

        return response

    def delete(self, name):
        person = People.query.filter_by(name=name).first()

        try:
            message = '{} successfully deleted.'.format(person.name)
            person.delete()
            response = {'status': 'success', 'message': message}

        except AttributeError:
            response = {'status': 'error', 'message': 'Person not found'}

        return response


class People_list(Resource):
    @auth.login_required
    def get(self):
        people = People.query.all()
        response = [{'id': p.id, 'name': p.name, 'age': p.age} for p in people]
        return response

    def post(self):
        data = request.json
        person = People(name=data['name'], age=data['age'])
        person.save()

        response = {
            'id': person.id,
            'name': person.name,
            'age': person.age
        }
        return response


class Welcome(Resource):
    def get(self):
        return "Welcome to my first API!"


class Activities_list(Resource):
    def get(self):
        activities = Activities.query.all()
        response = [{'id': act.id, 'name': act.name,
                     'person': act.person.name} for act in activities]
        return response

    def post(self):
        data = request.json
        person = People.query.filter_by(name=data['person']).first()
        try:
            activitie = Activities(name=data['name'], person=person)
            activitie.save()
            response = {
                'id': activitie.id,
                'person': activitie.person.name,
                'name': activitie.name
            }
        except AttributeError:
            response = {'status': 'error', 'message': 'Person not found'}

        return response

api.add_resource(Welcome, '/')
api.add_resource(People_list, '/person/')
api.add_resource(Person, '/person/<string:name>/')
api.add_resource(Activities_list, '/activitie/')


if __name__ == '__main__':
    app.run(debug=True)
