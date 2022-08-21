from pydoc import text
from tkinter import *
from typing import TextIO
import sqlite3

#Conectar ao banco sqlite3
conn = sqlite3.connect('usuarios.db')
acesso = conn.cursor()

acesso.execute('''
CREATE TABLE IF NOT EXISTS usuario(
    nome TEXT NOT NULL,
    imc TEXT NOT NULL,
    msg TEXT NOT NULL
)
''')

class Cal_imc:
    def __init__(self):
        self.window = Tk()
        self.window.title('Calcular IMC')
        self.window.geometry("400x430")
        self.window.resizable(0,0)

        self.tela1 = Frame(self.window, width=400, height=300)
        self.tela1.pack()
        self.tela2 = Frame(self.window, width=400, height=100)
        self.tela2.pack()
        #nome, peso e altura --> tela1
        self.nome = Label(self.tela1, text='Nome:', font=('Ivy 20'), fg="red").grid(row='0', column='0')
        self.telaNome = Entry(self.tela1, font="likhan 40", bg="#696969", fg="black", width=10)
        self.telaNome.grid(row="0", column="1")

        self.peso = Label(self.tela1, text='Peso:', font=('Ivy 20'), fg="red").grid(row='1', column='0')
        self.telaPeso = Entry(self.tela1, font="likhan 40", bg="#696969", fg="black", width=10)
        self.telaPeso.grid(row="1", column="1")

        self.altura = Label(self.tela1, text='Altura:', font=('Ivy 20'), fg="red").grid(row='2', column='0')
        self.telaAltura = Entry(self.tela1, font="likhan 40", bg="#696969", fg="black", width=10)
        self.telaAltura.grid(row="2", column="1")

        #tela2 --> botão e textoResult
        self.botaoOk = Button(self.tela2, bg="#3fb5a3", bd=6, text="OK", font='arial 12 bold', fg="red", width=14, height=1, command=lambda:self.bot())
        self.botaoOk.grid(row="0", column="0", columnspan='2')

        self.botaoLimpar = Button(self.tela2, bg="#3fb5a3", bd=6, text="Cancelar", font='arial 12 bold', fg="red", width=14, height=1, command=lambda:self.limparInfo())
        self.botaoLimpar.grid(row="0", column="2", columnspan='2')

        self.linha = Label(self.window, text='', width=25, bg="#1cf", font=('Ivy 20'))
        self.linha.pack()
        self.linha2 = Label(self.window, text='', width=25, bg="#1cf", font=('Ivy 20'))
        self.linha2.pack()
        self.linha3 = Label(self.window, text='', width=25, bg="#1cf", font=('Ivy 20'))
        self.linha3.pack()

        self.botaoSalvar = Button(self.window, bg="#3fb5a3", bd=6, text="Salvar", font='arial 12 bold', fg="red", width=14, height=1, command=lambda:self.salvar())
        self.botaoSalvar.pack()
        self.botaoHistorico = Button(self.window, bg="#3fb5a3", bd=6, text="Histórico", font='arial 12 bold', fg="red", width=14, height=1, command=lambda:self.listar())
        self.botaoHistorico.pack()


        self.window.mainloop()
    

    def limparInfo(self):
        self.telaAltura.delete(0, END)
        self.telaPeso.delete(0, END)
        self.telaNome.delete(0, END)
        self.linha.configure(text='')

    def bot(self):
        peso = eval(self.telaPeso.get())
        altura = eval(self.telaAltura.get())
        imc = peso / altura **2
        self.nome = self.telaNome.get()
        if imc < 16:
            msg = 'Magreza grave'
        elif imc < 17:
            msg = 'Magreza moderada'
        elif imc < 18.5:
            msg = 'Magreza leve'
        elif imc < 25:
            msg = 'Saudável'
        elif imc < 30:
            msg = 'Sobrepeso'
        elif imc < 35:
            msg = 'Obesidade Grau I'
        elif imc < 40:
            msg = 'Obesidade Grau II'
        else:
            msg = 'Obesidade Grau III'
        
        self.msg = msg
        self.imc = imc
        print(self.imc, msg, self.nome)
        self.linha.configure(text=self.nome)
        self.linha2.configure(text=('imc = ', int(self.imc)))
        self.linha3.configure(text=msg)


    def salvar(self):
        acesso.execute(f'''
            INSERT INTO usuario(nome, imc, msg)
            VALUES ('{self.nome}','{self.imc}','{self.msg}')
        ''')
        conn.commit()#guardar informações no banco de dados


    def listar(self):
        self.window2 = Tk()
        self.window2.title('Calcular IMC')
        self.window2.geometry("500x430")
        self.window2.resizable(0,0)

        acesso.execute('''
        SELECT nome, imc, msg FROM usuario;
        ''')
        cont = 0
        for nome in acesso.fetchall():#fetchall() --> retorna uma lista
            self.linha = Label(self.window2, text=(nome), bg="#1cf", font=('Ivy 15'))
            self.linha.grid(row=cont, column="0")
            print(nome)
            cont = cont + 1
        for imc in acesso.fetchall():
            self.linha = Label(self.window2, text=(imc), width=25, bg="#1cf", font=('Ivy 15'))
            self.linha.grid(row=cont, column="1")
            print(imc)
            cont = cont + 1
        for msg in acesso.fetchall():
            self.linha = Label(self.window2, text=msg, width=25, bg="#1cf", font=('Ivy 15'))
            self.linha.grid(row=cont, column="2")
            print(msg)
            cont = cont + 1

        self.window2.mainloop()

        
Cal_imc()
