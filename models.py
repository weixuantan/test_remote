import datetime

from extension import db

class Department(db.Model):
    __tablename__ = 'tb_department'
    id = db.Column(db.Integer, autoincrement=True)
    d_number = db.Column(db.String(225),nullable=False)
    d_name = db.Column(db.String(225),primary_key=True)

    @staticmethod
    def init_db():
        rets = [
            (1, '001','信息'),
            (2, '002', '人力')
        ]
        for ret in rets:
            department = Department()
            department.id = ret[0]
            department.d_number = ret[1]
            department.d_name = ret[2]
            db.session.add(department)
        db.session.commit()

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    ee_accounts = db.Column(db.String(225),nullable=False)
    ee_password = db.Column(db.String(225), nullable=False)
    ee_role = db.Column(db.String(225), nullable=False)
    ee_name= db.Column(db.String(225), nullable=False)
    ee_department = db.Column(db.String(225),db.ForeignKey('tb_department.d_name'))

    @staticmethod
    def init_db():
        rets = [
            (1,'20190734','123456','管理员','张三','信息'),
            (2, '20200056', '123456', '负责人', '李四', '人力'),
            (3,'20180653','123456','基础员工','王五','人力')
        ]
        for ret in rets:
            employee = Employee()
            employee.id = ret[0]
            employee.ee_accounts = ret[1]
            employee.ee_password = ret[2]
            employee.ee_role = ret[3]
            employee.ee_name = ret[4]
            employee.ee_department = ret[5]
            db.session.add(employee)
        db.session.commit()

class Welfare(db.Model):
    __tablename__ = 'welfare'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('employee.id'),nullable=True)
    approver_id = db.Column(db.Integer,db.ForeignKey('employee.id'),nullable=True)
    approve_status = db.Column(db.String(225),default='未审批')
    wf_name = db.Column(db.String(225),nullable=False)
    wf_desc = db.Column(db.Text,nullable=False)
    wf_amount = db.Column(db.Integer,nullable=False)
    wf_time = db.Column(db.DateTime)
    user = db.relationship('Employee',foreign_keys=[user_id])
    approver = db.relationship('Employee', foreign_keys=[approver_id])

    @staticmethod
    def init_db():
        rets = [
            (1, '3', '2', '已审核', '交通补贴', '交通补贴测试描述',2000,datetime.datetime.now()),
            (2, '3', '2', '已审核', '人才补贴', '人才补贴测试描述',30000,datetime.datetime.now())
        ]
        for ret in rets:
            welfare = Welfare()
            welfare.id = ret[0]
            welfare.user_id = ret[1]
            welfare.approver_id = ret[2]
            welfare.approve_status = ret[3]
            welfare.wf_name = ret[4]
            welfare.wf_desc = ret[5]
            welfare.wf_amount = ret[6]
            db.session.add(welfare)
        db.session.commit()

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('employee.id'),nullable=True)
    approver_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    approve_status = db.Column(db.String(225))
    work_type = db.Column(db.String(225))
    time_start =db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    time_sum = db.Column(db.Float)
    reason = db.Column(db.Text)
    user = db.relationship('Employee',foreign_keys=[user_id])
    approver = db.relationship('Employee', foreign_keys=[approver_id])

class WelfareFiles(db.Model):
    __tablename__ = 'WelfareFiles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wf_id =db.Column(db.Integer,db.ForeignKey('welfare.id'),nullable=True)
    file_path = db.Column(db.String(225))

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(225))
    img_src = db.Column(db.String(225))
    news_src = db.Column(db.String(225))
    time_push = db.Column(db.DateTime)

class UserMessage(db.Model):
    __tablename__ = 'usermessage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('employee.id'),nullable=True)
    phone = db.Column(db.String(225))
    address = db.Column(db.String(225))
    email = db.Column(db.String(225))
    birthday = db.Column(db.DateTime)
    user = db.relationship('Employee', foreign_keys=[user_id])

class Notice(db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(225))
    content = db.Column(db.Text)
    time_release = db.Column(db.DateTime)

class Evaluation(db.Model):
    __tablename__ = 'evaluation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    judged_id=db.Column(db.Integer,db.ForeignKey('employee.id'),)
    routine = db.Column(db.Float)
    project = db.Column(db.Float)
    profession = db.Column(db.Float)
