from uls_app import create_app
from uls_app.extensions import db

#Main method
if __name__ == '__main__':
    app2=create_app()
    db.create_all()
    app2.run(debug=True)