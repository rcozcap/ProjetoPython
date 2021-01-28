from tkinter import *
from tkinter import ttk
import pymysql as MySQLdb

class Main():
    
    def start(self):

        #Tela principal 

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

        #Tela de inserção de produtos

        self.sale = Tk()
        self.sale.title('Americanas')
        self.sale.geometry('550x450')
        self.sale.resizable(False, False)

        self.insert = Label(self.sale, text= 'Insira o código do item: ', padx=2, pady=30).grid(row=2, column=0)
        self.item = Entry(self.sale)
        self.item.grid(row=2, column=1)
        self.insbut = Button(self.sale, text='Adicionar Produto', command= self.add, height=2, width=15).grid(row=2, column=2, padx=20)
        self.finbut = Button(self.sale, text='Escolher Forma de Pagamento', command= self.pay, height=2, width=25).grid(row=4, column=2, pady=20, rowspan=4)
        
        #Treeview
        #Definimos os detalhes da Treeview, colunas, tamanho delas e os nomes(headings) que vão receber

        self.tree=ttk.Treeview(self.sale, selectmode='browse', columns=('column1', 'column2', 'column3', 'column4'),show='headings')

        self.tree.column('column1', width=50, minwidth=50, stretch=NO)
        self.tree.heading('#1', text='ID')

        self.tree.column('column2', width=200, minwidth=50, stretch=NO)
        self.tree.heading('#2', text='NOME')

        self.tree.column('column3', width=200, minwidth=50, stretch=NO)
        self.tree.heading('#3', text='CATEGORIA')

        self.tree.column('column4', width=100, minwidth=50, stretch=NO)
        self.tree.heading('#4', text='PREÇO')

        #Definição de onde a Treeview vai se posicionar na tela

        self.tree.grid(row=3, column=0, columnspan=3)

        self.sale.mainloop()     

    def add(self):

        #Conexão com o banco de dados
        #Como o Id é o mesmo que o inserido no banco de dados esse parâmetro é capturado aqui

        self.itemx = int(self.item.get())

        self.con = MySQLdb.connect(host='localhost', user='developer', passwd='1234567', db='shop')

        self.cursor = self.con.cursor()

        #E depois passado como parte do comando SQL no where para trazer o produto selecionado

        self.sql_select_Query = """Select * from products Where ProdId = %s"""

        self.cursor.execute(self.sql_select_Query, (self.itemx,))

        while TRUE:

            row = self.cursor.fetchone()

            self.tree.insert('', END, values=row)
        
        self.con.close()    

    def return_window(self, args):

        #Função para fechar a janela atual e retornar para a janela anterior

        if args == 1:

            self.payment.destroy()

            self.sales()

    def pay(self):

        #Tela de formas de pagamento

        self.payment = Tk()
        self.payment.title('Americanas')
        self.payment.geometry('550x450')
        self.payment.resizable(False, False)

        self.paymLabel = Label(self.payment, text='Escolha a forma de pagamento: ').grid(sticky=NW, padx= 25, pady=20, column=0, row=1)
        self.paymon = Label(self.payment, text='Insira o valor do pagamento em dinheiro').grid(sticky=NW, padx= 290, pady=20, column=0, row=1)

        #Combobox para escolher formas de pagamento e quantidade de vezes caso seja crédito

        self.comb = ttk.Combobox(self.payment, values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], width= 5)
        self.comb.grid(sticky=W, padx= 25, pady=60, column=0, row=1)
        self.comb.current(0)

        self.comb1 = ttk.Combobox(self.payment, values=['Dinheiro', 'Débito', 'Crédito', 'Desconto'])
        self.comb1.grid(sticky=W, padx= 100, pady= 10, column=0, row=1)
        self.comb1.current(0)

        self.valor = Entry(self.payment)
        self.valor.grid(sticky=W, padx= 290, pady=10, row=1, column=0)

        self.callback1

        self.ret = Button(self.payment, text='Voltar', command= lambda:self.return_window(1), height=2, width=15).place(x=380, y= 350)
        self.finalizar = Button(self.payment, text='Finalizar', command= self.final, height=2, width=15).place(x=380, y= 250)
        self.ret = Button(self.payment, text='Confirmar', command= self.payfinal, height=2, width=15).place(x=380, y= 150)

        self.lb_pay = LabelFrame(self.payment, text="Pagamento")
        self.lb_pay.place(x=30, y=100, width=300, height=300)

        self.comb1.bind("<<ComboboxSelected>>", self.callback1)
        
        self.payment.mainloop()        

    def callback1(self, event):    

        self.paym = self.comb.get()

        self.paym1 = self.comb1.get()

    def payfinal(self):

        self.payment = Tk()
        self.payment.title('Americanas')
        self.payment.geometry('550x450')
        self.payment.resizable(False, False)

        self.lb_pay = LabelFrame(self.payment, text="Pagamento")
        self.lb_pay.place(x=30, y=100, width=300, height=300)

        self.list_children = self.tree.get_children()
        self.Citem = len(self.list_children)
        self.lbp = Label(self.lb_pay, text= "Total de itens: {}\n".format(self.Citem))
        self.lbp.pack()

        #Captura apenas da coluna de preços da Treeview para somar os valores e alimentar os ifs da forma de pagamento

        for child_item in self.list_children:
            
            tot = self.tree.item(child_item)['values'][3]


        #A separação também foi usada para capturar apenas os valores dos itens, multiplicar pelo total de produtos e mostrar o valor total 
   
        self.total = float(tot) * float(self.Citem)
        lb3 = Label(self.lb_pay, text= "Total: {}".format(self.total))
        lb3.pack()

        self.paym
        self.paym1

        print(self.paym)
        print(self.paym1)

        #Regras das formas de pagamento, com descontos, juros e exibição dos valores pra cada e exibição da quantidade de parcelas

        if self.paym1 == 'Dinheiro':

            self.paymoney = (self.total - (self.total*10/100))
            self.troco = float(self.valor.get()) - self.paymoney

            moneylb = Label(self.lb_pay, text= f'Sua compra de R${self.total:.2f} irá custar R${self.paymoney:.2f}\n em dinheiro\
e o troco será R${self.troco:.2f}') 
            moneylb.pack()

        elif self.paym1 == 'Débito':
             self.paydeb = self.total - (self.total*10/100)

             moneylb1 = Label(self.lb_pay, text= f'Sua compra de R${self.total:.2f} irá custar R${self.paydeb:.2f}\n no débito em {self.paym} vez(es)') 
             moneylb1.pack()   

            #Até 3 vezes não possui juros

        elif self.paym1 == 'Crédito' and int(self.paym) <= 3:
            paycred = (self.total) 

            moneylb = Label(self.lb_pay, text= f'Sua compra de R${self.total:.2f} irá custar R${paycred:.2f}\n no crédito em {self.paym} vez(es)') 
            moneylb.pack()

        elif self.paym1 == 'Crédito' and int(self.paym) >= 4:
            paycred2 = self.total + (self.total*20/100)

            moneylb = Label(self.lb_pay, text= f'Sua compra de R${self.total:.2f} irá custar R${paycred2:.2f}\n com 20% de juros no crédito em {self.paym} vezes')            
            moneylb.pack()       

        self.payment.mainloop()     


    def final(self):

        #Tela de nota fiscal

        self.sale = Tk()
        self.sale.title('Americanas')
        self.sale.geometry('550x450')
        self.sale.resizable(False, False)

        lb_nf = LabelFrame(self.sale, text="Nota Fiscal", borderwidth=1, relief='solid')
        lb_nf.place(x=30, y=10, width=400, height=400)

        #Método get_children para capturar dados de dentro da Treeview e método len para trazer a quantidade total

        list_children = self.tree.get_children()
        Citem = len(list_children)
        lb1 = Label(lb_nf, text= "Total de itens: {}\n".format(Citem))

        #Dentro do for separei cada item da lista para inserir no Label todos os produtos que o cliente quiser comprar
       
        for child_item in list_children:
            
            id = self.tree.item(child_item)['values'][0]
            nam = self.tree.item(child_item)['values'][1]
            typ = self.tree.item(child_item)['values'][2]
            val = self.tree.item(child_item)['values'][3]
            lb2 = Label(lb_nf, text= "Item: {} - {} - {} - {}".format(id, nam, typ, val))
            lb1.pack()
            lb2.pack()
            tot = self.tree.item(child_item)['values'][3]

        #A separação também foi usada para capturar apenas os valores dos itens, multiplicar pelo total de produtos e mostrar o valor total    
            
        total = float(tot) * float(Citem)
        lb3 = Label(lb_nf, text= "Total: {}".format(total))
        lb3.pack()
    
        self.sale.mainloop()     

Main().start()