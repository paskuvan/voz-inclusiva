from gtts import gTTS
from io import BytesIO


class TTSService:

    def generar_audio(
        self,
        texto: str,
        lang: str = "es",
        tld: str = "com.mx",
        lento: bool = False,
        formato: str = "mp3"
    ) -> BytesIO:
        """Genera audio desde texto y retorna un BytesIO."""
        tts = gTTS(text=texto, lang=lang, tld=tld, slow=lento)

        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        return buffer