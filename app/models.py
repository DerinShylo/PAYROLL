# app/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ============================================================
# USER MODEL
# ============================================================
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    # Role flags
    is_admin = db.Column(db.Boolean, default=False)
    is_accounts = db.Column(db.Boolean, default=False)
    is_hr = db.Column(db.Boolean, default=False)

    # -------------------------
    # Authentication helpers
    # -------------------------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ============================================================
# ADMIN CREATION HELPER
# ============================================================
def ensure_admin_exists(app):
    """Ensure default system users exist without duplicate insert errors."""
    with app.app_context():
        db.create_all()

        # --- Admin User ---
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            print("✅ Created admin (username='admin', password='admin123')")

        # --- Accounts User ---
        accounts = User.query.filter_by(username='accounts').first()
        if not accounts:
            accounts = User(username='accounts', is_accounts=True)
            accounts.set_password('accounts123')
            db.session.add(accounts)
            print("✅ Created accounts (username='accounts', password='accounts123')")

        # --- HR User ---
        hr = User.query.filter_by(username='user1').first()
        if not hr:
            hr = User(username='user1', is_hr=True)
            hr.set_password('user123')
            db.session.add(hr)
            print("✅ Created HR user (username='user1', password='user123')")

        # Commit all changes safely
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Skipped duplicate user creation: {e}")


# ============================================================
# STAFF MODEL
# ============================================================
class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False, default='Teaching')
    department = db.Column(db.String(80), nullable=False)
    designation = db.Column(db.String(80), nullable=False)

    base_salary = db.Column(db.Float, nullable=False)
    allowances = db.Column(db.Float, default=0)
    deductions = db.Column(db.Float, default=0)

    date_joined = db.Column(db.Date, nullable=False)
    bank_account = db.Column(db.String(30), nullable=False)
    aadhar = db.Column(db.String(12), nullable=False)

    pf_number = db.Column(db.String(30))
    esi_number = db.Column(db.String(30))
    active = db.Column(db.Boolean, default=True)

    # Relationship
    salary_records = db.relationship('SalaryRecord', backref='staff_ref', lazy=True)

    def __repr__(self):
        return f"<Staff {self.staff_id} - {self.name}>"


# ============================================================
# SALARY RECORD MODEL
# ============================================================
class SalaryRecord(db.Model):
    __tablename__ = 'salary_records'

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)

    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    gross_salary = db.Column(db.Float, nullable=False)

    lop_days = db.Column(db.Float, default=0)
    lop_amount = db.Column(db.Float, default=0)
    epf = db.Column(db.Float, default=0)
    esi = db.Column(db.Float, default=0)

    # Individual deductions
    it = db.Column(db.Float, default=0)
    loan = db.Column(db.Float, default=0)
    advance = db.Column(db.Float, default=0)
    uniform = db.Column(db.Float, default=0)
    cd = db.Column(db.Float, default=0)
    hostel = db.Column(db.Float, default=0)
    misc = db.Column(db.Float, default=0)

    # Computed fields
    total_deductions = db.Column(db.Float, default=0)
    total_reimbursements = db.Column(db.Float, default=0)
    net_salary = db.Column(db.Float, default=0)

    date_created = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<SalaryRecord StaffID={self.staff_id} {self.month}/{self.year}>"


# ============================================================
# INCREMENT HISTORY MODEL
# ============================================================
class IncrementHistory(db.Model):
    __tablename__ = 'increment_history'

    id = db.Column(db.Integer, primary_key=True)
    increment_type = db.Column(db.String(50))
    target = db.Column(db.String(100))
    mode = db.Column(db.String(50))
    value = db.Column(db.Float)
    effective_month = db.Column(db.String(20))
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Increment {self.increment_type} on {self.target}>"


# ============================================================
# PROFESSIONAL TAX MODEL
# ============================================================
class ProfessionalTax(db.Model):
    __tablename__ = 'professional_tax'

    id = db.Column(db.Integer, primary_key=True)
    range_from = db.Column(db.Float, nullable=False)
    range_to = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Tax {self.range_from}-{self.range_to}: ₹{self.tax_amount}>"
