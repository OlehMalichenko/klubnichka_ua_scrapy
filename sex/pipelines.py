from pprint import pprint
import pymysql

class SexPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = pymysql.connect(host='localhost',
                               user='root',
                               passwd='',
                               database='sexshop',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()
        print('Cursor create')


    def process_item(self, item, spider):
        self.store_db(item)
        return item


    def store_db(self, item):
        query = """INSERT INTO klubnichka (href_1, href_2, name, link, price, old_price, available)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (item['href_1'],
                  item['href_2'],
                  item['name'],
                  item['link'],
                  item['price'],
                  item['old_price'],
                  item['available'])
        self.cursor.execute(query, values)
        self.conn.commit()


    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        print('clouse_spider from pipelines')
