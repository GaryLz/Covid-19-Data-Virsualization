import time
import pymysql


def getTime():
    time_str = time.strftime("%Y{}%m{}%d{} %X");
    return time_str.format("年", "月", "日")


def get_conn():
    """
    :return: 连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="ip地址",
                           user="用户名",
                           password="密码",
                           db="数据库名",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，((),(),)的形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res

def get_last_update_time():
    """
    :return: 返回大屏div class=update_time 的数据
    """
    # 取最新的时间戳
    sql = "select update_time from details order by update_time desc limit 1"
    res = query(sql)[0][0]
    return res.strftime("%Y-%m-%d %X");

def get_c1_data():
    """
    :return: 返回大屏div id=c1 的数据
    """
    # 取时间戳最新的那组数据
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal)," \
          "sum(dead) " \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    res_list = [str(i) for i in res[0]]
    res_tuple=tuple(res_list)
    return res_tuple



def get_c2_data():
    """
    :return:  返回各省数据
    """
    # 取时间戳最新的那组数据
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res


def get_l1_data():
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res


def get_l2_data():
    sql = "select ds,confirm_add,heal_add,dead_add from history"
    res = query(sql)
    return res


def get_r1_data():
    """
    :return:  返回非湖北地区城市确诊人数前5名
    """
    sql = 'SELECT province,confirm_add FROM ' \
          '(select province,sum(confirm_add) as confirm_add from details  ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'group by province) as a ' \
          'ORDER BY confirm_add DESC LIMIT 5'
    res = query(sql)
    return res


def get_r2_data():
    '''
        获取世界各国的疫情数据
        :return:
    '''
    # 取时间戳最新的那组数据
    sql = "select province,sum(confirm_add) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res


if __name__ == "__main__":
    print(get_c2_data())
    print(get_r2_data())

