# Sistema de pedidos y facturacion - SakuraMaki

Curso 1FIS0275 - Fundamentos de Programacion 2, ciclo 2026-2

Integrantes:
- Walinn
- Gian
- Lucas
- Angie

Programa de consola para un restaurante de comida japonesa. Permite registrar
productos y empleados, tomar pedidos y emitir boletas y facturas.

## Ejecutar

```bash
python main.py
```

Para correr las pruebas de la logica del negocio:

```bash
python pruebas/pruebas_negocio.py
```

Cada prueba imprime OK o FALLA y al final se muestra cuantas salieron bien.

## Menus

1. **Mantenimiento de datos maestros:** registrar y listar productos (plato, bebida o
   combo), registrar empleados (mozo, cocinero o repartidor) y consultar la
   remuneracion del personal.
2. **Gestion de pedidos:** registrar un pedido (salon, para llevar o delivery),
   agregar o quitar lineas, enviarlo a cocina y buscarlo por numero o por mesa.
3. **Facturacion:** emitir una boleta o una factura, cobrar el pedido y ver los
   comprobantes emitidos.

## Organizacion

```text
main.py                       Portada y menu principal
modelo/producto.py            Producto (abstracta), Bebida, Plato y Combo
modelo/empleado.py            Empleado (abstracta), Mozo, Repartidor y Cocinero
modelo/mesa.py                Mesa
modelo/pedido.py              DetallePedido y Pedido
modelo/comprobante.py         Comprobante (abstracta), Boleta y Factura
sistema/restaurante.py        Guarda productos, empleados, mesas, pedidos y comprobantes
modulos/mantenimiento.py      Pantallas de mantenimiento
modulos/pedidos.py            Pantallas de pedidos
modulos/facturacion.py        Pantallas de facturacion
utiles/validaciones.py        Lectura segura de datos con try/except
utiles/formato.py             Funcion para recortar texto
utiles/datos_iniciales.py     Productos, empleados y mesas de ejemplo
pruebas/pruebas_negocio.py    Pruebas de los metodos de negocio
```

## Reglas del negocio

- **Estados del pedido:** Registrado, En preparacion y Pagado.
- Un pedido se puede facturar si no esta pagado y tiene al menos una linea.
- Al pagar, el pedido pasa a Pagado, la mesa queda libre y el mozo acumula propina.
- **Precio del plato:** el tamano Mediano suma S/ 3 y el Grande suma S/ 6.
- **Combo:** suma el precio de sus productos y resta su descuento.
- **Recargo al consumo:** 10 % del subtotal, solo en pedidos de salon.
- **Factura:** el precio de venta incluye IGV. Se divide entre `1 + 0.18` para obtener
  el valor de venta, y la diferencia es el IGV.
- **Remuneracion:**
  - Mozo: sueldo basico mas un porcentaje de la propina acumulada.
  - Repartidor: sueldo basico mas un monto por cada entrega.
  - Cocinero: solo el sueldo basico.

## Conceptos de POO

- **Abstraccion:** `Producto`, `Empleado` y `Comprobante` son clases abstractas.
- **Herencia:** `Plato`, `Bebida` y `Combo` heredan de `Producto`; `Mozo`, `Repartidor`
  y `Cocinero` de `Empleado`; `Boleta` y `Factura` de `Comprobante`.
- **Polimorfismo:** cada subclase implementa a su manera `calcular_precio()`,
  `calcular_remuneracion()` o `imprimir()`, y tiene su propio `__str__`.
- **Encapsulamiento:** los atributos usan doble guion bajo y se consultan con metodos.
- **Composicion:** `Pedido` contiene objetos `DetallePedido`. Si se borra el pedido, sus
  lineas desaparecen, porque no existen sin el.
- **Agregacion:** `Combo` contiene productos. Si se borra el Combo Duo Sakura, el maki y
  el te verde siguen en la carta, porque existen por separado.
- **Manejo de excepciones:** el modelo lanza `ValueError` o `IndexError` cuando se rompe
  una regla (codigo repetido, RUC invalido, pedido ya pagado, linea inexistente). Los
  modulos las atrapan con `try/except` y muestran un mensaje en vez de cerrar el
  programa. `utiles/validaciones.py` repite la pregunta hasta recibir un dato valido.

## Datos de ejemplo

```text
Productos: MAK01, RAM01, GYO01, DON01, BEB03, BEB05 y el combo CMB02
Mozos: EMP015 y EMP018
Cocinero: EMP004
Repartidor: EMP011
Mesas: 1 a 12 (4 personas) y 13 a 18 (6 personas)
```

## Estilo del codigo

Pensado para explicarse en clase: textos con f-strings, alineacion con `ljust` y
`rjust`, bucles `for` y `while` normales, y sin list comprehensions, lambdas ni
decoradores (salvo `@abstractmethod`).
