# 🌸 365 Días · 365 Flores

Calendario floral anual: del **29/09/2026** al **28/09/2027**. Cada día tiene su
propio archivo `dia-MM-DD.html` con una foto y el significado de su flor.

## Estructura

| Archivo / carpeta | Qué es |
|---|---|
| `index.html` | Página principal con los botones «Todos los días» y «Día actual» |
| `dias.html` | Selector con buscador y meses para elegir cualquier día |
| `dia_actual.html` | Redirige automáticamente a la flor del día de hoy |
| `dia-MM-DD.html` | Las 365 páginas individuales (una por día, con candado hasta su fecha) |
| `flores.js` | Datos que leen las páginas (lo genera `generar_paginas.py`) |
| `style.css` | Estilos de todo el sitio |
| `flores.json` | Los datos (fecha, flor, significado) — edítalo si quieres |
| `generar_paginas.py` | Regenera `dias.html` y las 365 páginas desde `flores.json` |
| `img/` | Aquí van las fotos de cada flor |

## 🔒 Desbloqueo día a día

Cada flor se desbloquea a las **00:00 del día que le corresponde** (según la
fecha del dispositivo de quien visita la web). Hasta entonces, su página
muestra una «flor misteriosa» 🔒 con una cuenta atrás y una pista.

> **Nota:** al ser una web 100 % estática (GitHub Pages), el bloqueo es
> «blando»: los datos están en `flores.js` y una persona con conocimientos
> técnicos podría leerlos. Para un calendario personal o regalo es más que
> suficiente; si necesitas secreto real haría falta un servidor.

## 🖼️ Añadir las fotos

Cada página busca su foto en `img/` con este nombre:

```
img/MM-DD-flor-en-minusculas-sin-acentos.jpg
```

Ejemplos:
- `img/09-29-brezo-blanco.jpg` → Brezo blanco (29/09)
- `img/02-14-rosa-roja.jpg` → Rosa roja (14/02)
- `img/09-21-girasol-flores-amarillas.jpg` → Girasol (21/09)

Mientras falte una foto, la página muestra una imagen provisional automática.

## ✏️ Editar flores o significados

1. Modifica `flores.json` (formato: `{"n": 1, "dd": "29", "mm": "09", "name": "...", "meaning": "..."}`).
2. Ejecuta:

```bash
python generar_paginas.py
```

## 🚀 Subir a GitHub (GitHub Pages)

```bash
git init
git add .
git commit -m "Calendario 365 flores"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

Luego, en GitHub: **Settings → Pages → Source: main branch → Save**.
Tu web estará en `https://TU_USUARIO.github.io/TU_REPO/`.
