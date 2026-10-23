# IMEYFISHY OPTIMIZER

Optimizador seguro para jugadores competitivos de Fortnite (Windows 10/11 x64). Tema negro y morado.

## Descargar
Ve a la pestaña **Releases** y descarga `IMEYFISHY_OPTIMIZER.exe`. Es un único archivo: doble clic y listo.
No necesita Python ni ninguna instalación. Si Windows SmartScreen avisa, pulsa "Más información" → "Ejecutar de todas formas" (el .exe no está firmado digitalmente).

## Funciones
- Limpieza de temporales: analiza primero, muestra el espacio recuperable, limpia solo lo que elijas y omite archivos en uso.
- Bloatware: separa apps OPCIONALES de componentes ESENCIALES; nada se desinstala sin confirmación.
- Modo Competitivo: cierra solo las apps opcionales que selecciones (nunca Defender, drivers, EAC ni Fortnite) y aplica un perfil reversible.
- Monitor: CPU, RAM, disco, red y procesos con consumo excesivo, en tiempo real.
- Inicio de Windows: activa/desactiva entradas de arranque (igual que el Administrador de tareas); las críticas quedan protegidas.
- Restauración: registro de todos los cambios, reversión individual o total y creación de punto de restauración de Windows.

## Logo
Haz clic en el logo (arriba a la izquierda) dentro de la app y elige tu PNG.

## Compilación
GitHub Actions compila automáticamente el .exe con PyInstaller en Windows x64 en cada cambio (`.github/workflows/build.yml`).
