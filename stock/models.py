from django.db import models
import login.models

# Create your models here.
class stock_relate(models.Model):
    code = models.CharField(max_length=128,primary_key=True,unique=True,verbose_name="股票代码")
    category_id = models.ForeignKey('category',on_delete=models.CASCADE,db_column="category_id")

    class Meta:
        db_table = "stock_relate"

class CUR_STOCK(models.Model):
    CODE = models.OneToOneField('stock_relate',on_delete=models.CASCADE,primary_key=True,db_column="CODE")
    NAME = models.CharField(max_length=256,verbose_name="名称")
    PRICE = models.FloatField(max_length=256,verbose_name="价格")
    PERCENT = models.FloatField(max_length=256,verbose_name="涨跌幅")
    UPDOWN = models.FloatField(max_length=256,verbose_name="涨跌额")
    FIVE_MINUTE = models.FloatField(max_length=256,verbose_name="5分钟涨跌额")
    OPEN = models.FloatField(max_length=256,verbose_name="今开")
    YESTCLOSE = models.FloatField(max_length=256,verbose_name="昨收")
    HIGH = models.FloatField(max_length=256,verbose_name="最高")
    LOW = models.FloatField(max_length=256,verbose_name="最低")
    VOLUME = models.BigIntegerField(verbose_name="成交量")
    TURNOVER = models.FloatField(max_length=256,verbose_name="成交额")
    HS = models.FloatField(max_length=256,verbose_name="换手率")
    LB = models.FloatField(max_length=256,verbose_name="量比")
    WB = models.FloatField(max_length=256,verbose_name="委比")
    ZF = models.FloatField(max_length=256,verbose_name="振幅")
    PE = models.FloatField(max_length=256,verbose_name="市盈率")
    MCAP = models.FloatField(max_length=256,verbose_name="流通市值")
    TCAP = models.FloatField(max_length=256,verbose_name="总市值")
    MFSUM = models.FloatField(max_length=256,verbose_name="每股收益")
    MFRATIO_1 = models.FloatField(max_length=256,verbose_name="净利润",null=True)
    MFRATIO_2 = models.FloatField(max_length=256,verbose_name="主营收",null=True)
    DATE = models.CharField(max_length=256,verbose_name="爬取时间")

    def __str__(self):
        return self.CODE

    class Meta:
        db_table = "CUR_STOCK"

class category(models.Model):
    cate_id = models.CharField(max_length=128, verbose_name="类型编号",primary_key=True,unique=True)
    cate_name = models.CharField(max_length=256,verbose_name="类型名称")

    def __str__(self):
        return self.cate_id

    class Meta:
        db_table = "stock_category"

class company_info(models.Model):
    code = models.OneToOneField('stock_relate',on_delete=models.CASCADE,primary_key=True,db_column="code")
    form = models.CharField(max_length=256,verbose_name="组织形式",null=True)
    region = models.CharField(max_length=256,verbose_name="地域",null=True)
    name_c = models.CharField(max_length=256,verbose_name="中文简称",null=True)
    location = models.CharField(max_length=256,verbose_name="办公地址",null=True)
    full_name = models.CharField(max_length=256,verbose_name="公司全称",null=True)
    phone_c = models.CharField(max_length=256,verbose_name="公司电话",null=True)
    name_e = models.CharField(max_length=256,verbose_name="英语名称",null=True)
    email_c = models.EmailField(verbose_name="公司电子邮箱",null=True)
    capital = models.CharField(max_length=256,verbose_name="注册资本",null=True)
    chairman = models.CharField(max_length=256,verbose_name="董事长",null=True)
    number = models.CharField(max_length=256,verbose_name="员工人数",null=True)
    secretary = models.CharField(max_length=256,verbose_name="董事会秘书",null=True)
    representative = models.CharField(max_length=256,verbose_name="法人代表",null=True)
    phone_s = models.CharField(max_length=256,verbose_name="董秘电话",null=True)
    general_manager = models.CharField(max_length=256,verbose_name="总经理",null=True)
    fax_s = models.CharField(max_length=256,verbose_name="董秘传真",null=True)
    website = models.CharField(max_length=256,verbose_name="信息披露网址",null=True)
    newspaper = models.CharField(max_length=256,verbose_name="信息披露报纸名称",null=True)
    business_m = models.TextField(verbose_name="主营业务",null=True)
    business_s = models.TextField(verbose_name="经营范围",null=True)
    history = models.TextField(verbose_name="公司沿革",null=True)
    date_set = models.CharField(max_length=256,verbose_name="成立日期",null=True)
    date_launch = models.CharField(max_length=256,verbose_name="上市日期",null=True)
    type = models.CharField(max_length=256,verbose_name="发行方式",null=True)
    value = models.CharField(max_length=256,verbose_name="面值",null=True)
    num_issue = models.CharField(max_length=256,verbose_name="发行数量",null=True)
    price_issue = models.CharField(max_length=128,verbose_name="发行价格",null=True)
    total_price = models.CharField(max_length=256,verbose_name="募资资金总额",null=True)
    total_issue = models.CharField(max_length=256,verbose_name="发行费用",null=True)
    rate_issue = models.CharField(max_length=128,verbose_name="发行中签率",null=True)
    PE_ratio = models.CharField(max_length=128,verbose_name="发行市盈率",null=True)
    earn_per = models.CharField(max_length=256,verbose_name="发行后每股收益",null=True)
    net_worth = models.CharField(max_length=256,verbose_name="发行后每股净资产",null=True)
    open_first = models.CharField(max_length=256,verbose_name="上市首日开盘价",null=True)
    close_first = models.CharField(max_length=256,verbose_name="上市首日收盘价",null=True)
    turnover_first = models.CharField(max_length=256,verbose_name="上市首日换手率",null=True)
    underwriter = models.CharField(max_length=256,verbose_name="主承销商",null=True)
    sponsor_list = models.CharField(max_length=256,verbose_name="上市保荐人",null=True)
    firm_account = models.CharField(max_length=256,verbose_name="会计师事务所",null=True)

    class Meta:
        db_table = "stock_company_info"

class history_data(models.Model):
    date = models.DateField(verbose_name="日期")
    code = models.ForeignKey('stock_relate',on_delete=models.CASCADE,db_column="code")
    close = models.FloatField(max_length=256, verbose_name="收盘价",null=True)
    high = models.FloatField(max_length=256, verbose_name="最高价",null=True)
    low = models.FloatField(max_length=256, verbose_name="最低价",null=True)
    open = models.FloatField(max_length=256,verbose_name="开盘价",null=True)
    yest_close = models.FloatField(max_length=256,verbose_name="开盘价",null=True)
    updown = models.FloatField(max_length=256,verbose_name="涨跌额",null=True)
    percent = models.FloatField(max_length=256,verbose_name="涨跌幅",null=True)
    hs = models.FloatField(max_length=128, verbose_name="换手率(%)",null=True)
    volumn = models.FloatField(max_length=256,verbose_name="成交量(手)",null=True)
    turnover = models.FloatField(max_length=256,verbose_name="成交金额(万元)",null=True)
    tcap = models.FloatField(max_length=256,verbose_name="总市值",null=True)
    mcap = models.FloatField(max_length=256, verbose_name="流通市值",null=True)

    class Meta:
        db_table = "stock_history_data"

class myFavourite(models.Model):
    id = models.ForeignKey("login.User",on_delete=models.CASCADE,related_name="favourite_user_id",db_column="user_id")
    code = models.ForeignKey("stock_relate",on_delete=models.CASCADE,related_name="favour_user_code",db_column="favour_code")
    c_time = models.TimeField(auto_now_add=True,unique=True,primary_key=True)

    class Meta:
        db_table = "stock_myFavourite"

