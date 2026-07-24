# 🔍 Sistema de Monitoreo Automatizado de Servicios

Un ecosistema híbrido diseñado para monitorizar el estado de salud de servicios web, registrar históricos en bases de datos y desencadenar alertas automatizadas ante caídas o errores de infraestructura.

## 🚀 Arquitectura del Proyecto

Este proyecto combina la potencia de la programación en Python con la versatilidad de los flujos de trabajo en n8n, separando las responsabilidades de manera inteligente:

* **Motor de Monitoreo (Python):** Script principal que se encarga del trabajo pesado, realizando peticiones (ping) periódicas a los servicios definidos y manejando los tiempos de espera.
* **Persistencia Local (SQLite):** Base de datos relacional que almacena el histórico completo de los estados para futuras consultas y cálculos de SLA.
* **Visualización (Flask):** Un dashboard web ligero y claro que permite observar el estado de salud de la infraestructura en tiempo real.
* **Automatización de Respuesta (n8n):** Flujo encargado de la persistencia en la nube y el envío de alertas, activado únicamente ante eventos críticos para evitar la saturación.

## 🛠️ Tecnologías y Habilidades Destacadas

* **Lenguajes:** Python, HTML, CSS (Bootstrap)
* **Librerías / Frameworks:** `requests`, `flask`, `sqlite3`
* **Automatización y Orquestación:** n8n
* **Integraciones y APIs:** Google Sheets API, Gmail API, Webhooks
* **Control de Calidad (QA):** Uso de *mock data* (simulación de URLs falsas) para forzar respuestas de error (`NameResolutionError`) y validar el disparo de alertas en entornos seguros.

## ⚙️ Flujo Lógico de n8n

El sistema de alertas funciona mediante un Webhook que se comunica directamente con el motor de Python.

1.  **Webhook de Entrada:** Recibe el *payload* JSON exacto con la información del evento (servicio, url, status, code, mensaje y fecha).
2.  **Google Sheets (Append):** Almacena un registro histórico en la nube para reportes y seguimiento.
3.  **If ERROR/DOWN (Lógica Condicional):** Actúa como filtro inteligente para asegurar que el flujo continúe solo si el sistema detecta una caída.
4.  **Gmail (Notificación):** Envía un correo electrónico estructurado al equipo de IT informando sobre la incidencia.

## 📸 Evidencias de Ejecución

*(Nota: Asegúrate de tener estas imágenes en la carpeta de tu repositorio)*

**1. Flujo completo y exitoso en n8n:**
![Flujo de n8n](./test_pics/Workflow_n8n.png)

**2. Alerta recibida en la bandeja de entrada:**
![Alerta Gmail](./test_pics/AlertaEnMail.png)

**3. Persistencia de datos en la nube:**
![Google Sheets](./test_pics/PersitenciaEnGoogleSheets.png)
