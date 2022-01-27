## Creación y configuración del Jupyter Book

1. Creación de un ambiente Conda.
2. Creación del Jupyter Book principal: balancehidrico.github.io
3. Publicación de modificaciones.

### 1. Creación de un ambiente Conda

```shell
# Actualización de Conda
$ conda update conda

# Borrado del ambiente (si es que existe)
$ # conda remove -n balancehidrico --all

# Creación del ambiente
$ conda create -n balancehidrico

# Activación del ambiente
$ conda activate balancehidrico

# Configuración del ambiente
$ conda config --env --add channels conda-forge
$ conda config --env --set channel_priority strict

# Instalación de módulos requeridos
$ conda install git python=3 jupyter numpy pandas matplotlib plotly dash gdal fiona shapely geopandas rasterio folium jupyter-book ghp-import

# Desactivación del ambiente
$ conda deactivate
```

### 2. Creación del Jupyter Book principal y publicación inicial del sitio web en GitHub Pages

```shell
$ conda activate balancehidrico

# Creación del Jupyter Book con una plantilla inicial
$ jupyter-book create balancehidrico.github.io

# Generación de archivos HTML (en el subdirectorio _build/html)
$ jupyter-book build balancehidrico.github.io

# En este punto, se crea en GitHub el repositorio balancehidrico.github.io

# Configuración del repositorio local y su branch main (para manejar los archivos fuente)
$ cd balancehidrico.github.io
$ git init
$ git add .
$ git commit -m "Commit inicial"
$ git branch -M main
$ git remote add origin https://github.com/balancehidrico/balancehidrico.github.io.git
$ git push -u origin main

# Creación del branch gh-pages (para manejar los archivos HTML publicados)
$ ghp-import -n -p -f _build/html

# En este punto, se configura el repositorio para buscar los archivos de GH Pages en la rama gh-pages
# El sitio debe estar disponible en https://balancehidrico.github.io/

$ conda deactivate
```

### 3. Publicación de modificaciones

```shell
# Generación de archivos HTML (debe hacerse desde el directorio padre del Jupyter Book)
$ jupyter-book build balancehidrico.github.io

$ cd balancehidrico.github.io

# Aplicación de cambios en el branch main
$ git status
$ git add .
$ git commit -m "###Comentario###"
$ git push

# Aplicación de cambios en el branch gh-pages
$ ghp-import -n -p -f _build/html
```
