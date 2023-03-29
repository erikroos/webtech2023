from elections import db, app, Party

with app.app_context():
    db.create_all()
    db.session.add_all([Party('Links Water'), Party('Forumwater'), Party('Boerenwater')])
    db.session.commit()