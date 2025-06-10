from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import fluidsynth
import os
import tempfile

# --- Configuração ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
MIDI_DIR = os.path.join(STATIC_DIR, "midis")
SF2_PATH = os.path.join(STATIC_DIR, "sf2", "8Rock11e.sf2")

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="API de Renderização MIDI",
    description="Renderiza arquivos MIDI para áudio WAV usando FluidSynth."
)

@app.get("/render/{midi_filename}")
async def render_midi_endpoint(midi_filename: str):
    """
    Recebe o nome de um arquivo MIDI, renderiza para WAV e retorna o áudio.
    Este é o endpoint que sua página PHP vai chamar.
    """
    midi_path = os.path.join(MIDI_DIR, midi_filename)

    if not os.path.exists(midi_path):
        raise HTTPException(status_code=404, detail=f"Arquivo MIDI '{midi_filename}' não encontrado no servidor.")

    # Cria um arquivo temporário para a saída de áudio WAV
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        output_path = tmp_file.name

    try:
        # --- A MÁGICA ACONTECE AQUI ---
        fs = fluidsynth.Synth()
        # Configura para renderizar para um arquivo, sem tocar som no servidor
        fs.start(driver='file') 
        
        # Carrega o nosso SoundFont
        sfid = fs.sfload(SF2_PATH)
        fs.program_select(0, sfid, 0, 0)

        # Toca o MIDI, mas a saída vai direto para o arquivo WAV
        player = fluidsynth.Player(fs)
        player.play(midi_path)
        player.join(output_path) # Espera a renderização terminar e salva no arquivo

        # Libera os recursos do sintetizador
        fs.delete()
        
        # Retorna o arquivo de áudio gerado. 
        # O FastAPI garante que o arquivo temporário seja deletado após o envio.
        return FileResponse(output_path, media_type="audio/wav", filename=f"{os.path.splitext(midi_filename)[0]}.wav")

    except Exception as e:
        # Em caso de erro, limpa o arquivo temporário e retorna um erro 500
        if os.path.exists(output_path):
            os.unlink(output_path)
        raise HTTPException(status_code=500, detail=f"Erro durante a renderização: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "API de Renderização MIDI está funcionando! Use o endpoint /render/{nome_do_arquivo.mid}"}