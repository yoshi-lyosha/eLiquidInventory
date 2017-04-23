from website.app import db, models
# from website.app.users import constants as USER
from website.app.eliquids import constants as ELIQUID


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


def flavorings_gen():
    print('-----------------')
    a = ['Pineapple', 'Mango', 'Coconut', 'Menthol', 'Banana']
    b = ['TPA', 'TPA', 'TPA', 'TPA', 'TPA']
    for i in range(len(a)):
        f = models.Flavoring(flavoring_name=a[i], producer_name=b[i])
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


def print_all_flavorings():
    print('-----------------')
    print('List of flavorings:')
    print("{:12} {:14} {:13}".format('flavoring_id', 'flavoring_name', 'producer_name'))
    items = models.Flavoring.query.all()
    for item in items:
        print("{:12} {:14} {:13}".format(str(item.id), item.flavoring_name, item.producer_name))


def print_all_nicotine():
    print('-----------------')
    print('List of Nicotine:')
    print("{:11} {:13} {:13}".format('nicotine_id', 'producer_name', 'concentration'))
    items = models.Nicotine.query.all()
    for item in items:
        print("{:11} {:13} {:13}".format(str(item.id), item.producer_name, str(item.concentration)))


def delete_user(user):
    try:
        print('-----------------')
        print('Deleting user "{}"'.format(user.user_name))
        db.session.delete(user)
        db.session.commit()
        print('Object deleted')
    except Exception as e:
        print('Can\'t delete this user')
        print(e)


def delete_flavoring(flavoring):
    try:
        print('-----------------')
        print('Deleting flavoring "{}"'.format(flavoring.flavoring_name))
        db.session.delete(flavoring)
        db.session.commit()
        print('Object deleted')
    except Exception as e:
        print('Can\'t delete this item')
        print(e)


def delete_nicotine(nicotine):
    try:
        print('-----------------')
        print('Deleting nicotine "{}"'.format(nicotine.nicotine_name))
        db.session.delete(nicotine)
        db.session.commit()
        print('Object deleted')
    except Exception as e:
        print('Can\'t delete this item')
        print(e)


def add_flavoring_to_user(user, flavoring, amount):
    try:
        print('-----------------')
        print('Adding flavoring {} in {} inventory'.format(flavoring.flavoring_name, user.user_name))
        inv = models.UsersFlavoringInventory(user=user, flavoring=flavoring, amount=amount)
        db.session.add(inv)
        db.session.commit()
    except Exception as e:
        print('Can\'t add this flavoring to this user')
        print(e)


def add_nicotine_to_user(user, nicotine, amount):
    try:
        print('-----------------')
        print('Adding nicotine {}:{} in {} inventory'.format(nicotine.producer_name,
                                                             nicotine.concentration, user.user_name))
        inv = models.UsersNicotineInventory(user=user, nicotine=nicotine, amount=amount)
        db.session.add(inv)
        db.session.commit()
    except Exception as e:
        print('Can\'t add this nicotine to this user')
        print(e)


def print_user_inventory(user):
    try:
        print('-----------------')
        print('User {} flavorings inventory:'.format(user.user_name))
        flavorings_list = models.UsersFlavoringInventory.query.filter_by(user_id=user.id).all()
        for field in flavorings_list:
            print('{} ({}): {}'.format(models.Flavoring.query.filter_by(id=field.flavoring_id).first().flavoring_name,
                                       models.Flavoring.query.filter_by(id=field.flavoring_id).first().producer_name,
                                       field.amount))

        print('User {} nicotine inventory:'.format(user.user_name))
        nicotine_list = models.UsersNicotineInventory.query.filter_by(user_id=user.id).all()
        for field in nicotine_list:
            print('{} ({}mg/ml): {}'.format(models.Nicotine.query.filter_by(id=field.nicotine_id).first().producer_name,
                                            models.Nicotine.query.filter_by(id=field.nicotine_id).first().concentration,
                                            field.amount))

    except Exception as e:
        print('Can\'t do this')
        print(e)


def eliquid_create_by_user(user, eliquid_name, composition, public=True):
    # пытаемся добавить жижку
    try:
        print('-----------------')
        # проверяем статус
        if public:
            print('Creating public eLiquid:"{}", by user {}'.format(eliquid_name, user.user_name))
            e_liquid = models.ELiquid(eliquid_name=eliquid_name, user=user)
        elif not public:
            print('Creating private eLiquid:"{}", by user {}'.format(eliquid_name, user.user_name))
            e_liquid = models.ELiquid(eliquid_name=eliquid_name, user=user, status=ELIQUID.PRIVATE)
        else:
            raise Exception('wtf man')
        # пытаемся закоммитить
        try:
            db.session.add(e_liquid)
            db.session.commit()
        except Exception as e:
            print('Can\'t create eLiquid, stage 1, stopping')
            raise Exception(e)
        # пытаемся добавить аромки в состав
        try:
            for flavoring, quantity in composition.items():
                component = models.ELiquidComposition(e_liquid=e_liquid, flavoring=flavoring, quantity=quantity)
                db.session.add(component)
                print('Adding flavoring {} ({}): {}%'.format(flavoring.flavoring_name,
                                                             flavoring.producer_name, quantity))
            db.session.commit()
        except Exception as e:
            print('Can\'t create eLiquid, stage 2, stopping')
            db.session.delete(e_liquid)
            db.session.commit()
            print('rollback')
            raise Exception(e)
        print('eLiquid created')
    except Exception as e:
        print('Can\'t create eLiquid')
        print(e)
        db.session.rollback()
        print('rollback')


def print_all_public_eliquids():
    try:
        print('-----------------')
        print('List of public eLiquids:')
        print("{:10} {:15}".format('user_name', 'eLiquid_name'))
        eliquid_list = models.ELiquid.query.filter_by(status=ELIQUID.PUBLIC)
        for field in eliquid_list:
            print("{:10} {:15}".format(models.User.query.filter_by(id=field.user_id).first().user_name,
                                       field.eliquid_name))
    except Exception as e:
        print('Can\'t do this')
        print(e)


def print_eliquid_composition(eliquid):
    try:
        print('-----------------')
        print('Composition of eLiquid "{}":'.format(eliquid.eliquid_name))
        composition_list = models.ELiquidComposition.query.filter_by(eliquid_id=eliquid.id)
        print("{:15} {:15} {:15}".format('flavoring_name', 'producer', 'quantity'))
        for field in composition_list:
            print("{:15} {:15} {:15}".format(
                models.Flavoring.query.filter_by(id=field.flavoring_id).first().flavoring_name,
                models.Flavoring.query.filter_by(id=field.flavoring_id).first().producer_name,
                str(field.quantity) + ' %'))
    except Exception as e:
        print('Can\'t do this')
        print(e)


def print_all_public_eliquids_with_composition():
    try:
        print('-----------------')
        print('List of public eLiquids with its composition:')
        print("{:10} {:15}".format('user_name', 'eLiquid_name'))
        eliquid_list = models.ELiquid.query.filter_by(status=ELIQUID.PUBLIC)
        for el_field in eliquid_list:
            print("{:10} {:15}".format(models.User.query.filter_by(id=el_field.user_id).first().user_name,
                                       el_field.eliquid_name))
            eliquid = models.ELiquid.query.filter_by(eliquid_name=el_field.eliquid_name).first()
            composition_list = models.ELiquidComposition.query.filter_by(eliquid_id=eliquid.id)
            print('\t\t\t\\')
            print("\t\t\t{:15} {:15} {:15}".format('flavoring_name', 'producer', 'quantity'))
            for comp_field in composition_list:
                print("\t\t\t{:15} {:15} {:15}".format(
                    models.Flavoring.query.filter_by(id=comp_field.flavoring_id).first().flavoring_name,
                    models.Flavoring.query.filter_by(id=comp_field.flavoring_id).first().producer_name,
                    str(comp_field.quantity) + ' %'))
    except Exception as e:
        print('Can\'t do this')
        print(e)


def add_eliquid_to_user_favorite(user, eliquid):
    try:
        print('-----------------')
        print('Adding eLiquid "{}" to user {} favorites'.format(eliquid.eliquid_name, user.user_name))
        usr_fav = models.UsersFavouriteELiquids(user=user, e_liquid=eliquid)
        print('eLiquid "{}" added to user {} favorites'.format(eliquid.eliquid_name, user.user_name))
        db.session.add(usr_fav)
        db.session.commit()
    except Exception as e:
        print('Can\'t add eLiquid to favorites')
        print(e)
        db.session.rollback()
        print('rollback')


def print_users_favorits_eliquids(user):
    try:
        print('-----------------')
        print('User\'s {} favorite eliquids:'.format(user.user_name))

    except Exception as e:
        print('Can\'t add eLiquid to favorites')
        print(e)
        db.session.rollback()
        print('rollback')


def run_autotest_db_stage_1():
    """
    Тестирование функций добавления и вывода списков
    сущностей Юзер, Ароматизатор, Никотин
    """
    try:
        print('**********\nRunning autotest stage 1\n**********')
        user_gen()
        flavorings_gen()
        nicotine_gen()

        print_all_users()
        print_all_flavorings()
        print_all_nicotine()

    except Exception as e:
        print('Test_failed')
        print(e)
    finally:
        print('Test passed')


def run_autotest_db_stage_2():
    """
    Тестирование функций добавления в инвентарь
    Ароматизаторов и Никотина
    """
    try:
        print('**********\nRunning autotest stage 2\n**********')
        u1 = models.User.query.filter_by(user_name='FEDOS').first()
        u2 = models.User.query.filter_by(user_name='ALEXEY').first()
        f1 = models.Flavoring.query.filter_by(flavoring_name='Pineapple', producer_name='TPA').first()
        f2 = models.Flavoring.query.filter_by(flavoring_name='Menthol', producer_name='TPA').first()
        f3 = models.Flavoring.query.filter_by(flavoring_name='Mango', producer_name='TPA').first()
        f4 = models.Flavoring.query.filter_by(flavoring_name='Banana', producer_name='TPA').first()
        f5 = models.Flavoring.query.filter_by(flavoring_name='Coconut', producer_name='TPA').first()
        n1 = models.Nicotine.query.filter_by(producer_name='Xian', concentration='36').first()
        n2 = models.Nicotine.query.filter_by(producer_name='Merc', concentration='36').first()
        n3 = models.Nicotine.query.filter_by(producer_name='Alchemy', concentration='100').first()

        add_flavoring_to_user(u1, f1, 10)
        add_flavoring_to_user(u1, f2, 15)
        add_flavoring_to_user(u1, f3, 13)
        add_flavoring_to_user(u2, f1, 11)
        add_flavoring_to_user(u2, f3, 12)
        add_flavoring_to_user(u2, f4, 14)
        add_flavoring_to_user(u2, f5, 15)

        add_nicotine_to_user(u1, n1, 50)
        add_nicotine_to_user(u1, n2, 35)
        add_nicotine_to_user(u2, n3, 75)

        print_user_inventory(u1)
        print_user_inventory(u2)

    except Exception as e:
        print('Test_failed')
        print(e)
    finally:
        print('Test passed')


def run_autotest_db_stage_3():
    """
    Тестирование функций добавления новых
    публичных и приватных жижек
    """
    try:
        print('**********\nRunning autotest stage 3\n**********')
        u1 = models.User.query.filter_by(user_name='FEDOS').first()
        u2 = models.User.query.filter_by(user_name='ALEXEY').first()
        f1 = models.Flavoring.query.filter_by(flavoring_name='Pineapple', producer_name='TPA').first()
        f2 = models.Flavoring.query.filter_by(flavoring_name='Menthol', producer_name='TPA').first()
        f3 = models.Flavoring.query.filter_by(flavoring_name='Mango', producer_name='TPA').first()
        f4 = models.Flavoring.query.filter_by(flavoring_name='Banana', producer_name='TPA').first()
        f5 = models.Flavoring.query.filter_by(flavoring_name='Coconut', producer_name='TPA').first()

        eliquid_create_by_user(u2, 'top zhizhka, eboiii', {f1: 5, f2: 1, f3: 5, f4: 3, f5: 1}, public=False)
        eliquid_create_by_user(u1, 'top zhizhka, eboiii 2', {f1: 5, f2: 1, f3: 5, f4: 3, f5: 1})
        eliquid_create_by_user(u1, 'COLD STORM', {f2: 10, f3: 5})

        print_all_public_eliquids()
        print_all_public_eliquids_with_composition()

        el1 = models.ELiquid.query.filter_by(eliquid_name='top zhizhka, eboiii').first()
        print_eliquid_composition(el1)

    except Exception as e:
        print('Test_failed')
        print(e)
    finally:
        print('Test passed')


run_autotest_db_stage_1()
run_autotest_db_stage_2()
run_autotest_db_stage_3()
