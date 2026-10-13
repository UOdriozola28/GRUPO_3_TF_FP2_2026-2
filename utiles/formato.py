def recortar(texto, largo):
    resultado = ""
    for letra in texto:
        if len(resultado) < largo:
            resultado = resultado + letra
    return resultado
