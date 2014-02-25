#coding:utf-8
from flask.ext.login import current_user

from scapp import db
import datetime

class SC_Balance_Sheet(db.Model):
    '''
    资产负债表
    loan_type:  0：现金及银行存款(元) 1：应付账款(元) 2：应收账款(元)
                3：预收账款(元) 4：预付款项(元) 5：短期借款(元) 
                6：存货(元)  7：社会集资(元)  8：流动资产(元) 
                9：短期负债总计(元)  10：固定资产  11：长期借款(元) 
                12：其他经营资产 13：其他 14：总资产 
                15：长期负债总计 16：总负债 17：权益
                18：负债及所有者权益  19：流动比率%  20：负债率% 
                21：表外项目 22：对资产负债表的其他评价 23：经营历史与资本积累
                24：对现状的评价：经营组织和市场情况 25：对现状的评价：财务信息 26：过去12个月内的投资-业务方面
                27：过去12个月内的投资-私人方面 28：未来12个月计划的投资-业务方面 29：未来12个月计划的投资-私人方面
                30：客户在家庭或在社会经济网中的状况 
                31: 未来12个月的投资计划-生意方面
                32: 未来12个月的投资计划-个人方面
                33: 其他还款来源分析
    '''
    __tablename__ = 'sc_balance_sheet'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    loan_type=db.Column(db.Integer) #贷款类型 
    items_name = db.Column(db.String(32)) #名目
    index=db.Column(db.String(2)) #(同一类别的)序号
    content=db.Column(db.String(256)) #文本或数字的内容
    create_user = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    modify_user = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)

    def __init__(self,loan_apply_id,loan_type,items_name,index,content):
        self.loan_apply_id = loan_apply_id
        self.loan_type = loan_type
        self.items_name = items_name
        self.index = index
        self.content = content
        self.create_user = current_user.id
        self.create_date = datetime.datetime.now()


    def add(self):
        db.session.add(self)