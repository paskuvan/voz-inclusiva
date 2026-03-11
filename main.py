from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from tts_service import TTSService
from languages import IDIOMAS

app = FastAPI(title="Voz Inclusiva API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: pon tu dominio exacto
    allow_methods=["*"],
    allow_headers=["*"],
)

service = TTSService()


class TTSRequest(BaseModel):
    texto: str
    variante: str = "es-MX"
    lento: bool = False
    formato: str = "mp3"

    @validator("texto")
    def texto_no_vacio(cls, v):
        if not v.strip():
            raise ValueError("El texto no puede estar vacío")
        if len(v) > 1000:
            raise ValueError("Máximo 1000 caracteres")
        return v.strip()

    @validator("variante")
    def variante_valida(cls, v):
        if v not in IDIOMAS:
            raise ValueError(f"Variante no soportada: {v}")
        return v


@app.get("/")
def root():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/idiomas")
def listar_idiomas():
    """Retorna todos los idiomas disponibles."""
    return [{"id": k, **v} for k, v in IDIOMAS.items()]


@app.post("/tts")
def generar_voz(req: TTSRequest):
    """Convierte texto a audio y lo devuelve como stream MP3."""
    config = IDIOMAS[req.variante]

    try:
        buffer = service.generar_audio(
            texto=req.texto,
            lang=config["lang"],
            tld=config["tld"],
            lento=req.lento,
            formato=req.formato,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    filename = f"voz-inclusiva.{req.formato}"
    media_type = "audio/mpeg" if req.formato == "mp3" else "audio/wav"

    return StreamingResponse(
        buffer,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )