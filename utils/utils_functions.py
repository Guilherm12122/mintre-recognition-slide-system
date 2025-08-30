# LOCALIZADOR DE ENTRADAS DE AÚDIO VÁLIDAS

# >>> import speech_recognition as sr
# >>>
# >>> r = sr.Recognizer()
# >>>
# >>> for idx in [0, 4, 5, 11, 12]:
# ...     try:
# ...         print(f"\n🎤 Testando device_index={idx}")
# ...         with sr.Microphone(device_index=idx) as source:
# ...             r.adjust_for_ambient_noise(source, duration=1)
# ...             print("Fale algo por 3 segundos...")
# ...             audio = r.listen(source, timeout=3, phrase_time_limit=3)
# ...         print("Áudio capturado com sucesso!")
# ...     except Exception as e:
# ...         print(f"Falhou no {idx}: {e}")
