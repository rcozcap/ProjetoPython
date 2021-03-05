from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
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
from datetime import date, timedelta


class Main():

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.log.destroy()
            self.main.destroy()
            self.sale.destroy()
            self.payment.destroy()
            self.payment1.destroy()
            self.sale1.destroy()

    def login(self):

        self.log = Tk()
        self.log.title('Loja')
        self.log.geometry('300x300')
        self.log.resizable(False, False)

        self.email = Label(self.log, text='LOGIN',
                           padx=4, pady=30, font=('Helvetica', 18, 'bold')).place(x=110, y=30)
        self.em = Entry(self.log)
        self.em.place(x=15, y=130)
        self.em.insert(0, 'Digite o seu e-mail...')
        self.em.bind('<FocusIn>', self.on_entry_click)
        self.em.bind('<FocusOut>', self.on_focusout)
        self.em.config(fg='grey')
        self.passwrd = Entry(self.log)
        self.passwrd.place(x=160, y=130)
        self.passwrd.insert(0, 'Digite a sua senha...')
        self.passwrd.bind('<FocusIn>', self.on_entry_click1)
        self.passwrd.bind('<FocusOut>', self.on_focusout)
        self.passwrd.config(fg='grey')
        self.signin = Button(self.log, text='Entrar',
                             command=self.passw, height=2, width=15).place(x=105, y=190)

        self.log.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log.mainloop()

    def on_entry_click(self, event):

        if self.em.get() == 'Digite o seu e-mail...':
            self.em.delete(0, "end")  # deleta tudo no campo
            self.em.insert(0, '')  # insere campo em branco
            self.em.config(fg='black')

    def on_entry_click1(self, event):

        if self.passwrd.get() == 'Digite a sua senha...':
            self.passwrd.delete(0, "end")  # deleta tudo no campo
            self.passwrd.insert(0, '')  # insere campo em branco
            self.passwrd.config(fg='black')
            self.passwrd.config(show='*')

    def on_focusout(self, event):
        if self.em.get() == '':
            self.em.insert(0, 'Digite o seu e-mail...')
            self.em.config(fg='grey')

        if self.passwrd.get() == '':
            self.passwrd.insert(0, 'Digite a sua senha...')
            self.passwrd.config(fg='grey')
            self.passwrd.config(show='')

    def passw(self):

        logList = []

        # Conexão com o banco de dados
        # Como o Id é o mesmo que o inserido no banco de dados esse parâmetro é capturado aqui

        self.catch = self.em.get()
        self.catchpass = self.passwrd.get()

        self.con = MySQLdb.connect(
            host='localhost', user='developer', passwd='Senha do Banco de Dados', db='shop')

        self.cursor = self.con.cursor()

        # E depois passado como parte do comando SQL no where para trazer o produto selecionado

        self.sql_select_Query = """Select * from passwords Where EmpEmail = %s AND EmpPassword = %s"""

        self.cursor.execute(self.sql_select_Query,
                            (self.catch, self.catchpass, ))

        row = self.cursor.fetchall()

        for row in row:

            logListAdmn = ['ADM', 'Gerente', 'Supervisor', 'Diretor', 'Sócio']

            logListUser = ['Convidado', 'Analista', 'Caixa']

            if row[0] == self.catch and row[1] == self.catchpass and row[2] in logListAdmn:

                self.start()
            elif row[0] == self.catch and row[1] == self.catchpass and row[2] in logListUser:

                self.start1()

        self.con.close()

    def start(self):

        # Tela principal
        self.log.withdraw()
        self.main = Tk()
        self.main.title('Loja')
        self.main.geometry('500x450')
        self.main.resizable(False, False)

        # Criando a barra de menu

        menubar = Menu(self.main)
        self.main.config(menu=menubar)

        filemenu = Menu(menubar)
        filemenu1 = Menu(menubar)
        filemenu2 = Menu(menubar)

        menubar.add_cascade(label='Menu', menu=filemenu)
        menubar.add_cascade(label='Vendas', menu=filemenu1)
        menubar.add_cascade(label='Notas Fiscais', menu=filemenu2)

        filemenu.add_command(label='Editar')
        filemenu1.add_command(label='Novo', command=self.sales)
        filemenu2.add_command(label='Balanço do dia', command=self.invoices)

        self.main.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main.mainloop()

    def start1(self):

        # Tela principal
        self.log.withdraw()
        self.main = Tk()
        self.main.title('Loja')
        self.main.geometry('500x450')
        self.main.resizable(False, False)

        # Criando a barra de menu

        menubar = Menu(self.main)
        self.main.config(menu=menubar)

        filemenu = Menu(menubar)
        filemenu1 = Menu(menubar)
        filemenu2 = Menu(menubar)

        menubar.add_cascade(label='Menu', menu=filemenu)
        menubar.add_cascade(label='Vendas', menu=filemenu1)
        menubar.add_cascade(label='Notas Fiscais', menu=filemenu2)

        filemenu.add_command(label='Editar', state=DISABLED)
        filemenu1.add_command(label='Novo', command=self.sales)
        filemenu2.add_command(label='Balanço do dia',
                              command=self.invoices, state=DISABLED)

        self.main.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main.mainloop()

    def sales(self):

        # Tela de inserção de produtos
        self.main.withdraw()
        self.sale = Tk()
        self.sale.title('Loja')
        self.sale.geometry('570x450')
        self.sale.resizable(False, False)

        self.insert = Label(self.sale, text='Insira o código do item: ',
                            padx=2, pady=30).grid(row=2, column=0)
        self.item = Entry(self.sale)
        self.item.grid(row=2, column=1)
        self.addprod = Button(self.sale, text='Adicionar Produto',
                              command=self.add, height=2, width=15).grid(row=2, column=2, padx=20)
        self.paymbutton = Button(self.sale, text='Escolher Forma de Pagamento',
                                 command=self.pay, height=2, width=25).grid(row=4, column=2, pady=20, rowspan=4)
        self.backmain = Button(self.sale, text='Voltar', command=lambda: self.return_window_add(
            1), height=2, width=25).grid(row=4, column=1, rowspan=4)

        # Treeview
        # Definimos os detalhes da Treeview, colunas, tamanho delas e os nomes(headings) que vão receber

        self.tree = ttk.Treeview(self.sale, selectmode='browse', columns=(
            'column1', 'column2', 'column3', 'column4'), show='headings')

        self.tree.column('column1', width=50, minwidth=50, stretch=NO)
        self.tree.heading('#1', text='ID')

        self.tree.column('column2', width=200, minwidth=50, stretch=NO)
        self.tree.heading('#2', text='NOME')

        self.tree.column('column3', width=200, minwidth=50, stretch=NO)
        self.tree.heading('#3', text='CATEGORIA')

        self.tree.column('column4', width=100, minwidth=50, stretch=NO)
        self.tree.heading('#4', text='PREÇO')

        # Definição de onde a Treeview vai se posicionar na tela

        self.tree.grid(row=3, column=0, columnspan=3)

        # Definindo o scroll

        vsb = ttk.Scrollbar(self.sale, orient="vertical",
                            command=self.tree.yview)
        vsb.place(x=350+200+2, y=77, height=180+50)

        self.sale.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.sale.mainloop()

    def return_window_add(self, args):

        # Função para fechar a janela atual e retornar para a janela anterior

        if args == 1:

            self.sale.withdraw()
            self.main.deiconify()

    def return_window_inv(self, args):

        # Função para fechar a janela atual e retornar para a janela anterior

        if args == 1:

            self.inv.destroy()
            self.main.deiconify()

    def invoices(self):

        self.main.withdraw()
        self.inv = Tk()
        style = ttk.Style(self.inv)
        self.inv.title('Loja')
        self.inv.geometry('950x570')
        self.inv.resizable(False, False)

        style.configure('Treeview', rowheight=70)

        self.week1 = Button(self.inv, text='Mostrar relatório semanal',
                            command=self.week, height=2, width=25).place(x=750, y=100)

        self.month1 = Button(self.inv, text='Mostrar relatório mensal',
                             command=self.month, height=2, width=25).place(x=750, y=150)

        self.show = Button(self.inv, text='Exibir nota fiscal',
                           command=self.catch1, height=2, width=25).place(x=750, y=200)

        self.back1 = Button(self.inv, text='Voltar', command=lambda: self.return_window_inv(
            1), height=2, width=25).place(x=750, y=250)

        self.treeInv = ttk.Treeview(self.inv, selectmode='browse', columns=(
            'column1', 'column2', 'column3', 'column4', 'column5'), show='headings', style='MyStyle1.Treeview')

        vsb = ttk.Scrollbar(self.inv, orient="vertical",
                            command=self.treeInv.yview)
        vsb.place(x=500+200+2, y=50, height=500+20)

        self.treeInv.configure(yscrollcommand=vsb.set)

        self.treeInv.column('column1', width=50, minwidth=50, stretch=TRUE)
        self.treeInv.heading('#1', text='ID')

        self.treeInv.column('column2', width=300, minwidth=150, stretch=TRUE)
        self.treeInv.heading('#2', text='NOTA FISCAL')

        self.treeInv.column('column3', width=70, minwidth=50, stretch=TRUE)
        self.treeInv.heading('#3', text='DATA')

        self.treeInv.column('column4', width=100, minwidth=50, stretch=TRUE)
        self.treeInv.heading('#4', text='NOME')

        self.treeInv.column('column5', width=150, minwidth=50, stretch=TRUE)
        self.treeInv.heading('#5', text='E-MAIL')

        self.treeInv.place(x=50, y=50)

        lastWeek = date.today() - timedelta(days=7)
        lastMonth = date.today() - timedelta(days=30)

        self.con = MySQLdb.connect(
            host='localhost', user='developer', passwd='Senha do Banco de Dados', db='shop')

        self.cursor = self.con.cursor()

        self.sql_select_Query = """Select * from notafiscal Where CustData CURRENT_DATE()"""

        self.cursor.execute(self.sql_select_Query)

        row = self.cursor.fetchall()

        for row in row:

            self.treeInv.insert('', END, values=row)

        self.con.close()

        self.inv.mainloop()

    def catch1(self):

        Item = self.treeInv.selection()
        val = self.treeInv.item(Item, "values")

        self.inv1 = Tk()
        self.inv1.title('Loja')
        self.inv1.geometry('500x600')

        self.lb_inv = LabelFrame(
            self.inv1, text="Nota Fiscal", borderwidth=1, relief='solid', bg="white")
        self.lb_inv.place(x=30, y=10, width=440, height=540)

        lb_inv = Label(self.lb_inv, text=val[1])
        lb_inv.place(x=30, y=30)

        self.inv1.mainloop()

    def week(self):

        self.treeInv.delete(*self.treeInv.get_children())

        self.con = MySQLdb.connect(
            host='localhost', user='developer', passwd='Senha do Banco de Dados', db='shop')

        self.cursor = self.con.cursor()

        self.sql_select_Query = """Select * from notafiscal Where CustData BETWEEN CURRENT_DATE()-7 AND CURRENT_DATE()"""

        self.cursor.execute(self.sql_select_Query)

        row = self.cursor.fetchall()

        for row in row:

            self.treeInv.insert('', END, values=row)

        self.con.close()

    def month(self):

        self.treeInv.delete(*self.treeInv.get_children())

        self.con = MySQLdb.connect(
            host='localhost', user='developer', passwd='Senha do Banco de Dados', db='shop')

        self.cursor = self.con.cursor()

        self.sql_select_Query = """Select * from notafiscal Where CustData BETWEEN CURRENT_DATE()-90 AND CURRENT_DATE()"""

        self.cursor.execute(self.sql_select_Query)

        row = self.cursor.fetchall()

        for row in row:

            self.treeInv.insert('', END, values=row)

        self.con.close()

    def add(self):

        # Conexão com o banco de dados
        # Como o Id é o mesmo que o inserido no banco de dados esse parâmetro é capturado aqui

        self.itemx = int(self.item.get())

        self.con = MySQLdb.connect(
            host='localhost', user='developer', passwd='Senha do Banco de Dados', db='shop')

        self.cursor = self.con.cursor()

        # E depois passado como parte do comando SQL no where para trazer o produto selecionado

        self.sql_select_Query = """Select * from products Where ProdId = %s"""

        self.cursor.execute(self.sql_select_Query, (self.itemx,))

        while TRUE:

            row = self.cursor.fetchone()

            self.tree.insert('', END, values=row)

        self.con.close()

    def return_window_pay(self, args):

        # Função para retornar para a janela anterior

        if args == 1:
            # fechar janela atual
            self.payment.withdraw()
            # Voltar a mostrar janela oculta
            self.sale.deiconify()

    def pay(self):

        # Tela de formas de pagamento
        # Ocultar janela anterior
        self.sale.withdraw()
        self.payment = Tk()
        self.payment.title('Loja')
        self.payment.geometry('550x450')
        self.payment.resizable(False, False)

        self.paymLabel = Label(self.payment, text='Escolha a forma de pagamento: ').grid(
            sticky=NW, padx=25, pady=20, column=0, row=1)
        self.paymon = Label(self.payment, text='Insira o valor do pagamento em dinheiro').grid(
            sticky=NW, padx=290, pady=20, column=0, row=1)

        # Combobox para escolher formas de pagamento e quantidade de vezes caso seja crédito

        self.comb = ttk.Combobox(self.payment, values=[
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], width=5)
        self.comb.grid(sticky=W, padx=25, pady=60, column=0, row=1)
        self.comb.current(0)

        self.comb1 = ttk.Combobox(self.payment, values=[
            'Dinheiro', 'Débito', 'Crédito', 'Desconto'])
        self.comb1.grid(sticky=W, padx=100, pady=10, column=0, row=1)
        self.comb1.current(0)

        self.valor = Entry(self.payment)
        self.valor.grid(sticky=W, padx=290, pady=10, row=1, column=0)

        self.callback1

        self.ret = Button(self.payment, text='Voltar', command=lambda: self.return_window_pay(
            1), height=2, width=15).place(x=380, y=350)
        self.ret = Button(self.payment, text='Confirmar',
                          command=self.payfinal, height=2, width=15).place(x=380, y=150)

        self.lb_pay = LabelFrame(self.payment, text="Pagamento")
        self.lb_pay.place(x=30, y=100, width=300, height=300)

        self.comb1.bind("<<ComboboxSelected>>", self.callback1)

        self.payment.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.payment.mainloop()

    def callback1(self, event):

        # Recuperar dados da ComboBox

        self.paym = self.comb.get()

        self.paym1 = self.comb1.get()

    def return_window_payfinal(self, args):

        # Função para retornar para a janela anterior

        if args == 1:
            # fechar janela atual
            self.payment1.withdraw()
            # Voltar a mostrar janela oculta
            self.payment.deiconify()

    def payfinal(self):

        # Ocultar janela anterior
        self.payment.withdraw()
        self.payment1 = Tk()
        self.payment1.title('Loja')
        self.payment1.geometry('550x450')
        self.payment1.resizable(False, False)

        self.lb_pay = LabelFrame(self.payment1, text="Pagamento")
        self.lb_pay.place(x=30, y=100, width=300, height=300)

        self.finalizar = Button(self.payment1, text='Finalizar',
                                command=self.final, height=2, width=15).place(x=380, y=250)
        self.back = Button(self.payment1, text='Voltar',
                           command=lambda: self.return_window_payfinal(1), height=2, width=15)
        self.back.place(x=380, y=330)

        self.payment1.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.list_children = self.tree.get_children()
        self.Citem = len(self.list_children)
        self.lbp = Label(
            self.lb_pay, text="Total de itens: {}\n".format(self.Citem))
        self.lbp.pack()

        # Captura apenas da coluna de preços da Treeview para somar os valores e alimentar os ifs da forma de pagamento

        plist = []

        for child_item in self.list_children:

            p = float(self.tree.item(child_item)['values'][3].split()[0])
            plist.append(p)

        tot2 = sum(plist)

        # A separação também foi usada para capturar apenas os valores dos itens, multiplicar pelo total de produtos e mostrar o valor total

        self.total = tot2
        lb3 = Label(self.lb_pay, text="Total: {}".format(self.total))
        lb3.pack()

        self.paym
        self.paym1

        # Regras das formas de pagamento, com descontos, juros e exibição dos valores pra cada e exibição da quantidade de parcelas

        if self.paym1 == 'Dinheiro':

            # Pagamentos em débiro ou dinheiro possuem desconto

            self.paymoney = (self.total - (self.total*10/100))
            self.troco = float(self.valor.get()) - self.paymoney

            moneylb = Label(self.lb_pay, text=f'Sua compra de R${self.total:.2f} irá custar R${self.paymoney:.2f}\n em dinheiro\
e o troco será R${self.troco:.2f}')
            moneylb.pack()

        elif self.paym1 == 'Débito':
            self.paydeb = self.total - (self.total*10/100)

            moneylb = Label(
                self.lb_pay, text=f'Sua compra de R${self.total:.2f} irá custar R${self.paydeb:.2f}\n no débito em {self.paym} vez(es)')
            moneylb.pack()

            # Até 3 vezes não possui juros

        elif self.paym1 == 'Crédito' and int(self.paym) <= 3:
            paycred = (self.total)

            moneylb = Label(
                self.lb_pay, text=f'Sua compra de R${self.total:.2f} irá custar R${paycred:.2f}\n no crédito em {self.paym} vez(es)')
            moneylb.pack()

            # Acima de 3 vezes o cliente paga com 20% de juros

        elif self.paym1 == 'Crédito' and int(self.paym) >= 4:
            paycred2 = self.total + (self.total*20/100)

            moneylb = Label(
                self.lb_pay, text=f'Sua compra de R${self.total:.2f} irá custar R${paycred2:.2f}\n com 20% de juros no crédito em {self.paym} vezes')
            moneylb.pack()

        self.payment1.mainloop()

        # Número da nota fiscal pega o last insert id do banco de dados (autoincrement) evitando gerar duplicidade

    def createPdf(self):
        notasend = []

        self.message1 = f'Olá prezado(a) {self.Nm.get()}\n\nConforme solicitado, segue abaixo os dados\n referentes a sua nota fiscal:\
\nProduto:\n {self.mmg}\n Valor Total da Compra: {self.total}\nForma de pagamento {self.paym1}\n{self.moneyLabel["text"]}\
\nObrigado pela preferência!!'

        # Separando mensagem em uma lista usando o "\n" como separador

        nota = self.message1.split("\n")
        for i in nota:
            notasend.append(i)
        cnv = canvas.Canvas(
            f'C:\\Users\\Ana\\Desktop\\E-mails_nf\\Nota_Fiscal.pdf')

        # Imprimindo cada posição da lista em sua ordem pra formar a nota fiscal

        cnv.drawString(220, 750, notasend[0])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 725, notasend[1])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 700, notasend[2])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 675, notasend[3])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 650, notasend[4])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 625, notasend[5])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 600, notasend[6])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 575, notasend[7])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 550, notasend[8])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 525, notasend[9])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 500, notasend[10])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.drawString(150, 475, notasend[11])
        cnv.setFont("Helvetica-Bold", 12)
        cnv.save()
        return 0

    def snd(self):
        # Configuração
        host = 'smtp-mail.outlook.com'
        port = 587
        user = 'seu email'
        password = 'sua senha'

        # Criando objeto
        self.lbmail = Label(self.sale, text=f'Conectando ao servidor....')
        self.lbmail.place(x=350, y=30)
        server = smtplib.SMTP(host, port)

        # Login com servidor
        self.lbmail2 = Label(self.sale, text=f'Fazendo login....')
        self.lbmail2.place(x=350, y=60)
        server.ehlo()
        server.starttls()
        server.login(user, password)

        # Criando mensagem
        self.message = f'Olá prezado(a) {self.Nm.get()}\n \nConforme solicitado, segue abaixo os dados referentes a sua nota fiscal\
\n\nProduto:\n {self.mmg}\n\nValor Total da Compra: {self.total}\n\nForma de pagamento {self.paym1}\n\n{self.moneyLabel["text"]}\
\n\nObrigado pela preferência!!'

        # Inserindo nota fiscal no banco de dados

        self.con = MySQLdb.connect(
            host='localhost', user='developer', passwd='Senha do Banco de Dados', db='shop')

        self.cursor = self.con.cursor()

        self.sql_select_Query = """Insert INTO notafiscal (CustId, CustInv, CustName, CustEmail) VALUES(NULL, %s, %s, %s)"""

        self.cursor.execute(self.sql_select_Query,
                            (self.message, self.Nm.get(), self.Em.get(),))

        self.con.commit()

        # Trazendo o último ID inserido no banco para usar como número da nota fiscal

        self.sql_select_Query1 = """SELECT LAST_INSERT_ID()"""

        self.cursor.execute(self.sql_select_Query1)

        self.idVl = self.cursor.fetchone()

        self.con.close()

        # Comando para o programa aguardar 1 segundo

        time.sleep(1)

        self.lbmail3 = Label(self.sale, text=f'Criando mensagem....')
        self.lbmail2.place(x=350, y=90)
        email_msg = MIMEMultipart()
        email_msg['From'] = user
        email_msg['To'] = self.Em.get()
        email_msg['Subject'] = f'Nota Fiscal {self.idVl}'
        self.lbmail4 = Label(self.sale, text=f'Adicionando texto....')
        self.lbmail2.place(x=350, y=120)
        email_msg.attach(MIMEText(self.message, 'plain'))

        # anexando arquivo pdf da nota fiscal

        pdfname = f'C:\\Users\\Ana\\Desktop\\E-mails_nf\\Nota_Fiscal.pdf'
        fp = open(pdfname, 'rb')
        anexo = MIMEApplication(fp.read(), _subtype="pdf")
        fp.close()
        anexo.add_header('Content-Disposition', 'attachment',
                         filename='Nota_Fiscal.pdf')
        email_msg.attach(anexo)

        # Enviando mensagem
        self.lbmail4 = Label(self.sale, text=f'Enviando mensagem....')
        self.lbmail2.place(x=350, y=150)
        server.sendmail(email_msg['From'],
                        email_msg['To'], email_msg.as_string())
        self.lbmail4 = Label(self.sale, text=f'Mensagem enviada....')
        self.lbmail2.place(x=350, y=180)
        server.quit()

    def print(self):

        # Função para impressão abrindo o arquivo para imprimir diretamente no software

        os.startfile(r"C:\\Users\\Ana\\Desktop\\E-mails_nf\\Nota_Fiscal.pdf")

    def return_window_final(self, args):

        # Função para retornar para a janela anterior

        if args == 1:
            # fechar janela atual
            self.sale1.withdraw()
            # Voltar a mostrar janela oculta
            self.payment1.deiconify()

    def another_sell(self, args):

        # Função para retornar para a janela anterior

        if args == 1:
            # fechar janela atual
            self.sale1.destroy()
            # Voltar a mostrar janela oculta
            self.sale.deiconify()

    def final(self):

        # Tela de nota fiscal

        self.payment1.withdraw()
        self.sale1 = Tk()
        self.sale1.title('Loja')
        self.sale1.geometry('550x450')
        self.sale1.resizable(False, False)

        self.lb_nf = LabelFrame(
            self.sale1, text="Nota Fiscal", borderwidth=1, relief='solid')
        self.lb_nf.place(x=30, y=10, width=300, height=400)
        self.prt = Button(self.sale1, text='Imprimir',
                          command=self.print, height=2, width=25).place(x=345, y=265)
        self.create = Button(self.sale1, text='Gerar pdf',
                             command=self.createPdf, height=2, width=25).place(x=345, y=170)
        self.send = Button(self.sale1, text='Enviar para o e-mail',
                           command=self.snd, height=2, width=25).place(x=345, y=220)
        self.bk = Button(self.sale1, text='Voltar', command=lambda: self.return_window_final(
            1), height=2, width=25).place(x=345, y=315)
        self.finish = Button(self.sale1, text='Encerrar e ir para a\n próxima venda',
                             command=lambda: self.another_sell(1), height=3, width=25).place(x=345, y=365)
        lbNm = Label(self.sale1, text=f'Digite o nome: ')
        lbNm.place(x=350, y=80)
        self.Nm = Entry(self.sale1)
        self.Nm.place(width=180, x=345, y=100)
        lbNe = Label(self.sale1, text=f'Digite o e-mail: ')
        lbNe.place(x=350, y=120)
        self.Em = Entry(self.sale1)
        self.Em.place(width=180, x=345, y=140)

        # Método get_children para capturar dados de dentro da Treeview e método len para trazer a quantidade total

        list_children = self.tree.get_children()
        Citem = len(list_children)
        lb1 = Label(self.lb_nf, text="Total de itens: {}\n".format(Citem))

        self.sale1.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Dentro do for separei cada item da lista para inserir no Label todos os produtos que o cliente quiser comprar

        plist_fin = []

        for child_item in list_children:

            self.id = self.tree.item(child_item)['values'][0]
            self.nam = self.tree.item(child_item)['values'][1]
            self.typ = self.tree.item(child_item)['values'][2]
            self.val = self.tree.item(child_item)['values'][3]
            self.lb2 = Label(
                self.lb_nf, text="Item: {} - {} - {} - {}".format(self.id, self.nam, self.typ, self.val))
            lb1.pack()
            self.lb2.pack()

            p = float(self.tree.item(child_item)['values'][3].split()[0])
            plist_fin.append(p)

        tot2 = sum(plist_fin)

        # A separação também foi usada para capturar apenas os valores dos itens, multiplicar pelo total de produtos e mostrar o valor total

        self.total = tot2
        lb3 = Label(self.lb_nf, text="Total: {}".format(self.total))
        lb3.pack()
        lb4 = Label(self.lb_nf, text=f'Forma de pagamento {self.paym1}')
        lb4.pack()

        if self.paym1 == 'Dinheiro':

            self.paymoney = (self.total - (self.total*10/100))
            self.troco = float(self.valor.get()) - self.paymoney

            self.moneyLabel = Label(self.lb_nf, text=f'Sua compra de R${self.total:.2f} foi paga\n no valor de R${self.paymoney:.2f}\n em dinheiro\
e o troco foi de R${self.troco:.2f}')
            self.moneyLabel.pack()

        elif self.paym1 == 'Débito':
            self.paydeb = self.total - (self.total*10/100)

            self.moneyLabel = Label(
                self.lb_nf, text=f'Sua compra de R${self.total:.2f} foi paga\n no valor de R${self.paydeb:.2f}\n no débito em {self.paym} vez(es)')
            self.moneyLabel.pack()

            # Até 3 vezes não possui juros

        elif self.paym1 == 'Crédito' and int(self.paym) <= 3:
            self.paycred = (self.total)

            self.moneyLabel = Label(
                self.lb_nf, text=f'Sua compra de R${self.total:.2f} foi paga\n no valor de R${self.paycred:.2f}\n no crédito em {self.paym} vez(es)')
            self.moneyLabel.pack()

        elif self.paym1 == 'Crédito' and int(self.paym) >= 4:
            self.paycred2 = self.total + (self.total*20/100)

            self.moneyLabel = Label(
                self.lb_nf, text=f'Sua compra de R${self.total:.2f} foi paga\n no valor de R${self.paycred2:.2f}\n com 20% de juros no crédito em {self.paym} vezes')
            self.moneyLabel.pack()

        self.someList = []

        for child_item in list_children:

            self.id = self.tree.item(child_item)['values'][0]
            self.nam = self.tree.item(child_item)['values'][1]
            self.typ = self.tree.item(child_item)['values'][2]
            self.val = self.tree.item(child_item)['values'][3]

            # Trazendo cada item da lista separado por quebra de linha para ser incluído na nota fiscal

            self.someList.append(
                f"{self.id} {self.nam} {self.typ} {self.val}")

        self.mmg = ', '.join(self.someList)
        self.mmg = self.mmg.replace(',', '\n')

        print(self.mmg)

        self.sale1.mainloop()


Main().login()
