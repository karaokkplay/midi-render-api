# Usa uma imagem Python leve e oficial
FROM python:3.11-slim

# PASSO 1: Instala a biblioteca de sistema FluidSynth
RUN apt-get update && apt-get install -y --no-install-recommends fluidsynth

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# PASSO 2: Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do seu projeto
COPY . .

# Expõe a porta que a API vai usar
EXPOSE 10000

# PASSO 3: Comando para ligar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
