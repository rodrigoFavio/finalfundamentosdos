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
    def get_codigo(self): return self.__codigo
    def get_titulo(self): return self.__titulo
    def get_autor(self): return self.__autor
    def get_categoria(self): return self.__categoria
    def get_stock(self): return self.__stock
    def get_precio(self): return self.__precio
    def get_total_usos(self): return self.__veces_vendido + self.__veces_prestado

    # ----- Setters -----
    def set_titulo(self, titulo): self.__titulo = titulo
    def set_autor(self, autor): self.__autor = autor
    def set_categoria(self, categoria): self.__categoria = categoria
    def set_stock(self, stock):
        if stock >= 0:
            self.__stock = stock
        else:
            print("El stock no puede ser negativo.")
    def set_precio(self, precio):
        if precio > 0:
            self.__precio = precio
        else:
            print("El precio debe ser positivo.")

    def aumentar_ventas(self, cantidad): self.__veces_vendido += cantidad
    def aumentar_prestamos(self): self.__veces_prestado += 1

    @abstractmethod
    def tipo(self):
        pass

    def __str__(self):
        return f"[{self.tipo()}] {self.__titulo} - {self.__autor} | S/.{self.__precio:.2f} | Stock: {self.__stock}"


class Libro(Publicacion):
    def tipo(self): return "Libro"


class Revista(Publicacion):
    def tipo(self): return "Revista"


# ===================================
# CLASES DE USUARIOS
# ===================================
class Usuario(ABC):
    def __init__(self, dni, nombre, correo):
        self.__dni = dni
        self.__nombre = nombre
        self.__correo = correo

    # ----- Getters -----
    def get_dni(self): return self.__dni
    def get_nombre(self): return self.__nombre
    def get_correo(self): return self.__correo

    # ----- Setters -----
    def set_nombre(self, nombre): self.__nombre = nombre
    def set_correo(self, correo):
        if "@" in correo and "." in correo:
            self.__correo = correo
        else:
            print("Correo inválido.")

    @staticmethod
    def validar_dni(dni):
        return dni.isdigit() and len(dni) == 8

    @abstractmethod
    def tipo(self):
        pass

    def __str__(self):
        return f"{self.__nombre} ({self.tipo()}) - DNI: {self.__dni}, Correo: {self.__correo}"


class Estudiante(Usuario):
    def tipo(self): return "Estudiante"


class Docente(Usuario):
    def tipo(self): return "Docente"


# ===================================
# CLASES DE OPERACIONES
# ===================================
class Prestamo:
    def __init__(self, id_prestamo, publicacion, usuario, fecha, vence):
        self.id_prestamo = id_prestamo
        self.publicacion = publicacion
        self.usuario = usuario
        self.fecha = fecha
        self.vence = vence
        self.devuelto = None

    def devolver(self):
        self.devuelto = datetime.now()
        self.publicacion.set_stock(self.publicacion.get_stock() + 1)

    def calcular_multa(self):
        if not self.devuelto:
            return 0
        atraso = (self.devuelto.date() - self.vence.date()).days
        return max(0, atraso * 1.0)  # multa de S/1 por día de retraso

    def __str__(self):
        estado = "Devuelto" if self.devuelto else "Prestado"
        return f"[{self.id_prestamo}] {self.publicacion.get_titulo()} → {self.usuario.get_nombre()} | {estado}"


class Venta:
    def __init__(self, id_venta, usuario, publicacion, cantidad):
        self.id_venta = id_venta
        self.usuario = usuario
        self.publicacion = publicacion
        self.cantidad = cantidad
        self.fecha = datetime.now()
        self.total = publicacion.get_precio() * cantidad

    def __str__(self):
        return f"[{self.id_venta}] {self.publicacion.get_titulo()} x{self.cantidad} → {self.usuario.get_nombre()} | Total: S/.{self.total:.2f}"


# ===================================
# CLASE PRINCIPAL: BIBLIOTECA
# ===================================
class Biblioteca:
    def __init__(self):
        self.publicaciones = []
        self.usuarios = []
        self.prestamos = []
        self.ventas = []
        self.next_prestamo_id = 1
        self.next_venta_id = 1

    # ------------------------
    # Registrar publicación
    # ------------------------
    def registrar_publicacion(self, codigo, titulo, autor, categoria, stock, precio, tipo):
        # Validar duplicado
        if any(p.get_codigo() == codigo for p in self.publicaciones):
            print(" Ya existe una publicación con ese código.")
            return
        if tipo.lower() == "libro":
            pub = Libro(codigo, titulo, autor, categoria, stock, precio)
        else:
            pub = Revista(codigo, titulo, autor, categoria, stock, precio)
        self.publicaciones.append(pub)
        print(" Publicación registrada correctamente.")

    # ------------------------
    # Registrar usuario
    # ------------------------
    def registrar_usuario(self, dni, nombre, correo, tipo):
        if not Usuario.validar_dni(dni):
            print(" DNI inválido. Debe tener 8 dígitos numéricos.")
            return
        if any(u.get_dni() == dni for u in self.usuarios):
            print(" Ya existe un usuario con ese DNI.")
            return
        if tipo.lower() == "estudiante":
            user = Estudiante(dni, nombre, correo)
        else:
            user = Docente(dni, nombre, correo)
        self.usuarios.append(user)
        print(" Usuario registrado correctamente.")

    # ------------------------
    # Registrar préstamo
    # ------------------------
    def registrar_prestamo(self, dni, codigo):
        usuario = next((u for u in self.usuarios if u.get_dni() == dni), None)
        publicacion = next((p for p in self.publicaciones if p.get_codigo() == codigo), None)
        if not usuario or not publicacion:
            print(" Usuario o publicación no encontrados.")
            return
        if publicacion.get_stock() <= 0:
            print("No hay stock disponible.")
            return
        vence = datetime.now() + timedelta(days=7)
        prestamo = Prestamo(self.next_prestamo_id, publicacion, usuario, datetime.now(), vence)
        publicacion.set_stock(publicacion.get_stock() - 1)
        publicacion.aumentar_prestamos()
        self.prestamos.append(prestamo)
        self.next_prestamo_id += 1
        print(f" Préstamo registrado. Vence el {vence.date()}.")

    # ------------------------
    # Devolver libro
    # ------------------------
    def devolver_libro(self, id_prestamo):
        prestamo = next((p for p in self.prestamos if p.id_prestamo == id_prestamo), None)
        if not prestamo:
            print(" Préstamo no encontrado.")
            return
        prestamo.devolver()
        multa = prestamo.calcular_multa()
        print(f"Devolución registrada. Multa: S/.{multa:.2f}")

    # ------------------------
    # Registrar venta
    # ------------------------
    def registrar_venta(self, dni, codigo, cantidad):
        usuario = next((u for u in self.usuarios if u.get_dni() == dni), None)
        publicacion = next((p for p in self.publicaciones if p.get_codigo() == codigo), None)
        if not usuario or not publicacion:
            print("Usuario o publicación no encontrados.")
            return
        if cantidad > publicacion.get_stock():
            print("Stock insuficiente.")
            return
        venta = Venta(self.next_venta_id, usuario, publicacion, cantidad)
        publicacion.set_stock(publicacion.get_stock() - cantidad)
        publicacion.aumentar_ventas(cantidad)
        self.ventas.append(venta)
        self.next_venta_id += 1
        print(f"Venta registrada. Total: S/.{venta.total:.2f}")

    # ------------------------
    # Reportes y listados
    # ------------------------
    def listar_publicaciones(self):
        for p in self.publicaciones:
            print(p)

    def ver_stock_bajo(self):
        bajos = [p for p in self.publicaciones if p.get_stock() < 3]
        if not bajos:
            print("No hay publicaciones con stock bajo.")
        else:
            print("Publicaciones con stock bajo:")
            for p in bajos:
                print(" ", p)

    def top_publicaciones(self):
        top = sorted(self.publicaciones, key=lambda p: p.get_total_usos(), reverse=True)[:5]
        print("\n Top de publicaciones más demandadas:")
        for p in top:
            print(f"  {p.get_titulo()} | Usos totales: {p.get_total_usos()}")


# ===================================
# MENÚ PRINCIPAL
# ===================================
def menu():
    bib = Biblioteca()
    while True:
        print("\n=== SISTEMA DE BIBLIOTECA ===")
        print("1. Registrar publicación")
        print("2. Registrar usuario")
        print("3. Registrar préstamo")
        print("4. Devolver libro")
        print("5. Registrar venta")
        print("6. Listar publicaciones")
        print("7. Ver stock bajo")
        print("8. Top publicaciones más demandadas")
        print("9. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            c = input("Código: ")
            t = input("Título: ")
            a = input("Autor: ")
            cat = input("Categoría: ")
            s = int(input("Stock: "))
            p = float(input("Precio: "))
            tipo = input("Tipo (Libro/Revista): ")
            bib.registrar_publicacion(c, t, a, cat, s, p, tipo)

        elif opcion == "2":
            dni = input("DNI: ")
            nom = input("Nombre: ")
            corr = input("Correo: ")
            tipo = input("Tipo (Estudiante/Docente): ")
            bib.registrar_usuario(dni, nom, corr, tipo)

        elif opcion == "3":
            dni = input("DNI del usuario: ")
            cod = input("Código del libro/revista: ")
            bib.registrar_prestamo(dni, cod)

        elif opcion == "4":
            idp = int(input("ID del préstamo: "))
            bib.devolver_libro(idp)

        elif opcion == "5":
            dni = input("DNI del comprador: ")
            cod = input("Código del libro/revista: ")
            cant = int(input("Cantidad: "))
            bib.registrar_venta(dni, cod, cant)

        elif opcion == "6":
            bib.listar_publicaciones()

        elif opcion == "7":
            bib.ver_stock_bajo()

        elif opcion == "8":
            bib.top_publicaciones()

        elif opcion == "9":
            print(" Saliendo del sistema...")
            break
        else:
            print(" Opción inválida.")


# ===================================
# EJECUCIÓN
# ===================================
if __name__ == "__main__":
    menu()
