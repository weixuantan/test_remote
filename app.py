import os
from datetime import datetime
import json
from operator import and_
from flask import Flask, request, send_file
from flask.views import MethodView

import tree
from extension import db,cors
from models import Employee, Department, Welfare, Attendance, WelfareFiles, News, UserMessage, Notice, Evaluation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:a994494193@localhost:3306/hr_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True
db.init_app(app)
cors.init_app(app)



@app.cli.command()
def create():
    # db.drop_all()
    # db.create_all()
    # Department.init_db()
    # Employee.init_db()
    # Welfare.init_db()
    db.create_all()
    print(datetime.now())
class DepartmentApi(MethodView):
    def get(self, d_name):
        if not d_name:
            departments: [Department] = Department.query.all()
            results = [
                {
                    'id': department.id,
                    'd_number': department.d_number,
                    'd_name': department.d_name,
                } for department in departments
            ]
            return {
                'status': 'sucess',
                'message': '数据查询成功',
                'results': results
            }
        department: Department = Department.query.get(d_name)
        return {
            'status': 'sucess',
            'message': '数据查询成功',
            'results': {
                'id': department.id,
                    'd_number': department.d_number,
                    'd_name': department.d_name,
            }
        }
department_view = DepartmentApi.as_view('department_api')
app.add_url_rule('/department/',defaults={'d_name':None},view_func=department_view,methods=['GET'])

class NewsApi(MethodView):
    def get(self):
        news:[News] = News.query.all()
        results=[
            {
                'id':new.id,
                'title':new.title,
                'img_src':new.img_src,
                'news_src':new.news_src,
                'time_push':new.time_push.strftime("%Y-%m-%d")
            }for new in news
        ]
        return {
            'results':results
        }

    def post(self):
        new=News()
        form=request.json
        new.title=form.get('title')
        new.img_src=form.get('img_src')
        new.news_src = form.get('news_src')
        new.time_push = datetime.now()
        db.session.add(new)
        db.session.commit()

        return {'status': 'sucess',
                'message': '数据添加成功',
                }

    def delete(self,new_id):
        new = News.query.get(new_id)
        db.session.delete(new)
        db.session.commit()
        return {'status': 'sucess',
            'message': '数据删除成功'}

    def put(self,new_id):
        new:News = News.query.get(new_id)
        form = request.json
        new.title = form.get('title')
        new.img_src = form.get('img_src')
        new.news_src = form.get('news_src')
        new.time_push = datetime.now()
        db.session.commit()
        return {'status': 'sucess',
                'message': '数据修改成功'}

news_view = NewsApi.as_view('news_api')
app.add_url_rule('/news/',
                 view_func=news_view,methods=['GET'])
app.add_url_rule('/news/<int:new_id>',
                 view_func=news_view,methods=['PUT','DELETE'])
app.add_url_rule('/news/',
                 view_func=news_view,methods=['POST'])

class NoticeApi(MethodView):
    def get(self):
        notice:[Notice]=Notice.query.all()
        results = [
            {
                'id': n.id,
                'title': n.title,
                'content': n.content,
                'time_release': n.time_release.strftime("%Y-%m-%d")
            } for n in notice
        ]
        return {
            'results': results
        }
    def post(self):
        notice=Notice()
        form = request.json
        notice.title = form.get('title')
        notice.content = form.get('content')
        notice.time_release = datetime.now()
        db.session.add(notice)
        db.session.commit()

        return {'status': 'sucess',
                'message': '数据添加成功',
                }
    def put(self,notice_id):
        form = request.json
        notice:Notice=Notice.query.get(notice_id)
        notice.title = form.get('title')
        notice.content = form.get('content')
        notice.time_release = datetime.now()
        db.session.add(notice)
        db.session.commit()
        return {'status': 'sucess',
                'message': '数据修改成功'}
    def delete(self,notice_id):
        notice:Notice=Notice.query.get(notice_id)
        db.session.delete(notice)
        db.session.commit()
        return {'status': 'sucess',
            'message': '数据删除成功'}

notice_view = NoticeApi.as_view('notice_api')
app.add_url_rule('/notice/',
                 view_func=notice_view,methods=['GET'])
app.add_url_rule('/notice/<int:notice_id>',
                 view_func=notice_view,methods=['PUT','DELETE'])
app.add_url_rule('/notice/',
                 view_func=notice_view,methods=['POST'])

class UserMessageApi(MethodView):
    def get(self,user_id):
        if UserMessage.query.filter(UserMessage.user_id==user_id).first():
            user:UserMessage=UserMessage.query.filter(UserMessage.user_id==user_id).first()
            return {
                'status': 'sucess',
                'message': '数据查询成功',
                'results': {
                    'id': user.id,
                    'birthday': user.birthday.strftime("%Y-%m-%d"),
                    'address': user.address,
                    'phone': user.phone,
                    'email': user.email,
                }
            }
        else:
            return {
                'status':'none'
            }
    def post(self,user_id):
        try:
            if UserMessage.query.filter(UserMessage.user_id==user_id):
                user:UserMessage=UserMessage.query.filter(UserMessage.user_id==user_id).first()
                form = request.json
                user.user_id = user_id
                user.phone = form.get('phone')
                user.address = form.get('address')
                user.email = form.get('email')
                user.birthday = form.get('birthday')
                db.session.commit()
        except:
            user=UserMessage()
            form = request.json
            user.user_id=user_id
            user.phone = form.get('phone')
            user.address= form.get('address')
            user.email = form.get('email')
            user.birthday = form.get('birthday')
            db.session.add(user)
            db.session.commit()
        return {
            'status':'提交成功'
        }
usermessage_view = UserMessageApi.as_view('usermessage_api')
app.add_url_rule('/usermessage/<int:user_id>',
                 view_func=usermessage_view,methods=['GET','POST'])




class EmployeeApi(MethodView):
    def get(self,employee_id):
        if not employee_id:
            employees: [Employee] = Employee.query.all()
            results = [
                {
                    'id':employee.id,
                    'ee_accounts': employee.ee_accounts,
                    'ee_password': employee.ee_password,
                    'ee_role': employee.ee_role,
                    'ee_name': employee.ee_name,
                    'ee_department': employee.ee_department,
                }for employee in employees
            ]
            return {
                'status':'sucess',
                'message':'数据获取成功',
                'results':results
            }
        employee: Employee = Employee.query.get(employee_id)
        return {
            'status': 'sucess',
            'message': '数据查询成功',
            'results': {
                'id': employee.id,
                'ee_accounts': employee.ee_accounts,
                'ee_password': employee.ee_password,
                'ee_role': employee.ee_role,
                'ee_name': employee.ee_name,
                'ee_department': employee.ee_department,
            }
        }
    def post(self):
        form = request.json
        employee = Employee()
        employee.ee_accounts = form.get('ee_accounts')
        employee.ee_password = form.get('ee_password')
        employee.ee_role = form.get('ee_role')
        employee.ee_name = form.get('ee_name')
        employee.ee_department = form.get('ee_department')
        db.session.add(employee)
        db.session.commit()

        return {'status': 'sucess',
            'message': '数据添加成功',
                }

    def delete(self,employee_id):
        employee = Employee.query.get(employee_id)
        db.session.delete(employee)
        db.session.commit()
        return {'status': 'sucess',
            'message': '数据删除成功'}

    def put(self,employee_id):
        employee: Employee = Employee.query.get(employee_id)
        form = request.json
        employee.ee_accounts = form.get('ee_accounts')
        employee.ee_password = form.get('ee_password')
        employee.ee_role = form.get('ee_role')
        employee.ee_name = form.get('ee_name')
        employee.ee_department = form.get('ee_department')
        db.session.commit()
        return {'status': 'sucess',
                'message': '数据修改成功'}



employee_view = EmployeeApi.as_view('employee_api')
app.add_url_rule('/employees/',defaults={'employee_id':None},
                 view_func=employee_view,methods=['GET'])
app.add_url_rule('/employees/<int:employee_id>',
                 view_func=employee_view,methods=['GET','PUT','DELETE'])
app.add_url_rule('/employees/',
                 view_func=employee_view,methods=['POST'])
# app.add_url_rule('/employees/login',
#                  view_func=employee_view,methods=['POST'])

class LoginApi(MethodView):
    def post(self):
        form = request.json
        login_accounts = form.get('accounts')
        login_password = form.get('password')
        employee: Employee = Employee.query.filter(Employee.ee_accounts==login_accounts).first()
        if len(Employee.query.filter(
                and_(Employee.ee_accounts == login_accounts, Employee.ee_password == login_password)).all()) > 0:
            return {'status': 'login_success',
                    'message': '登录成功',
                    'employee_name':employee.ee_name,
                    'employee_id':employee.id,
                    'employee_role':employee.ee_role}
        elif len(Employee.query.filter(
                and_(Employee.ee_accounts == login_accounts, Employee.ee_password != login_password)).all()) > 0:
            return {'status': 'password_error',
                    'message': '密码错误'}
        else:
            print(login_accounts, login_password)
            return {'status': 'a_error',
                    'message': '不存在该用户'}
login_view = LoginApi.as_view('login_api')
app.add_url_rule('/login/',
                 view_func=login_view,methods=['POST'])

@app.route('/editPassword/<int:user_id>',methods=['POST'])
def editPassword(user_id):
    user:Employee=Employee.query.get(user_id)
    form=request.json
    if form.get('ee_password')!=user.ee_password:
        return {
            'status':'error',
            'message':'原密码输入错误'
        }
    else:
        user.ee_password=form.get('password')
        db.session.commit()
        return {
            'status': 'success',
            'message':'修改成功'
        }

# 福利功能

# 通过id获取用户福利
@app.route('/getWelfare/<int:user_id>',methods=['GET'])
def getWelfare(user_id):
    welfare_list:[Welfare]=Welfare.query.filter(and_(Welfare.approve_status=='已审核', Welfare.user_id == user_id)).all()
    print(welfare_list)
    results = [
        {
            'id': welfare.id,
            'user_id': welfare.user_id,
            'approver_id': welfare.approver_id,
            'approve_status': welfare.approve_status,
            'wf_amount': welfare.wf_amount,
            'wf_time':welfare.wf_time.strftime("%Y-%m-%d"),
            'wf_name': welfare.wf_name,
            'wf_desc': welfare.wf_desc,
        } for welfare in welfare_list
    ]
    return {
                'status':'sucess',
                'message':'数据获取成功',
                'results':results
            }

# 获取管理员发布的福利
@app.route('/getReleasedWelfare/',methods=['GET'])
def getReleasedWelfare():
    welfare_list: [Welfare] = Welfare.query.filter(
        and_(Welfare.user_id == 1,Welfare.approver_id == 1 )).all()
    print(welfare_list)
    results = [
        {
            'id': welfare.id,
            'user_id': welfare.user_id,
            'approver_id': welfare.approver_id,
            'approve_status': welfare.approve_status,
            'wf_amount': welfare.wf_amount,
            'wf_time': welfare.wf_time.strftime("%Y-%m-%d"),
            'wf_name': welfare.wf_name,
            'wf_desc': welfare.wf_desc,
        } for welfare in welfare_list
    ]
    approver:[Employee] = Employee.query.filter(Employee.ee_role=='负责人').all()

    return {
        'status': 'sucess',
        'message': '数据获取成功',
        'results': results,
        'approver':[
            {
                'id':approve.id,
                'ee_name':approve.ee_name
            }for approve in approver
        ]
    }

# 获取需要审核的福利
@app.route('/getAuditWelfare/<int:user_id>',methods=['GET'])
def getAuditWelfare(user_id):
    welfare_list: [Welfare] = Welfare.query.filter(
        and_(Welfare.approve_status == '待审核',Welfare.approver_id == user_id )).all()
    results = [
        {
            'id': welfare.id,
            'user_id': welfare.user_id,
            'approver_id': welfare.approver_id,
            'approve_status': welfare.approve_status,
            'wf_amount': welfare.wf_amount,
            'wf_time': welfare.wf_time.strftime("%Y-%m-%d"),
            'wf_name': welfare.wf_name,
            'wf_desc': welfare.wf_desc,
        } for welfare in welfare_list
    ]
    return {
        'status': 'sucess',
        'message': '数据获取成功',
        'results': results
    }

#获取用户审核中的福利
@app.route('/getUserAuditWelfareByID/<int:user_id>',methods=['GET'])
def getUserAuditWelfareByID(user_id):
    welfare_list: [Welfare] = Welfare.query.filter(
        and_(Welfare.approve_status!='已审核', Welfare.user_id == user_id)).all()
    results = [
        {
            'id': welfare.id,
            'user_id': welfare.user_id,
            'approver_id': welfare.approver_id,
            'approve_status': welfare.approve_status,
            'wf_amount': welfare.wf_amount,
            'wf_time': welfare.wf_time.strftime("%Y-%m-%d"),
            'wf_name': welfare.wf_name,
            'wf_desc': welfare.wf_desc,
        } for welfare in welfare_list
    ]
    print()
    return {
        'status': 'sucess',
        'message': '数据获取成功',
        'results': results
    }

# 管理员发布可申请的福利
@app.route('/releaseWelfare/',methods=['POST'])
def releaseWelfare():
    welfare = Welfare()
    form = request.json
    welfare.user_id = 1
    welfare.approver_id = 1
    welfare.approve_status = '未审核'
    welfare.wf_name = form.get('wf_name')
    welfare.wf_desc = form.get('wf_desc')
    welfare.wf_amount = form.get('wf_amount')
    welfare.wf_time = datetime.now()
    db.session.add(welfare)
    db.session.commit()
    return {
        'status': 'sucess',
        'message': '数据获取成功',
    }

# 用户申请福利
@app.route('/applyWelfare/',methods=['POST'])
def applyWelfare():
    welfare = Welfare()
    form = request.json
    welfare.user_id = form.get('user_id')
    welfare.approver_id = form.get('approver_id')
    welfare.approve_status = '待审核'
    welfare.wf_name = form.get('wf_name')
    welfare.wf_desc = form.get('wf_desc')
    welfare.wf_amount = form.get('wf_amount')
    welfare.wf_time = datetime.now()
    db.session.add(welfare)
    db.session.commit()
    print(welfare.id)
    return {
        'status': 'sucess',
        'message': '数据获取成功',
        'wf_id':welfare.id,
    }

# 负责人审核福利
@app.route('/auditWelfare/',methods=['POST'])
def auditWelfare():

    form = request.json
    welfare: Welfare = Welfare.query.get(form.get('id'))
    # welfare.user_id = form.get('user_id')
    # welfare.approver_id = form.get('approver_id')
    welfare.approve_status = form.get('approve_status')
    # welfare.wf_name = form.get('wf_name')
    # welfare.wf_desc = form.get('wf_desc')
    # welfare.wf_amount = form.get('wf_amount')
    welfare.wf_time = datetime.now()
    db.session.commit()
    return {
        'status': 'sucess',
        'message': '数据获取成功',
    }


# 出勤报备
@app.route('/applyAttendance/',methods=['POST'])
def applyAttendance():
    attendance = Attendance()
    form = request.json
    attendance.user_id = form.get('user_id')
    attendance.approver_id = form.get('approver_id')
    attendance.work_type = form.get('work_type')
    attendance.time_start = datetime.strptime(form.get('time_start'),"%Y-%m-%d %H:%M:%S")
    attendance.time_end = datetime.strptime(form.get('time_end'),"%Y-%m-%d %H:%M:%S")
    if attendance.work_type=="正常出勤":
        attendance.approve_status = '已通过'
        attendance.time_sum = (attendance.time_end-attendance.time_start).seconds//3600
    elif attendance.work_type=="因事请假" or attendance.work_type=="工作出差":
        attendance.approve_status = '待审核'
        attendance.time_sum = (attendance.time_end - attendance.time_start).days

    attendance.reason = form.get('reason')
    db.session.add(attendance)
    db.session.commit()
    print((attendance.time_end-attendance.time_start).days//6)
    return {
        'status': 'sucess',
        'message': '数据获取成功',
    }
@app.route('/auditAuttendance',methods=['POST'])
def auditAuttendance():
    form = request.json
    attendance = Attendance.query.get(form.get('id'))
    attendance.approve_status = form.get('approve_status')
    db.session.commit()
    return {
        'status': 'sucess',
        'message': '数据获取成功',
    }


# 展示个人的出勤审核状态
@app.route('/getAttendanceByID/<int:user_id>',methods=['GET'])
def getAttendanceByID(user_id):
    attendance_list:[Attendance] = Attendance.query.filter(Attendance.user_id==user_id).all()
    results=[{
        'id':attendance.id,
        'work_type':attendance.work_type,
        'approve_status':attendance.approve_status,
        'time_start':attendance.time_start.strftime("%Y-%m-%d"),
        'time_sum':attendance.time_sum
    }for attendance in attendance_list]
    approver: [Employee] = Employee.query.filter(Employee.ee_role == '负责人').all()
    return {
        'results':results,
        'approver': [
            {
                'id': approve.id,
                'ee_name': approve.ee_name
            } for approve in approver
        ]
    }

@app.route('/getAuditAuttendance/<int:approve_id>',methods=['GET'])
def getAuditAuttendance(approve_id):
    attendance_list: [Attendance] = Attendance.query.filter(and_(Attendance.approver_id == approve_id,Attendance.approve_status=="待审核")).all()
    audited_user=Employee()
    results = [{
        'id': attendance.id,
        'work_type': attendance.work_type,
        'approve_status': attendance.approve_status,
        'time_start': attendance.time_start.strftime("%Y-%m-%d"),
        'time_end': attendance.time_end.strftime("%Y-%m-%d"),
        'time_sum': attendance.time_sum,
        'audited_name':audited_user.query.filter(Employee.id==attendance.user_id).first().ee_name,
        'reason':attendance.reason
    } for attendance in attendance_list]
    print(results)
    return {
        'results':results,}

@app.route('/uploadFiles/<int:wf_id>',methods=['POST'])
def uploadFiles(wf_id):
    files = request.files.getlist('file')

    filepaths = []
    error_filenames =[]
    basedif = os.path.abspath(os.path.dirname(__file__))
    path = basedif + "/static/welfareUpload/"
    for file in files:
        wf_field = WelfareFiles()
        filename = file.filename
        file_path = path + filename
        file.save(file_path)
        wf_field.wf_id = wf_id
        wf_field.file_path = file_path
        db.session.add(wf_field)
        db.session.commit()
        filepaths.append(file_path)
    result ={
        'code':200,
        'result':'sucess',
        'message': filepaths
    }
    print(files)
    return result

@app.route('/getWelfareFiles/<int:wf_id>',methods=['GET'])
def getWelfareFiles(wf_id):
    wf_fileList:[WelfareFiles]=WelfareFiles.query.filter(WelfareFiles.wf_id==wf_id).all()
    result=[]
    for wf_file in wf_fileList:
        result.append(wf_file.file_path)
    print(result)
    return {'results':result}


@app.route('/downloadFiles',methods=['POST'])
def downloadFiles():
    filepath = request.json['filepath']
    print('正常')
    return send_file(filepath,as_attachment=True)

@app.route('/getAttendanceChart/<int:user_id>',methods=['GET'])
def getAttendanceChart(user_id):
    attendance:[Attendance] = Attendance.query.filter(and_(Attendance.user_id==user_id,Attendance.work_type=="正常出勤")).order_by(Attendance.time_start.desc()).limit(7)[::-1]

    xData=[]
    yData=[]
    for a in attendance:
        xData.append(a.time_start.strftime("%Y-%m-%d"))
        yData.append(a.time_sum)
    return {
        'xData':xData,
        'yData':yData
    }

@app.route('/getEvaluationByID/<int:user_id>',methods=['GET'])
def getEvaluationByID(user_id):
    user:Employee=Employee.query.get(user_id)
    judged_user:Employee=Employee.query.filter(and_(Employee.id!=user_id,Employee.ee_department==user.ee_department)).all()
    user_evaluation:Evaluation=Evaluation.query.filter(Evaluation.user_id==user_id).all()
    # judger_list=[val for val in judged_user.id if val not in user_evaluation.user_id ]
    user_list=[]
    for u in user_evaluation:
        user_list.append(u.judged_id)
    results = [{
        'id': employee.id,
        'ee_accounts': employee.ee_accounts,
        'ee_role': employee.ee_role,
        'ee_name': employee.ee_name,
        'ee_department': employee.ee_department,
    }for employee in judged_user if employee.id not in user_list ]
    print(user_list)
    return {
        'results':results,
        'user_len':len(judged_user),
        'judged_len':len(user_evaluation)
    }

@app.route('/addEvaluation/',methods=['POST'])
def addEvaluation():
    form=request.json


    if len(Evaluation.query.filter(and_(Evaluation.user_id == form.get('user_id'),Evaluation.judged_id==form.get('judged_id'))).all())!=0:
            return {
                'status':'error',
                'message':'你已提交过对该员工的评价，请勿重复评价'
            }
    else:
        evaluation=Evaluation()

        evaluation.user_id = form.get('user_id')
        evaluation.judged_id = form.get('judged_id')
        evaluation.routine = form.get('routine')
        evaluation.project = form.get('project')
        evaluation.profession = form.get('profession')
        db.session.add(evaluation)
        db.session.commit()
    return {
        'status': 'success',
        'message':'提交成功',
    }

@app.route('/inputTestDevc/<int:user_id>',methods=['GET'])
def inputTestDevc(user_id):
    attendance:[Attendance] = Attendance.query.filter(and_(Attendance.user_id==user_id,Attendance.work_type=="正常出勤")).order_by(Attendance.time_start.desc()).limit(7)[::-1]
    time_count=0
    r_count=0
    p1_count=0
    p2_count=0
    test=[]
    for a in attendance:
        time_count+=a.time_sum
    a_time=round(time_count/len(attendance),1)
    if a_time>=8:
        test.append(1)
    else:
        test.append(0)
    user_evaluation:[Evaluation]=Evaluation.query.filter(Evaluation.judged_id==user_id).all()
    for e in user_evaluation:
        r_count+=e.routine
        p1_count+=e.project
        p2_count += e.profession
    e_r=r_count/len(user_evaluation)
    if e_r>=3 and e_r<4:
        test.append(1)
    elif e_r>=4:
        test.append(2)
    else:
        test.append(0)

    e_p=(p1_count*0.6+p2_count*0.4)/len(user_evaluation)
    if e_p>=3 and e_p<4:
        test.append(1)
    elif e_p>=4:
        test.append(2)
    else:
        test.append(0)
    user_welfare:[Welfare]=Welfare.query.filter(Welfare.approve_status=='已审核',Welfare.user_id==user_id).all()
    e_w=round(len(user_welfare),1)
    if e_w>=3:
        test.append(1)
    else:
        test.append(0)
    dataSet, labels = tree.createDataSet()
    featLabels = []
    myTree = tree.createTree(dataSet, labels, featLabels)
    result = tree.classify(myTree, featLabels, test)
    print(result)
    results={
        'a_time':a_time,
        'e_r':e_r,
        'e_p':e_p,
        'e_w':e_w,
        'result':result
    }
    return {
        "results":results
    }
if __name__ == '__main__':
    app.run()
