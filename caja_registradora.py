import unittest

class ProductoNoExiste(Exception):
    pass

class PedidoFinalizado(Exception):
    pass

class PedidoVacio(Exception):
    pass

class CompraNoFinalizada(Exception):
    pass

class PagoInsuficiente(Exception):
    pass

class Producto(object):
    def __init__(self, codigo, nombre, precio, descuento = 0):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__precio = precio
        self.__descuento = descuento

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        self.__codigo = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, valor):
        self.__precio = valor

    @property
    def descuento(self):
        return self.__descuento

    @descuento.setter
    def descuento(self, valor):
        self.__descuento = valor

    def __str__(self):
        return 'Código: ' + str(self.__codigo) + ', nombre: ' + self.__nombre + ', precio: ' + str(self.__precio)


class Pedido(object):
    def __init__ (self):
        self.productos = []
        self.cantidades = []

    def agregar_producto(self, p):
        if p in self.productos:
            indice = self.productos.index(p)
            self.cantidades[indice] = self.cantidades[indice] + 1
        else:
            self.productos.append(p)
            self.cantidades.append(1)

    def mostrar_pedido(self):
        print('Código\t\tNombre\t\t\tP U\tCant\tPrecio')
        for (p,c) in zip(self.productos, self.cantidades):
            print(str(p.codigo) + '\t\t' + p.nombre + '\t\t$' + str(p.precio) + '\t' + str(c) + '\t$' + str(p.precio * c))

class Caja(object):
    def __init__ (self, lista):
        self.pedidoactual = Pedido()
        self.fin = False
        self.lista = lista

    def pedido_actual(self):
        return self.pedidoactual

    def agregar_producto(self, c):
        verificador = 0
        for p in self.lista:
            if c == p.codigo:
                self.pedido_actual().agregar_producto(p)
                verificador = 1
        if verificador == 0:
            raise ProductoNoExiste('El producto con código {} no existe'.format(c))


    def finalizar(self):
        if self.fin:
            raise PedidoFinalizado('El pedido ya se encuentra finalizado')
        if not self.pedido_actual().productos:
            raise PedidoVacio('El pedido está vacío')
        self.fin = True

    def subtotal_pedido(self):
        subtotal = 0
        for (p,c) in zip(self.pedido_actual().productos, self.pedido_actual().cantidades):
            subtotal += (p.precio * c)
        return subtotal

    def total_pedido(self):
        if self.fin == False:
            raise CompraNoFinalizada('Finalice la compra para calcular el total')
        total = 0
        for (p,c) in zip(self.pedido_actual().productos, self.pedido_actual().cantidades):
            total += (p.precio - ((p.precio * p.descuento) / 100)) * c
        return total

    def calculo_pago(self, pago):
        total = self.total_pedido()
        if total > pago:
            raise PagoInsuficiente('El monto debe ser mayor al total del pedido')
        return pago - total

class CajaTest(unittest.TestCase):

    def setUp(self):
        self.p1 = Producto(12345, 'Pimientos', 100, 20)
        self.p2 = Producto(33444, 'Naranjas', 30, 10)
        self.p3 = Producto(20202, 'Kiwis', 70)
        self.lista = [self.p1, self.p2, self.p3]
        self.caja = Caja(self.lista)

    def test01_ProductoNoExiste(self):
        codigo = 77777
        self.assertRaises(ProductoNoExiste, self.caja.agregar_producto, codigo)

    def test02_PedidoYaFinalizado(self):
        self.caja.agregar_producto(12345)
        self.caja.agregar_producto(12345)
        self.caja.finalizar()

    def test03_PedidoFinalizadoVacio(self):
        self.assertRaises(PedidoVacio, self.caja.finalizar)

    def test04_TotalSinFinalizar(self):
        self.caja.agregar_producto(12345)
        self.caja.agregar_producto(12345)
        self.assertRaises(CompraNoFinalizada, self.caja.total_pedido)

    def test05_PagoMenorATotal(self):
        self.caja.agregar_producto(12345)
        self.caja.agregar_producto(12345)
        self.caja.agregar_producto(20202)
        self.caja.finalizar()
        pago = 10
        self.assertRaises(PagoInsuficiente, self.caja.calculo_pago, pago)

    def test06_CalculoVuelto(self):
        self.caja.agregar_producto(12345)
        self.caja.agregar_producto(12345)
        self.caja.agregar_producto(20202)
        self.caja.finalizar()
        self.assertEqual(70, self.caja.calculo_pago(300))

    def test07_AgregarProducto(self):
        self.caja.agregar_producto(12345)
        self.assertEqual(1, len(self.caja.pedido_actual().productos))
        self.assertEqual(12345, self.caja.pedido_actual().productos[0].codigo)

    def test08_CalcularSubTotal(self):
        self.caja.agregar_producto(12345)
        self.caja.agregar_producto(12345)
        self.caja.agregar_producto(20202)
        self.assertEqual(270, self.caja.subtotal_pedido())

    def test08_CalcularTotal(self):
        self.caja.agregar_producto(12345)
        self.caja.agregar_producto(12345)
        self.caja.agregar_producto(20202)
        self.caja.finalizar()
        self.assertEqual(230, self.caja.total_pedido())

if __name__ == '__main__':
    unittest.main()