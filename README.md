# FloraFiel Mascotas — Módulo Odoo 17

Módulo personalizado para Odoo 17 que implementa una **Ficha de Mascota** asociada a los clientes de FloraFiel S.L.

Permite registrar las mascotas de cada cliente con sus datos físicos y calcula automáticamente la edad y la ración diaria de pienso recomendada según especie y tamaño.

---

## Características

- Ficha de mascota con especie, raza, peso, tamaño y fecha de nacimiento
- Cálculo automático de edad en años (con decimal)
- Cálculo automático de ración diaria de pienso según especie y tamaño
- Relación con clientes reales de Odoo (filtrado por `customer_rank > 0`)
- Pestaña "Mascotas" integrada en la ficha del cliente
- Vistas lista, kanban y formulario
- Sistema de permisos con grupos Usuario y Manager

---

## Requisitos

- Odoo 17 Community instalado y funcionando
- Python 3.10+
- Módulos Odoo: `base`, `contacts`

---

## Instalación paso a paso

### 1. Conectar al servidor

```bash
ssh root@TU_SERVIDOR -p TU_PUERTO
```

### 2. Ir a la carpeta de custom-addons

```bash
cd /opt/odoo/odoo17/custom-addons
```

### 3. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/florafiel_mascotas.git
```

O si lo descargas como ZIP, súbelo con SCP desde tu máquina local:

```bash
scp -P TU_PUERTO -r florafiel_mascotas root@TU_SERVIDOR:/opt/odoo/odoo17/custom-addons/
```

### 4. Verificar permisos

```bash
chown -R odoo17:odoo17 /opt/odoo/odoo17/custom-addons/florafiel_mascotas
```

### 5. Verificar que el path está en odoo.conf

```bash
cat /etc/odoo/odoo17.conf | grep addons_path
```

Debe contener `/opt/odoo/odoo17/custom-addons`. Si no está, añádelo:

```bash
nano /etc/odoo/odoo17.conf
```

```ini
addons_path = /opt/odoo/odoo17/addons,/opt/odoo/odoo17/custom-addons
```

### 6. Reiniciar el servicio

```bash
sudo systemctl restart odoo17
```

### 7. Instalar el módulo desde Odoo

1. Abre Odoo en el navegador
2. Ve a **Ajustes → Activar modo desarrollador**
3. Ve a **Aplicaciones → Actualizar lista de aplicaciones** → Confirmar
4. Busca `FloraFiel Mascotas` (quita el filtro "Aplicaciones" si no aparece)
5. Haz clic en **Activar**

### 8. Asignar permisos al usuario administrador

1. Ve a **Ajustes → Usuarios → Administrador**
2. En la sección **FloraFiel Mascotas** selecciona **Manager**
3. Guarda

---

## Uso

### Crear una mascota

1. Ve a **FloraFiel Mascotas → Todas las mascotas**
2. Haz clic en **Nuevo**
3. Rellena nombre, especie, tamaño, peso y fecha de nacimiento
4. Selecciona el cliente propietario
5. Guarda — los campos **Edad** y **Ración diaria** se calculan automáticamente

### Ver mascotas desde la ficha del cliente

1. Ve a **Contactos**
2. Abre cualquier cliente
3. Haz clic en la pestaña **Mascotas**

---

## Tabla de raciones diarias recomendadas

| Especie | Tamaño | Factor (g/kg de peso) |
|---|---|---|
| Perro | Pequeño | 30 |
| Perro | Mediano | 25 |
| Perro | Grande | 20 |
| Gato | Pequeño | 20 |
| Gato | Mediano | 18 |
| Gato | Grande | 15 |
| Otro | Cualquiera | 22 |

---

## Solución de problemas

### El módulo no aparece en el menú

- Cierra sesión y vuelve a entrar
- Verifica que tu usuario tiene el grupo **FloraFiel Mascotas / Manager** asignado

### Un cliente no aparece en el campo Cliente

Los clientes deben tener `customer_rank > 0`. Si un cliente se registró desde el eCommerce y no aparece, ejecuta:

```bash
sudo -u odoo17 psql -d florafiel_probas -c \
  "UPDATE res_partner SET customer_rank = 1 \
   WHERE customer_rank = 0 \
   AND id IN (SELECT DISTINCT partner_id FROM sale_order WHERE state IN ('sale', 'done'));"
```

### Error al actualizar el módulo

Reinicia siempre antes de actualizar si has tocado archivos Python:

```bash
sudo systemctl restart odoo17
```

Luego desde **Aplicaciones → FloraFiel Mascotas → Actualizar**.

### Ver logs en tiempo real

```bash
sudo tail -f /var/log/odoo17/odoo17.log
```

---

## Estructura del módulo

```
florafiel_mascotas/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── mascota.py          # Modelo principal + campos calculados
│   └── res_partner.py      # Herencia Python sobre res.partner
├── views/
│   ├── mascota_views.xml   # Vistas lista, kanban, formulario y menús
│   └── res_partner_views.xml  # Herencia XPath sobre ficha de cliente
├── security/
│   ├── security.xml        # Definición de grupos Usuario/Manager
│   └── ir.model.access.csv # Permisos por modelo
└── data/
    └── mascotas_demo.xml   # Datos iniciales (vacío por defecto)
```

---

## Autor

**Luis Miguel Agra Álvarez**  
IES Armando Cotarelo Valledor  
Sistemas de Gestión Empresarial — DAM 25/26
