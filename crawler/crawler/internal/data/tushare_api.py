import tushare as ts


class StockApi:
    def __init__(self, token=''):
        self.pro = ts.pro_api(token)

    def get_stock_basic(self):
        """
        作用: 查询当前所有正常上市交易的股票列表
        """
        df_stock = self.pro.stock_basic(exchange='', list_status='L')
        return df_stock

    def get_trade_cal(self, start_date, end_date, exchange="SSE"):
        """
        获取各大交易所交易日历数据,默认提取的是上交所
        """
        df = self.pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date)
        return df

    def get_hs_const(self, hs_type='SH', is_new=1):
        """
        作用: 获取沪股通、深股通成分数据
        """
        # 获取沪股通成分
        # df = pro.hs_const(hs_type='SH')

        # 获取深股通成分
        # df = pro.hs_const(hs_type='SZ')

        df = self.pro.hs_const(hs_type=hs_type, is_new=is_new)
        return df

    def get_stock_company(self, ts_code, exchange):
        """
        param exchange: SSE-上交所 SZSE-深交所
        作用: 获取上市公司基础信息，单次提取4000条，可以根据交易所分批提取
        """
        df = self.pro.stock_company(exchange=exchange)
        return df

    def get_moneyflow_hsgt(self):
        """
        作用：获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制
        """
        df = self.pro.moneyflow_hsgt(start_date='20180125', end_date='20180808')
        return df

    def get_daily(self, ts_code, start_date, end_date):
        """
        数据说明：交易日每天15点～16点之间。本接口是未复权行情，停牌期间不提供数据。
        描述：获取股票行情数据，或通过通用行情接口获取数据，包含了前后复权数据
        """
        df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df

    def get_pro_bar(self, ts_code, start_date=None, end_date=None, adj='qfq'):
        """
        作用: 获取股票复权行情数据
        ts_code	    str	Y	证券代码
        start_date	str	N	开始日期 (格式：YYYYMMDD)
        end_date	str	N	结束日期 (格式：YYYYMMDD)
        asset	    str	Y	资产类别：E股票 I沪深指数 C数字货币 F期货 FD基金 O期权，默认E
        adj	        str	N	复权类型(只针对股票)：None未复权 qfq前复权 hfq后复权 , 默认None
        freq	    str	Y	数据频度 ：1MIN表示1分钟（1/5/15/30/60分钟） D日线 ，默认D
        ma	        list	N	均线，支持任意周期的均价和均量，输入任意合理int数值
        """
        df = ts.pro_bar(ts_code=ts_code, adj=adj, start_date=start_date, end_date=end_date)
        return df


class IndexApi:
    def __init__(self, token=''):
        self.pro = ts.pro_api(token)

    def get_index_basic(self, market):
        """
        描述：获取指数基础信息
        market	    str	Y	交易所或服务商
        publisher	str	N	发布商
        category	str	N	指数类别

        market:
            MSCI	MSCI指数
            CSI 	中证指数
            SSE	    上交所指数
            SZSE	深交所指数
            CICC	中金指数
            SW  	申万指数
            OTH	    其他指数
        """
        df = self.pro.index_basic(market='SW')
        return df

    def get_index_daily(self, ts_code, start_date, end_date):
        """
        作用: 获取指数每日行情
        权限: 常规指数需累积200积分可调取
        ts_code	str	TS指数代码
        """
        df = self.pro.index_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df

    def get_index_weight(self, ts_code, start_date, end_date):
        """
        描述：获取各类指数成分和权重，月度数据 ，如需日度指数成分和权重，请联系 waditu@163.com
        来源：指数公司网站公开数据
        积分：用户需要至少400积分才可以调取
        """
        df = self.pro.index_weight(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df


class FundApi:
    def __init__(self, token=''):
        self.pro = ts.pro_api(token)

    def get_fund_nav(self, ts_code, start_date, end_date):
        """
        描述：获取公募基金净值数据
        积分：用户需要至少400积分才可以调取

        ts_code	    str	N	TS基金代码 （二选一）
        end_date	str	N	净值日期 （二选一）
        market	    str	N	E场内 O场外
        """
        df = self.pro.fund_nav(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df

    def get_fund_portfolio(self, ts_code):
        """
        描述：获取公募基金持仓数据，季度更新
        积分：用户需要至少1000积分才可以调取
        """
        df = self.pro.fund_portfolio(ts_code=ts_code)
        return df

    def get_fund_daily(self, ts_code, start_date, end_date):
        """
        描述：获取场内基金日线行情，类似股票日行情
        更新：每日收盘后2小时内
        限量：单次最大800行记录，总量不限制
        积分：用户需要至少500积分才可以调取
        """
        df = self.pro.fund_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df


class IndustryApi:
    def __init__(self, token=''):
        self.pro = ts.pro_api(token)

    def get_index_classify(self, index_code=None, level='L1', src='SW'):
        """
        描述：获取申万行业分类，包括申万28个一级分类，104个二级分类，227个三级分类的列表信息
        权限：用户需2000积分可以调取，具体请参阅积分获取办法

        index_code	str	N	指数代码
        level	    str	N	行业分级（L1/L2/L3）
        src	        str	N	指数来源（SW申万）
        """
        # 获取申万一级行业列表
        df = self.pro.index_classify(index_code=index_code, level=level, src=src)
        return df

    def get_index_member(self, index_code):
        """
        描述：申万行业成分
        限量：单次最大2000行，总量不限制
        权限：用户需2000积分可调取
    
        index_code	str	N	指数代码
        ts_code	    str	N	股票代码
        is_new	    str	N	是否最新（默认为“Y是”）
        """
        # 获取黄金分类的成份股
        df = self.pro.index_member(index_code=index_code)

        # 获取000001.SZ所属行业
        # df = pro.index_member(ts_code='000001.SZ')
        return df
