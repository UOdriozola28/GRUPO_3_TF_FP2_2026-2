# Sistema de gestion de pedidos y facturacion - SakuraMaki S.A.C.

Aplicacion de consola en Python organizada con la misma estructura del repositorio
`EXAMPLE-RESTAURANTE`. Esta version implementa el modulo de facturacion descrito
en las HU-10, HU-11 y HU-12 del Capitulo 2.

## Ejecutar

```bash
python3 main.py
```

Al iniciar se carga el pedido `PED-000001`, mesa 7, en estado `Listo`. Para probar
la pantalla de facturacion use el cajero `EMP021`.

## Pruebas

```bash
python3 -m unittest discover -s pruebas -v
```

## Estructura

```text
modelo/       clases Producto, Empleado, Pedido, Mesa y Comprobante
sistema/      coordinacion, correlativos y cierre del pedido
modulos/      pantallas de consola; facturacion contiene la entrega principal
utiles/       validaciones de entrada y datos iniciales
pruebas/      pruebas automatizadas de las reglas de facturacion
main.py       menu principal
```

## Reglas de facturacion implementadas

- Solo se factura un pedido en estado `Listo` y con productos.
- Se valida que el responsable exista, este activo y tenga rol `Cajero`.
- Se emiten boletas `B001` y facturas `F001` con correlativos independientes.
- La factura exige RUC de 11 digitos y razon social.
- Se muestran valor de venta, IGV de 18 %, recargo al consumo y total.
- La operacion solicita confirmacion antes de modificar el pedido.
- Al cobrar, el pedido pasa a `Pagado` y la mesa de salon queda libre.
