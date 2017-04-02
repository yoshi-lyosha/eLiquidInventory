from website.app import db, models
# u = models.User(user_name='FEDOS', email='FEDOS@FEDOS.FEDOS', password='PESOS')
# db.session.add(u)
# db.session.commit()

users = models.User.query.all()
print(users)

for user in users:
    print(user.id, user.user_name, user.email, user.password)
