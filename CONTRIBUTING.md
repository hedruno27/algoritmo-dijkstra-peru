# Cómo Contribuir

¡Gracias por tu interés en contribuir a este proyecto! 🎉

## Reportar Bugs

1. Verifica que el bug no haya sido reportado ya en [Issues](../../issues).
2. Abre un nuevo Issue usando la plantilla de **Bug Report**.
3. Incluye: pasos para reproducirlo, comportamiento esperado vs. actual, y tu entorno (SO, versión de Python).

## Proponer Mejoras

1. Abre un Issue usando la plantilla de **Feature Request**.
2. Describe la mejora y por qué sería útil.

## Pull Requests

1. Haz un **fork** del repositorio.
2. Crea una rama descriptiva:
   ```bash
   git checkout -b feature/nombre-de-la-mejora
   # o
   git checkout -b fix/descripcion-del-bug
   ```
3. Realiza tus cambios con commits atómicos y mensajes claros:
   ```
   feat: agregar visualización de distancias en el panel
   fix: corregir cálculo de distancia acumulada
   docs: actualizar README con instrucciones de venv
   ```
4. Asegúrate de que la aplicación funcione correctamente antes de enviar.
5. Abre el Pull Request describiendo los cambios realizados.

## Convención de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

| Prefijo | Uso |
|---------|-----|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de bug |
| `docs:` | Cambios en documentación |
| `style:` | Cambios de formato/estilo (sin lógica) |
| `refactor:` | Refactorización de código |
| `chore:` | Tareas de mantenimiento |
