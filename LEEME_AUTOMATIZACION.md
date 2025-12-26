# Guía de Automatización

Para actualizar tu web automáticamente:

## 1. Configuración Inicial (Solo una vez)
1. Abre tu terminal (Terminal.app).
2. Arrastra el archivo `subir_cambios.sh` a la terminal y dale Enter si te pide permisos.
3. Si te dice "No remote configuration", copia y pega esto:
   `git remote add origin https://github.com/samuelhes/plannerprogenerator.git`

## 2. Uso Diario (Automático)
Cada vez que quieras subir cambios, solo haz doble click en `subir_cambios.sh` (o ejecútalo desde terminal: `./subir_cambios.sh`).

El script hará todo:
1. Guardar tus archivos (Commit).
2. Subirlos a GitHub (Push).
3. Render se actualizará solo.
