from website.app import db, models
from random import randint

# u = models.User(user_name='NOTFEDOS', email='NOTFEDOS@FEDOS.FEDOS', password='PESOS')
# db.session.add(u)
# db.session.commit()
#
#
# u = models.User(user_name='FEDOS', email='FEDOS@FEDOS.FEDOS', password='PESOS')
# db.session.add(u)
# db.session.commit()
#
# users = models.User.query.all()
# print(users)
#
# for user in users:
#     print(user.id, user.user_name, user.email, user.password)
#
# a = ['Pineapple', 'Mango', 'Coconut', 'Menthol', 'Banana']
# b = ['TPA', 'TPA', 'TPA', 'TPA', 'TPA']
# for i in range(len(a)):
#     f = models.Flavor(flavor_name=a[i], producer_name=b[i])
#     db.session.add(f)
#     db.session.commit()
#
# for i in range(1,6):
#     ufi = models.UserFlavorInventory(user_id=2, flavor_id=i, amount=randint(5,15))
#     db.session.add(ufi)
#     db.session.commit()

# ufi = models.UserFlavorInventory(user_id=2, flavor_id=1, amount=randint(5,15))
# db.session.add(ufi)
# db.session.commit()


users = models.User.query.all()
for u in users:
    print(u)
    db.session.delete(u)
