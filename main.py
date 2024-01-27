from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 
import psycopg2 



app = Flask(__name__)
app.config['SECRET_KEY'] = 'bananajezuta'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fluoclip:464130@100.124.214.138:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# Create A Model For Table
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(1000), nullable = False)
    lastName = db.Column(db.String(1000), nullable = False)
    email = db.Column(db.String(6000), nullable = False)


@app.route("/")
def home():
    return "Home"


@app.route('/add-users', methods=['POST'])
def add_user():
    try:
        data = request.json
        new_user = User(firstName=data['firstName'],lastName=data['lastName'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        response = {
            'message': 'User added',
            'user_id': new_user.id
        }
        return jsonify(response), 201

    except Exception as e:
        error_message = f'Došlo je do pogreške: {str(e)}'
        return jsonify({'error': error_message}), 500


@app.route('/delete-users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Pronalaženje korisnika po ID-u
        user_to_delete = User.query.get(user_id)

        if user_to_delete:
            # Brisanje korisnika iz baze podataka
            db.session.delete(user_to_delete)
            db.session.commit()

            # Odgovor s potvrdom
            response = {
                'message': f'Korisnik s ID-om {user_id} uspješno obrisan!'
            }
            return jsonify(response), 200
        else:
            # Ako korisnik nije pronađen
            return jsonify({'error': f'Korisnik s ID-om {user_id} nije pronađen.'}), 404

    except Exception as e:
        # Ako dođe do pogreške
        error_message = f'Došlo je do pogreške: {str(e)}'
        return jsonify({'error': error_message}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # <--- create db object.
    app.run(debug=True)