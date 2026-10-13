# Modulo de facturacion - SakuraMaki

Esta rama contiene una preview independiente del modulo de facturacion. Su objetivo
es demostrar las HU-10, HU-11 y HU-12 mientras los demas integrantes desarrollan
los modulos de mantenimiento y pedidos.

## Ejecutar

```bash
python3 main.py
```

La preview muestra los pedidos y cajeros disponibles antes de abrir el menu.

## Organizacion

```text
main.py                  Clases minimas y datos para ejecutar la preview
modelo/comprobante.py    Comprobante, Boleta y Factura
modulos/facturacion.py   Menu y flujo de emision
utiles/validaciones_facturacion.py   Lectura segura de datos con try/except
```

## Orden sugerido para explicar el codigo

1. `main.py` crea los datos precargados y llama al menu de facturacion.
2. `facturacion.py` busca y valida el pedido y el cajero.
3. El usuario selecciona boleta o factura y el medio de pago.
4. `comprobante.py` crea el objeto correspondiente y prepara su impresion.
5. El restaurante guarda el comprobante, paga el pedido y libera la mesa.

## Conceptos de POO

- Abstraccion: `Comprobante` define la estructura comun.
- Herencia: `Boleta` y `Factura` heredan de `Comprobante`.
- Polimorfismo: cada subclase implementa su propio metodo `imprimir()`.
- Encapsulamiento: los atributos usan doble guion bajo y se consultan mediante metodos.
- Composicion: `Pedido` contiene objetos `DetallePedido`.

## Datos para la demostracion

```text
Cajeros: EMP021 y EMP022
Pedidos: PED-000001, PED-000002 y PED-000003
Mesas disponibles para busqueda: 7 y 12
```

La factura usa precios que incluyen IGV. Por eso divide el precio de venta entre
`1 + 0.18` para obtener el valor de venta y calcula la diferencia como IGV.
