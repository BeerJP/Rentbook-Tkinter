from mysql.connector import connect
from pymysql import *


class Connect:
    def __init__(self):
        self.conn = connect(
            host="localhost",
            user="root",
            password="",
            database="db_library"
        )

    def bookInsert(self, b_id, b_name, b_unit, sc_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO books (b_id, b_name, b_unit, sc_id) VALUES (%s, %s, %s, %s)"
        value = (b_id, b_name, b_unit, sc_id)
        cursor.execute(query, value)
        self.conn.commit()
        cursor.close()

    def show_AllBooks(self):
        cursor = self.conn.cursor()
        query = "SELECT b_id,b_name,b_unit FROM books ORDER BY b_id"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return list(result)

    def show_Books(self, category):
        cursor = self.conn.cursor()
        query = """SELECT
                       b.b_id,b.b_name,b.b_unit
                    FROM
                        books as b
                    INNER JOIN
                        sub_category as sc ON b.sc_id = sc.sc_id
                    WHERE 
                        sc.c_id = %s
                    ORDER BY b.b_id"""
        cursor.execute(query, category)
        result = cursor.fetchall()
        cursor.close()
        return list(result)

    def show_Unit(self, b_id):
        cursor = self.conn.cursor()
        query = "SELECT b_unit,b_rent FROM books WHERE b_id = %s"
        cursor.execute(query, b_id)
        result = cursor.fetchone()
        cursor.close()
        return list(result)

    def show_Sc(self, category):
        cursor = self.conn.cursor()
        query = """SELECT
                       sc.sc_name
                    FROM
                        sub_category as sc
                    INNER JOIN
                        category as c ON sc.c_id = c.c_id
                    WHERE 
                        c.c_name = %s"""
        cursor.execute(query, category)
        result = cursor.fetchall()
        cursor.close()
        return list(result)

    def c_id(self, category):
        cursor = self.conn.cursor()
        query = "SELECT c_id from category WHERE c_name = %s"
        cursor.execute(query, category)
        result = cursor.fetchone()
        cursor.close()
        return list(result)

    def sc_id(self, sub_category):
        cursor = self.conn.cursor()
        query = "SELECT sc_id from sub_category WHERE sc_name = %s"
        cursor.execute(query, sub_category)
        result = cursor.fetchone()
        cursor.close()
        return list(result)

    def check_bID(self, b_id):
        cursor = self.conn.cursor()
        query = "SELECT b_id from books WHERE b_id LIKE %s"
        cursor.execute(query, b_id)
        result = cursor.fetchall()
        cursor.close()
        return list(result)

    def show_Member(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM member"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return list(result)

    def show_Mid(self, m_id):
        cursor = self.conn.cursor()
        query = "SELECT m_id from member WHERE m_id = %s"
        cursor.execute(query, m_id)
        result = cursor.fetchone()
        cursor.close()
        return list(result)

    def word_Member(self, word1, word2, word3):
        cursor = self.conn.cursor()
        query = """SELECT * FROM member 
                    WHERE m_id LIKE %s
                    OR m_fname LIKE %s
                    OR m_lname LIKE %s"""
        val = (word1, word2, word3)
        cursor.execute(query, val)
        result = cursor.fetchall()
        cursor.close()
        return list(result)

    def member_insert(self, m_fn, m_ln, m_ph, m_dt):
        cursor = self.conn.cursor()
        query = "INSERT INTO member (m_fname, m_lname, m_phone, m_reg) VALUES (%s, %s, %s, %s)"
        value = (m_fn, m_ln, m_ph, m_dt)
        cursor.execute(query, value)
        self.conn.commit()
        cursor.close()

    def show_Order(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM orders"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return list(result)

    def show_Oid(self, o_id):
        cursor = self.conn.cursor()
        query = "SELECT o_id, du_date, o_st from orders WHERE o_id = %s"
        cursor.execute(query, o_id)
        result = cursor.fetchone()
        cursor.close()
        return list(result)

    def select_Oid(self):
        cursor = self.conn.cursor()
        query = "SELECT o_id FROM orders ORDER BY o_id DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return list(result)

    def return_detail(self, o_id):
        cursor = self.conn.cursor()
        query = """SELECT
                       b.b_id,b.b_name
                    FROM
                        books as b
                    INNER JOIN
                        order_details as od ON od.b_id = b.b_id
                    WHERE
                        od.o_id = %s
                    ORDER BY b.b_id"""
        cursor.execute(query, o_id)
        result = cursor.fetchall()
        cursor.close()
        return list(result)

    def order_insert(self, o_id, m_id, rn, re):
        cursor = self.conn.cursor()
        query = "INSERT INTO orders (o_id, m_id, rn_date, du_date, o_st) VALUES (%s, %s, %s, %s, %s)"
        value = (o_id, m_id, rn, re, "0")
        cursor.execute(query, value)
        self.conn.commit()
        cursor.close()

    def order_detail(self, b_id, o_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO order_details (b_id, o_id) VALUES (%s, %s)"
        value = (b_id, o_id)
        cursor.execute(query, value)
        self.conn.commit()
        cursor.close()

    def return_insert(self, re, oid):
        cursor = self.conn.cursor()
        query = "INSERT INTO returns (re_date, o_id) VALUES (%s, %s)"
        value = (re, oid)
        cursor.execute(query, value)
        self.conn.commit()
        cursor.close()

    def get_reDate(self, o_id):
        cursor = self.conn.cursor()
        query = "SELECT re_date FROM returns WHERE o_id = %s"
        cursor.execute(query, o_id)
        result = cursor.fetchone()
        cursor.close()
        return result

    def book_update(self, unit, rent, b_id):
        cursor = self.conn.cursor()
        query = """UPDATE books SET 
                    b_unit = %s, b_rent = %s
                    WHERE b_id = %s"""
        value = (unit, rent, b_id)
        cursor.execute(query, value)
        self.conn.commit()
        cursor.close()

    def order_update(self, o_id):
        cursor = self.conn.cursor()
        query = """UPDATE orders SET o_st = %s WHERE o_id = %s"""
        value = ("1", o_id)
        cursor.execute(query, value)
        self.conn.commit()
        cursor.close()

    def check_Order(self, m_id):
        cursor = self.conn.cursor()
        query = """SELECT o_st 
                    FROM orders
                    WHERE m_id = %s 
                    ORDER BY m_id DESC LIMIT 1"""
        cursor.execute(query, m_id)
        result = cursor.fetchone()
        cursor.close()
        return list(result)
