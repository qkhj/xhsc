#coding:utf-8
from flask.ext.login import current_user

from scapp import db
import datetime

# 交叉检验
class SC_Cross_Examination(db.Model):
    '''
    资产负债表
    loan_type:  0：销售额交叉检验 1：毛利润/成本交叉检验 2：其他交叉检验
                3：期初权益合计 4：分析期间收入合计 5：大项支出合计
                6：其他收入  7：升值  8：折旧(资产负债表内折旧)
                9：表外资产  10：应有权益  11：实际权益(资产负债表所有者权益)
                12：权益差额(应有权益-实际权益) 13：分析期间累计收入 14：权益交叉检验比率 
    '''
    __tablename__ = 'sc_cross_examination'
    id = db.Column(db.Integer, primary_key=True)
    loan_apply_id=db.Column(db.Integer)
    loan_type=db.Column(db.Integer) #类型 
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