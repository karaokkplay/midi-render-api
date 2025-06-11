# Use a imagem base oficial do Python
FROM python:3.11-slim

# Passo 1: Instalar as dependências do sistema operacional
# Isso garante que a biblioteca C do FluidSynth esteja disponível
RUN apt-get update && apt-get install -y --no-install-recommends fluidsynth

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia primeiro o arquivo de dependências para aproveitar o cache do Docker
COPY requirements.txt .

# Passo 2: Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código da sua aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação vai rodar (o Render vai mapear isso)
EXPOSE 10000

# Passo 3: Define o comando para iniciar a aplicação
# Usa o mesmo Start Command que tínhamos antes
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
