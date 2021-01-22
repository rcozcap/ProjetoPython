from tkinter import *
from tkinter import ttk
import pymysql as MySQLdb

class Main():
    
    def start(self):
        self.main = Tk()
        self.main.title('Americanas')
        self.main.geometry('500x450')
        self.main.resizable(False, False)

        menubar = Menu(self.main)
        self.main.config(menu=menubar)

        filemenu = Menu(menubar)
        filemenu1 = Menu(menubar)
        filemenu2 = Menu(menubar)

        menubar.add_cascade(label = 'Menu', menu = filemenu)
        menubar.add_cascade(label = 'Vendas', menu = filemenu1)
        menubar.add_cascade(label = 'Notas Fiscais', menu = filemenu2)

        filemenu.add_command(label = 'Editar')
        filemenu1.add_command(label = 'Novo', command = self.sales)
        filemenu2.add_command(label = 'Balanço do dia')

        self.main.mainloop()

    def sales(self):
        self.sale = Tk()
        self.sale.title('Americanas')
        self.sale.geometry('550x450')
        self.sale.resizable(False, False)

        Label(self.sale, text= 'Insira o código do item: ', padx=2, pady=30).grid(row=2, column=0)
        self.item = Entry(self.sale)
        self.item.grid(row=2, column=1)
        Button(self.sale, text='Adicionar Produto', command= self.add, height=2, width=15).grid(row=2, column=2, padx=20)
        Button(self.sale, text='Finalizar Compra', command= self.final, height=2, width=15).grid(row=4, column=2, pady=20, rowspan=4)

        self.tree=ttk.Treeview(self.sale, selectmode='browse', columns=('column1', 'column2', 'column3', 'column4'),show='headings')

        self.tree.column('column1', width=50, minwidth=50, stretch=NO)
        self.tree.heading('#1', text='ID')

        self.tree.column('column2', width=200, minwidth=50, stretch=NO)
        self.tree.heading('#2', text='NOME')

        self.tree.column('column3', width=200, minwidth=50, stretch=NO)
        self.tree.heading('#3', text='CATEGORIA')

        self.tree.column('column4', width=100, minwidth=50, stretch=NO)
        self.tree.heading('#4', text='PREÇO')

        self.tree.grid(row=3, column=0, columnspan=3)

        self.sale.mainloop()     

    def add(self):

        self.itemx = int(self.item.get())

        self.con = MySQLdb.connect(host='localhost', user='developer', passwd='1234567', db='shop')

        self.cursor = self.con.cursor()

        self.sql_select_Query = """Select * from products Where ProdId = %s"""

        self.cursor.execute(self.sql_select_Query, (self.itemx,))

        while TRUE:

            row = self.cursor.fetchone()

            self.tree.insert('', END, values=row)

            #Label(self.sale, text= row[0], padx=10, pady=30).grid(row=0, column=0, columnspan=2)
        
        self.con.close()    


                           
    ''' def con(self):

        con = MySQLdb.connect(host='localhost', user='developer', passwd='1234567', db='shop')

        cursor = con.cursor()

        sql_select_Query = """Select * from products Where ProdId = %s"""

        cursor.execute(sql_select_Query, (self.itemx,))

        row = cursor.fetchall()

        Label(self.sale, text= row[0], padx=10, pady=30).grid(row=3, column=0, columnspan=2)

        con.close()   '''     
            
    def final(self):

        self.sale = Tk()
        self.sale.title('Americanas')
        self.sale.geometry('550x450')
        self.sale.resizable(False, False)

        lb_nf = LabelFrame(self.sale, text="Nota Fiscal", borderwidth=1, relief='solid')
        lb_nf.place(x=30, y=10, width=400, height=400)

        list_children = self.tree.get_children()
        Citem = len(list_children)
        lb1 = Label(lb_nf, text= "Total de itens: {}\n".format(Citem))
        for child_item in list_children:
            
            lb2 = Label(lb_nf, text= "Total de itens: {}".format(self.tree.item(child_item)['Values']))
            lb1.pack()
            lb2.pack()
    
        self.sale.mainloop()     


        '''
        print(' / LOJAS AMERICANAS / ' * 10)
        print('=-=-' * 20)
        preco = float(input('Preço das compras:'))
        print('=-=-' * 20)
        print(FORMAS DE PAGAMENTO:
            [1] - À VISTA DINHEIRO/CHEQUE
            [2] - À VISTA NO CARTÃO
            [3] - 2x NO CARTÃO
            [4] - 3x OU MAIS NO CARTÃO
            [5] - APLICAR DESCONTO)
        print('=-=-' * 20)
        opcao = int(input('ESCOLHA SUA OPÇÃO'))
        print('=-=-' * 20)
        if opcao == 1:
            total = preco - (preco * 10 /100)

        elif opcao == 2:
            total = preco - (preco * 10/100)

        elif opcao == 3:
            total = preco
            parcela = total / 2
            print(f'Sua compra de R${total:.2f} será parcelada em 2x de R${parcela:.2f} no cartão')

        elif opcao == 4:
            total = preco + (preco * 20 / 100)
            totalparc = int(input('Qual a quantidade de parcelas ?'))
            parcela = total/totalparc
            print(f'Sua compra de R${preco:.2f}, com juros custara R${total:.2f} parcelado em {totalparc}x de R${parcela:.2f} no cartão')

        elif opcao == 5:
            desc = float(input('Qual a porcentagem de desconto ?'))
            total = preco - (preco * desc / 100 )
            print(f'SUA COMPRA CUSTARA R${total:.2f}')

        else:
            total = preco
            print('OPCÇÃO INVALIDA, TENTE NOVAMENTE!')

        print(f'Sua compra de R${preco:.2f}, irá custar R${total:.2f} no final da compra')
        '''

Main().start()