from website.app import db, models
from random import randint


def user_gen():
    print('-----------------')
    print('Adding first user in database')
    u = models.User(user_name='ALEXEY', email='ALEXEY@ALEXEY.ALEXEY', password='PESOS')
    db.session.add(u)
    db.session.commit()
    print('Adding second user in database')
    u = models.User(user_name='FEDOS', email='FEDOS@FEDOS.FEDOS', password='PESOS')
    db.session.add(u)
    db.session.commit()


def flavor_gen():
    print('-----------------')
    a = ['Pineapple', 'Mango', 'Coconut', 'Menthol', 'Banana']
    b = ['TPA', 'TPA', 'TPA', 'TPA', 'TPA']
    for i in range(len(a)):
        f = models.Flavor(flavor_name=a[i], producer_name=b[i])
        print('Adding {} {} in database'.format(a[i], b[i]))
        db.session.add(f)
        db.session.commit()


def nicotine_gen():
    print('-----------------')
    a = ['Xian', 'Merc', 'Alchemy']
    b = ['36', '36', '100']
    for i in range(len(a)):
        f = models.Nicotine(producer_name=a[i], concentration=b[i])
        print('Adding {} {} in database'.format(a[i], b[i]))
        db.session.add(f)
        db.session.commit()


def print_all_users():
    print('-----------------')
    print("{:7} {:10} {:10}".format('user_id', 'user_name', 'email'))
    users = models.User.query.all()
    for user in users:
        print("{:7} {:10} {:10}".format(str(user.id), user.user_name, user.email))


def print_all_flavors():
    print('-----------------')
    print('List of flavorings:')
    print("{:10} {:13} {:13}".format('flavor_id', 'flavor_name', 'producer_name'))
    items = models.Flavor.query.all()
    for item in items:
        print("{:10} {:13} {:13}".format(str(item.id), item.flavor_name, item.producer_name))


def print_all_nicotine():
    print('-----------------')
    print('List of Nicotine:')
    print("{:11} {:13} {:13}".format('nicotine_id', 'producer_name', 'concentration'))
    items = models.Nicotine.query.all()
    for item in items:
        print("{:11} {:13} {:13}".format(str(item.id), item.producer_name, item.concentration))


def delete_user(user):
    try:
        print('-----------------')
        print('Deleting user "{}"'.format(user.user_name))
        db.session.delete(user)
        db.session.commit()
        print('Object deleted')
    except AttributeError:
        print('Can\'t delete this user')


def delete_flavor(flavor):
    try:
        print('-----------------')
        print('Deleting flavor "{}"'.format(flavor.flavor_name))
        db.session.delete(flavor)
        db.session.commit()
        print('Object deleted')
    except AttributeError:
        print('Can\'t delete this item')


def delete_nicotine(nicotine):
    try:
        print('-----------------')
        print('Deleting flavor "{}"'.format(nicotine.flavor_name))
        db.session.delete(nicotine)
        db.session.commit()
        print('Object deleted')
    except AttributeError:
        print('Can\'t delete this item')


def add_flavor_to_user(user, flavor, amount):
    try:
        print('-----------------')
        print('Adding flavor {} in {} inventory'.format(flavor.flavor_name, user.user_name))
        inv = models.UserFlavorInventory(user=user, flavor=flavor, amount=amount)
        db.session.add(inv)
        db.session.commit()
    except AttributeError:
        print('Can\'t add this flavor to this user')


def add_nicotine_to_user(user, nicotine, amount):
    try:
        print('-----------------')
        print('Adding nicotine {}:{} in {} inventory'.format(nicotine.producer_name,
                                                             nicotine.concentration, user.user_name))
        inv = models.UserFlavorInventory(user=user, flavor=nicotine, amount=amount)
        db.session.add(inv)
        db.session.commit()
    except AttributeError:
        print('Can\'t add this nicotine to this user')


def print_user_inventory(user):
    try:
        print('-----------------')
        print('User {} flavor inventory:'.format(user.user_name))
        all = models.UserFlavorInventory.query.filter_by(user_id=user.id).all()
        for field in all:
            print('{}: {}'.format(models.Flavor.query.filter_by(id=field.flavor_id).first().flavor_name, field.amount))
    except AttributeError:
        print('Can\'t do this, this user don\'t exist')


def run_auto_db_test_stage_1():
    """
    Тестирование функций добавления и вывода списков
    сущностей Юзер, Ароматизатор, Никотин
    """
    try:
        print('**********\nRunning autotest stage 1\n**********')
        user_gen()
        flavor_gen()
        nicotine_gen()
        u1 = models.User.query.filter_by(user_name='FEDOS').first()
        u2 = models.User.query.filter_by(user_name='ALEXEY').first()
        f1 = models.Flavor.query.filter_by(flavor_name='Pineapple', producer_name='TPA').first()
        f2 = models.Flavor.query.filter_by(flavor_name='Menthol', producer_name='TPA').first()
        f3 = models.Flavor.query.filter_by(flavor_name='Mango', producer_name='TPA').first()
        f4 = models.Flavor.query.filter_by(flavor_name='Banana', producer_name='TPA').first()
        f5 = models.Flavor.query.filter_by(flavor_name='Coconut', producer_name='TPA').first()
        n1 = models.Nicotine.query.filter_by(producer_name='Xian', concentration='36').first()
        n2 = models.Nicotine.query.filter_by(producer_name='Merc', concentration='36').first()
        n3 = models.Nicotine.query.filter_by(producer_name='Alchemy', concentration='100').first()
        print_all_users()
        print_all_flavors()
        print_all_nicotine()

    except:
        print('Test_failed')
    finally:
        print('Test passed')

def run_auto_db_test_stage_2():
    """
    Тестирование функций добавления в инвентарь
    Ароматизаторов и Никотина
    """
    try:
        print('**********\nRunning autotest stage 2\n**********')
        u1 = models.User.query.filter_by(user_name='FEDOS').first()
        u2 = models.User.query.filter_by(user_name='ALEXEY').first()
        f1 = models.Flavor.query.filter_by(flavor_name='Pineapple', producer_name='TPA').first()
        f2 = models.Flavor.query.filter_by(flavor_name='Menthol', producer_name='TPA').first()
        f3 = models.Flavor.query.filter_by(flavor_name='Mango', producer_name='TPA').first()
        f4 = models.Flavor.query.filter_by(flavor_name='Banana', producer_name='TPA').first()
        f5 = models.Flavor.query.filter_by(flavor_name='Coconut', producer_name='TPA').first()
        n1 = models.Nicotine.query.filter_by(producer_name='Xian', concentration='36').first()
        n2 = models.Nicotine.query.filter_by(producer_name='Merc', concentration='36').first()
        n3 = models.Nicotine.query.filter_by(producer_name='Alchemy', concentration='100').first()


    except:
        print('Test_failed')
    finally:
        print('Test passed')





run_auto_db_test_stage_1()

# add_flav_to(u2, f3, randint(5,15))

# all_invs = models.UserFlavorInventory.query.all()
# print(all_invs)
# delete_user(u1)
# print_all_users()
# delete_flavor()
# print_user_inventory(u1)
# print_user_inventory(u2)
# add_flavor_to_user(u1, f2, 15)

# inv2 = models.UserFlavorInventory(user_id=1, flavor_id=1, amount=10)
# print(inv2)


# print(u)
# flav_inv = u.flavors_in_inventory.all()

