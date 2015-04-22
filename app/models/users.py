from app import db
from app.models import orders

def initUsers():
    '''
    Initializes the database with some users and return True if it's done, False if it was already done.
    @return True if users are successfully initialized, false otherwise.
    '''
    if(not(User.query.filter_by(pseudo="ferret").first() is None)):
        return False

    addUser("admin", "admin", True)

    return True

def addUser(pseudo, password, admin = False):
    '''
    Add a user to the database with its pseudo, password and admin status and return True if it's done.
    @type pseudo: string
    @type password: string
    @type admin: boolean
    @param admin: True if the user is an admin of the website, false otherwise
    @return True if the user is added, False otherwise
    '''
    if(not(User.query.filter_by(pseudo=pseudo).first() is None)):
        return False

    u = User(pseudo, password, admin)
    db.session.add(u)
    db.session.commit()

    return True

class UserOrder(db.Model):
    '''
    Represents the association between a user and an order with the user pseudo and the order id
    @author cachera - brabant
    '''
    __tablename__ = "user_order"
    user_pseudo = db.Column(db.String, db.ForeignKey("user.pseudo"), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), primary_key=True)

    def __init__(self, user_pseudo, order_id):
        self.user_pseudo = user_pseudo
        self.order_id = order_id

class User(db.Model):
    '''
    Represents a registered user in the database with its pseudo, as primary key, pass and orders and its admin status
    @author cachera - brabant
    '''
    __tablename__ = "user"
    pseudo = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64))
    admin = db.Column(db.Boolean, default=False)
    orders = db.relationship("UserOrder", backref="user", lazy="dynamic")

    def __init__(self, pseudo, password, admin):
        self.pseudo = pseudo
        self.password = password
        self.admin = admin

    def authenticate(self, password):
        '''
        Authenticate the user if the password match with its password
        @type password: string
        @return True if the user is logged, false otherwise
        '''
        return self.password == password

    def isAdmin(self):
        return self.admin

    def addOrder(self, orderId):
        '''
        Links an order to this user
        @type orderId: number
        @param orderId: the order to link to the user
        '''
        userOrder = UserOrder(self.pseudo, orderId)
        db.session.add(userOrder)
        db.session.commit()

    def __repr__(self):
        '''
        Represents the order as a string
        '''
        return "{}".format(self.pseudo)
