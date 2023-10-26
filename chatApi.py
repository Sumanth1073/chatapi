from flask import Flask, render_template
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatAPI-DB.db'

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000), nullable=False)
    from_user = db.Column(db.String(200), nullable=False)
    to_user = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('documentation.html')

@app.route('/get_users', methods=['GET'])
def get_users():
    all_users = [user[0] for user in db.session.query(Message.from_user.distinct().label('viewer')).all()]
    all_users.extend([user[0] for user in db.session.query(Message.to_user.distinct().label('viewer')).all()])

    all_users = list(set(all_users))

    return jsonify(users=all_users), 200

@app.route('/get_messages', methods=['GET'])
def get_messages():
    all_logs = db.session.query(Message).all()

    return jsonify(logs=[log.to_dict() for log in all_logs]), 200

@app.route('/new_message', methods=['POST'])
def post_message():
    new_message_text = request.form.get('message')
    from_user = request.form.get('from_user')
    to_user = request.form.get('to_user')

    all_messages = db.session.query(Message).all()
    message_id = 0
    if len(all_messages) != 0:
        message_id = all_messages[-1].id + 1
        
    new_message = Message(id=message_id,
                  message=new_message_text,
                  from_user=from_user,
                  to_user=to_user)
    
    db.session.add(new_message)
    db.session.commit()

    return jsonify(response={"success": "Successfully added the new chat message."}), 200

@app.route('/update_message', methods=['PATCH'])
def update_message():
    id = request.form.get('id')
    edited_message_text = request.form.get('edited_message_text')

    old_message = db.session.query(Message).get(id)

    if old_message == None:
        return jsonify(error={"Not Found": "Invalid message Id."}), 400
    
    old_message.message = edited_message_text
    
    db.session.commit()

    return jsonify(response={"success": "Successfully updated the Message database."}), 200

@app.route('/delete_message', methods=['DELETE'])
def delete_message():
    id = request.form.get('id')

    message = db.session.query(Message).get(id)

    if message == None:
        return jsonify(error={"Not Found": "Invalid message Id."}), 404
    
    db.session.delete(message)

    db.session.commit()

    return jsonify(response={"success": "Successfully deleted message from the database."}), 200
        


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("3000"), debug=True)
    

