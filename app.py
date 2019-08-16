from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os

app = Flask(__name__)

_basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(_basedir, 'grafica.db')

db = SQLAlchemy(app)

##### MODELS ########
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    notes = db.Column(db.Text)
    data_pedido = db.Column(db.DateTime, server_default=func.now())
    data_prazo = db.Column(db.Date)
    id_status = db.Column(db.Integer, db.ForeignKey('status_pedido.id'))
    quantidade = db.Column(db.Integer)
    price = db.Column(db.Float)


class StatusPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
#######################

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html'), 200


@app.route('/')
def index():
    pedidos_ativos = Pedido.query.filter_by(id_status=1).all()
    pedidos_concluidos = Pedido.query.filter_by(id_status=2).all()
    return render_template('index.html', pedidos_ativos=pedidos_ativos, pedidos_concluidos=pedidos_concluidos)


@app.route('/add', methods=['POST'])
def add():
    pedido = Pedido(description=request.form['pedidos'], id_status=1, quantidade=2,price=60)
    db.session.add(pedido)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):
    pedido = Pedido.query.filter_by(id=int(id)).first()
    pedido.id_status = 2
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete/<id>")
def delete(id):
    pedido = Pedido.query.filter_by(id=int(id)).first()
    db.session.delete(pedido)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/index2")
def index2():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)