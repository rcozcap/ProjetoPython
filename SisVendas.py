from tkinter import *
from tkinter import ttk
import pymysql as MySQLdb
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import messagebox
from reportlab.pdfgen import canvas, textobject
import webbrowser
import os
import time

class Main():
    
    def start(self):

        #Tela principal 

        self.main = Tk()
        self.main.title('Americanas')
        self.main.geometry('500x450')
        self.main.resizable(False, False)

        # Criando a barra de menu

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
        self.addprod = Button(self.sale, text='Adicionar Produto', command= self.add, height=2, width=15).grid(row=2, column=2, padx=20)
        self.paymbutton = Button(self.sale, text='Escolher Forma de Pagamento', command= self.pay, height=2, width=25).grid(row=4, column=2, pady=20, rowspan=4)
        self.backmain = Button(self.sale, text='Voltar', command= lambda:self.return_window_add(1), height=2, width=25).grid(row=4, column= 1, rowspan= 4)
        
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

    def return_window_add(self, args):

        #Função para fechar a janela atual e retornar para a janela anterior

        if args == 1:

            self.sale.destroy()

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

    def return_window_pay(self, args):

        #Função para retornar para a janela anterior

        if args == 1:

            self.payment.destroy()

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

        self.ret = Button(self.payment, text='Voltar', command= lambda:self.return_window_pay(1), height=2, width=15).place(x=380, y= 350)
        self.finalizar = Button(self.payment, text='Finalizar', command= self.final, height=2, width=15).place(x=380, y= 250)
        self.ret = Button(self.payment, text='Confirmar', command= self.payfinal, height=2, width=15).place(x=380, y= 150)

        self.lb_pay = LabelFrame(self.payment, text="Pagamento")
        self.lb_pay.place(x=30, y=100, width=300, height=300)

        self.comb1.bind("<<ComboboxSelected>>", self.callback1)
        
        self.payment.mainloop()        

    def callback1(self, event):    

        # Recuperar dados da ComboBox

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

        #Regras das formas de pagamento, com descontos, juros e exibição dos valores pra cada e exibição da quantidade de parcelas

        if self.paym1 == 'Dinheiro':

            # Pagamentos em débiro ou dinheiro possuem desconto

            self.paymoney = (self.total - (self.total*10/100))
            self.troco = float(self.valor.get()) - self.paymoney

            moneylb = Label(self.lb_pay, text= f'Sua compra de R${self.total:.2f} irá custar R${self.paymoney:.2f}\n em dinheiro\
e o troco será R${self.troco:.2f}') 
            moneylb.pack()

        elif self.paym1 == 'Débito':
             self.paydeb = self.total - (self.total*10/100)

             moneylb = Label(self.lb_pay, text= f'Sua compra de R${self.total:.2f} irá custar R${self.paydeb:.2f}\n no débito em {self.paym} vez(es)') 
             moneylb.pack()   

            # Até 3 vezes não possui juros

        elif self.paym1 == 'Crédito' and int(self.paym) <= 3:
            paycred = (self.total) 

            moneylb = Label(self.lb_pay, text= f'Sua compra de R${self.total:.2f} irá custar R${paycred:.2f}\n no crédito em {self.paym} vez(es)') 
            moneylb.pack()

            # Acima de 3 vezes o cliente paga com 20% de juros

        elif self.paym1 == 'Crédito' and int(self.paym) >= 4:
            paycred2 = self.total + (self.total*20/100)

            moneylb = Label(self.lb_pay, text= f'Sua compra de R${self.total:.2f} irá custar R${paycred2:.2f}\n com 20% de juros no crédito em {self.paym} vezes')            
            moneylb.pack()       

        self.payment.mainloop()     

        #Número da nota fiscal pega o last insert id do banco de dados (autoincrement) evitando gerar duplicidade

    def createPdf(self):
        notasend = []

        self.message = f'Olá prezado(a) {self.Nm.get()}\n\nConforme solicitado, segue abaixo os dados\n referentes a sua nota fiscal:\
\nProduto: {self.mmg}\nValor Total da Compra: {self.total}\nForma de pagamento {self.paym1}\n{self.moneyLabel["text"]}\
\nObrigado pela preferência!!'

        # Separando mensagem em uma lista usando o "\n" como separador

        nota = self.message.split("\n")
        for i in nota:
            notasend.append(i)
        cnv = canvas.Canvas(f'C:\\Users\\Ana\\Desktop\\E-mails_nf\\Nota_Fiscal.pdf')

        # Imprimindo cada posição da lista em sua ordem pra formar a nota fiscal

        cnv.drawString(220,750, notasend[0])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150,725, notasend[1])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150,700, notasend[2])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150,675, notasend[3])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150,650, notasend[4])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150,625, notasend[5])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150,600, notasend[6])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.save()
        return 0    

    def snd(self):
        # Configuração
        host = 'smtp-mail.outlook.com'
        port = 587
        user = 'seu e-mail'
        password = 'sua senha'

        # Criando objeto
        self.lbmail = Label(self.sale, text= f'Conectando ao servidor....')
        self.lbmail.place(x=350, y=30)
        server = smtplib.SMTP(host, port)

        # Login com servidor
        self.lbmail2 = Label(self.sale, text= f'Fazendo login....')
        self.lbmail2.place(x=350, y=60)
        server.ehlo()
        server.starttls()
        server.login(user, password)

        # Criando mensagem
        self.message = f'Olá prezado(a) {self.Nm.get()}\n \nConforme solicitado, segue abaixo os dados referentes a sua nota fiscal\
\n\nProduto: {self.mmg}\n\nValor Total da Compra: {self.total}\n\nForma de pagamento {self.paym1}\n\n{self.moneyLabel["text"]}\
\n\nObrigado pela preferência!!'

        # Inserindo nota fiscal no banco de dados

        self.con = MySQLdb.connect(host='localhost', user='developer', passwd='1234567', db='shop')

        self.cursor = self.con.cursor()

        self.sql_select_Query = """Insert INTO notaFiscal (CustId, CustInv, CustName, CustEmail) VALUES(NULL, %s, %s, %s)"""

        self.cursor.execute(self.sql_select_Query, (self.message, self.Nm.get(), self.Em.get(),))

        self.con.commit()

        # Trazendo o último ID inserido no banco para usar como número da nota fiscal
        
        self.sql_select_Query1 = """SELECT LAST_INSERT_ID()"""

        self.cursor.execute(self.sql_select_Query1)

        self.idVl = self.cursor.fetchone() 

        self.con.close()

        # Comando para o programa aguardar 1 segundo

        time.sleep(1)

        self.lbmail3 = Label(self.sale, text= f'Criando mensagem....')
        self.lbmail2.place(x=350, y=90)
        email_msg = MIMEMultipart()
        email_msg['From'] = user
        email_msg['To'] = self.Em.get()
        email_msg['Subject'] = f'Nota Fiscal {self.idVl}'
        self.lbmail4 = Label(self.sale, text= f'Adicionando texto....')
        self.lbmail2.place(x=350, y=120)
        email_msg.attach(MIMEText(self.message, 'plain'))

        # anexando arquivo pdf da nota fiscal

        pdfname=f'C:\\Users\\Ana\\Desktop\\E-mails_nf\\Nota_Fiscal.pdf'
        fp=open(pdfname,'rb')
        anexo = MIMEApplication(fp.read(), _subtype="pdf")
        fp.close()
        anexo.add_header('Content-Disposition','attachment',filename='Nota_Fiscal.pdf')
        email_msg.attach(anexo)

        # Enviando mensagem
        self.lbmail4 = Label(self.sale, text= f'Enviando mensagem....')
        self.lbmail2.place(x=350, y=150)
        server.sendmail(email_msg['From'], email_msg['To'],email_msg.as_string())
        self.lbmail4 = Label(self.sale, text= f'Mensagem enviada....')
        self.lbmail2.place(x=350, y=180)
        server.quit()

    def print(self):

        # Função para impressão abrindo o arquivo para imprimir diretamente no software

        os.system(r"C:\\Users\\Ana\\Desktop\\E-mails_nf\\Nota_Fiscal.pdf")      

    def final(self):

        #Tela de nota fiscal

        self.sale1 = Tk()
        self.sale1.title('Americanas')
        self.sale1.geometry('550x450')
        self.sale1.resizable(False, False)

        self.lb_nf = LabelFrame(self.sale1, text="Nota Fiscal", borderwidth=1, relief='solid')
        self.lb_nf.place(x=30, y=10, width=300, height=400)
        self.prt = Button(self.sale1, text='Imprimir', command= self.print, height=2, width=15).place(x=380, y= 350)
        self.create = Button(self.sale1, text='Gerar pdf', command= self.createPdf, height=2, width=15).place(x=380, y= 258)
        self.send = Button(self.sale1, text='Enviar para o e-mail', command= self.snd, height=2, width=25).place(x=345, y= 305)
        lbNm = Label(self.sale1, text= f'Digite o nome: ')
        lbNm.place(x=350, y=170)
        self.Nm = Entry(self.sale1)
        self.Nm.place(width= 180, x=345, y=190)
        lbNe = Label(self.sale1, text= f'Digite o e-mail: ')
        lbNe.place(x=350, y=210)
        self.Em = Entry(self.sale1)
        self.Em.place(width= 180, x=345, y=230)

        #Método get_children para capturar dados de dentro da Treeview e método len para trazer a quantidade total

        list_children = self.tree.get_children()
        Citem = len(list_children)
        lb1 = Label(self.lb_nf, text= "Total de itens: {}\n".format(Citem))


        #Dentro do for separei cada item da lista para inserir no Label todos os produtos que o cliente quiser comprar
       
        for child_item in list_children:
            
            self.id = self.tree.item(child_item)['values'][0]
            self.nam = self.tree.item(child_item)['values'][1]
            self.typ = self.tree.item(child_item)['values'][2]
            self.val = self.tree.item(child_item)['values'][3]
            self.lb2 = Label(self.lb_nf, text= "Item: {} - {} - {} - {}".format(self.id, self.nam, self.typ, self.val))
            lb1.pack()
            self.lb2.pack()
            tot = self.tree.item(child_item)['values'][3]

        #A separação também foi usada para capturar apenas os valores dos itens, multiplicar pelo total de produtos e mostrar o valor total    

        self.total = float(tot) * float(Citem)
        lb3 = Label(self.lb_nf, text= "Total: {}".format(self.total))
        lb3.pack()
        lb4 = Label(self.lb_nf, text= f'Forma de pagamento {self.paym1}')
        lb4.pack()

        if self.paym1 == 'Dinheiro':

            self.paymoney = (self.total - (self.total*10/100))
            self.troco = float(self.valor.get()) - self.paymoney

            self.moneyLabel = Label(self.lb_nf, text= f'Sua compra de R${self.total:.2f} foi paga\n no valor de R${self.paymoney:.2f}\n em dinheiro\
e o troco foi de R${self.troco:.2f}') 
            self.moneyLabel.pack()

        elif self.paym1 == 'Débito':
            self.paydeb = self.total - (self.total*10/100)

            self.moneyLabel = Label(self.lb_nf, text= f'Sua compra de R${self.total:.2f} foi paga\n no valor de R${self.paydeb:.2f}\n no débito em {self.paym} vez(es)') 
            self.moneyLabel.pack()   

            #Até 3 vezes não possui juros

        elif self.paym1 == 'Crédito' and int(self.paym) <= 3:
            self.paycred = (self.total) 

            self.moneyLabel = Label(self.lb_nf, text= f'Sua compra de R${self.total:.2f} foi paga\n no valor de R${self.paycred:.2f}\n no crédito em {self.paym} vez(es)') 
            self.moneyLabel.pack()

        elif self.paym1 == 'Crédito' and int(self.paym) >= 4:
            self.paycred2 = self.total + (self.total*20/100)

            self.moneyLabel = Label(self.lb_nf, text= f'Sua compra de R${self.total:.2f} foi paga\n no valor de R${self.paycred2:.2f}\n com 20% de juros no crédito em {self.paym} vezes')            
            self.moneyLabel.pack()

        for child_item in list_children:

            self.someList = []
            
            self.id = self.tree.item(child_item)['values'][0]
            self.nam = self.tree.item(child_item)['values'][1]
            self.typ = self.tree.item(child_item)['values'][2]
            self.val = self.tree.item(child_item)['values'][3]

            # Trazendo cada item da lista separado por quebra de linha para ser incluído na nota fiscal

            for child_item in list_children:

                self.someList.append(f"{self.id} {self.nam} {self.typ} {self.val}")

        self.mmg = ', '.join(self.someList)
        self.mmg = self.mmg.replace(',','\n')
       
        self.sale1.mainloop()     

Main().start()