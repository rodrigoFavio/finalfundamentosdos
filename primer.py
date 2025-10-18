from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# ===================================
# CLASES DE PUBLICACIONES
# ===================================
class Publicacion(ABC):
    def __init__(self, codigo, titulo, autor, categoria, stock, precio):
        self.__codigo = codigo
        self.__titulo = titulo
        self.__autor = autor
        self.__categoria = categoria
        self.__stock = stock
        self.__precio = precio
        self.__veces_vendido = 0
        self.__veces_prestado = 0

    # ----- Getters -----
    def get_codigo(self): 
        return self.__codigo
    def get_titulo(self): 
        return self.__titulo
    def get_autor(self): 
        return self.__autor
    def get_categoria(self): 
        return self.__categoria
    def get_stock(self): 
        return self.__stock
    def get_precio(self): 
        return self.__precio
    def get_total_usos(self): 
        return self.__veces_vendido + self.__veces_prestado

    # ----- Setters -----
    def set_titulo(self, titulo): 
        self.__titulo = titulo
    def set_autor(self, autor): 
        self.__autor = autor
    def set_categoria(self, categoria): 
        self.__categoria = categoria
    def set_stock(self, stock):
        if stock >= 0:
            self.__stock = stock
        else:
            print(" El stock no puede ser negativo.")
    def set_precio(self, precio):
        if precio > 0:
            self.__precio = precio
        else:
            print(" El precio debe ser positivo.")

    def aumentar_ventas(self, cantidad): 
        self.__veces_vendido += cantidad
    def aumentar_prestamos(self): 
        self.__veces_prestado += 1

    @abstractmethod
    def tipo(self):
        pass

    def __str__(self):
        return f"[{self.tipo()}] {self.__titulo} - {self.__autor} | S/.{self.__precio:.2f} | Stock: {self.__stock}"


class Libro(Publicacion):
    def tipo(self): return "Libro"


class Revista(Publicacion):
    def tipo(self): return "Revista"
