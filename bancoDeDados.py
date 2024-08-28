import sqlite3

class Usuario:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return "Usuário: {}".format(self.nome)
    
    def salvar(self):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome) VALUES (?)", (self.nome,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def listar_usuarios():
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios
    
    @staticmethod
    def buscar_usuario(nome):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome=?", (nome,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario
    
    @staticmethod
    def deletar_usuario(nome):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE nome=?", (nome,))
        conn.commit()
        conn.close()

class Memoria:
    def __init__(self, nome, midia):
        self.nome = nome
        self.midia = midia
        self.localizao_memoria = None

    def __str__(self):
        return "Memória: {}".format(self.nome)

    def salvar(self):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO memorias (nome, midia) VALUES (?, ?)", (self.nome, self.midia))
        conn.commit()
        conn.close()
    
    @staticmethod
    def listar_memorias():
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM memorias")
        memorias = cursor.fetchall()
        conn.close()
        return memorias
    
    @staticmethod
    def buscar_memoria(nome):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM memorias WHERE nome=?", (nome,))
        memoria = cursor.fetchone()
        conn.close()
        return memoria
    
    @staticmethod
    def deletar_memoria(nome):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memorias WHERE nome=?", (nome,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def associar_memoria_usuario(nome_usuario, nome_memoria):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios_memorias (usuario, memoria) VALUES (?, ?)", (nome_usuario, nome_memoria))
        conn.commit()
        conn.close()
    

if __name__ == "__main__":
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (nome text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS memorias (nome text, midia text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios_memorias (usuario text, memoria text)")
    conn.commit()
    conn.close()