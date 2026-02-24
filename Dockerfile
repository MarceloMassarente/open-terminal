FROM python:3.12

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Core utilities
    coreutils findutils grep sed gawk diffutils patch \
    less file tree bc man-db \
    # Networking
    curl wget net-tools iputils-ping dnsutils netcat-openbsd socat telnet \
    openssh-client rsync \
    # Editors
    vim nano \
    # Version control
    git \
    # Build tools
    build-essential cmake make \
    # Scripting & languages
    perl ruby-full lua5.4 \
    # Data processing
    jq xmlstarlet sqlite3 csvkit miller \
    postgresql-client default-mysql-client redis-tools \
    # Media & documents
    ffmpeg pandoc imagemagick \
    poppler-utils tesseract-ocr qpdf ghostscript libreoffice \
    graphviz \
    # Scientific and geospatial native deps
    gfortran libopenblas-dev liblapack-dev \
    gdal-bin libgdal-dev \
    # Developer tooling
    shellcheck ripgrep fd-find fzf \
    # Compression
    zip unzip tar gzip bzip2 xz-utils zstd p7zip-full \
    # System
    procps htop lsof strace sysstat \
    sudo tmux screen \
    ca-certificates gnupg apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

# Node.js (LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g npm@latest yarn pnpm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir \
    numpy pandas scipy scikit-learn \
    polars pyarrow statsmodels xgboost lightgbm catboost \
    matplotlib seaborn plotly \
    bokeh altair \
    jupyter ipython \
    jupyterlab notebook \
    requests beautifulsoup4 lxml \
    sqlalchemy psycopg2-binary \
    pymysql redis pymongo duckdb \
    openpyxl xlsxwriter odfpy python-docx reportlab \
    pdfplumber pypdf pdf2image pytesseract \
    opencv-python-headless pillow \
    shapely geopandas folium \
    networkx sympy \
    fastparquet tabulate \
    pyyaml toml jsonlines \
    tqdm rich

COPY . .
RUN pip install --no-cache-dir .

RUN useradd -m user && echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER user
WORKDIR /home/user

EXPOSE 8000

COPY entrypoint.sh /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["run"]
