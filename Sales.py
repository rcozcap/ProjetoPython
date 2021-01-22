from tkinter import *
import pymysql as MySQLdb

class Sales():

    def sales(self):
        self.sale = Tk()
        self.sale.title('Americanas')
        self.sale.geometry('500x450')
        self.sale.resizable(False, False)

        Label(self.sale, text= 'Insira os itens: ', padx=2, pady=30).grid(row=2, column=0)
        item = Entry(self.sale)
        item.grid(row=2, column=1)
        Button(self.sale, text='Adicionar Produto', command= Sales.add, height=2, width=15).grid(row=2, column=2, padx=20)

        self.sale.mainloop()     

    def add(self):

        itemx = self.item.get()      
                        
        con = MySQLdb.connect(host='localhost', user='developer', passwd='1234567', db='shop')

        cursor = con.cursor()

        sql_select_Query = """Select * from products Where ProdId = %s"""

        cursor.execute(sql_select_Query, (itemx,))

        row = cursor.fetchall()

        Label(self.sale, text= row[0], padx=10, pady=30).grid(row=3, column=0, columnspan=2)

        con.close()
 
Sales()