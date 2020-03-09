from models import People, Users

# Realiza consulta na tabela pessoas
def query_people():
    person = People.query.all()
    print(person)
    '''
    person = People.query.filter_by(name='Kaneki')
    for i in person:
        print(i.age)
    
    person = People.query.filter_by(name='Kaneki').first()
    print(person.age)
    '''
    
# Insere dados na tabela pessoa
def insert_person(name,age):
    person = People(name=name,age=age)
    person.save()
    print(person)

# Altera dados na tabela pessoa
def change_person(name,new_name,age):
    person = People.query.filter_by(name=name).first()
    person.age = 19
    person.name = new_name
    person.save()

# Exclui dados na tabela pessoa
def delete_person(name):
    person = People.query.filter_by(name=name).first()
    person.delete()

def insert_user(login, password):
    user = Users(login=login, password=password)
    user.save()

def check_all_users():
    users = Users.query.all()
    print(users)

if __name__ == '__main__':
    #insert_person('Minato',32)
    #query_people()
    #change_person('Naruto','Itachi','18')
    #query_people()
    #delete_person('Inawami')
    #insert_user('Kaneki','1234')
    insert_user('Monster','4862')
    check_all_users()
    #print(Users.query.all())
    
    
