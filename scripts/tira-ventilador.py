#!/usr/bin/env python3
"""
Remove o ventilador de parede da foto do salão.

O fundo ali é parede lisa, então não precisa de IA: a região é preenchida
resolvendo a equação de Laplace (média iterativa dos vizinhos) com as bordas
fixas na parede em volta. Numa superfície com iluminação suave isso reconstrói
o degradê sem emenda visível. No fim entra um grão leve, para o trecho não
ficar liso demais perto do ruído do resto da foto.
"""

import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(BASE, 'fotos', 'salao.jpg')
SAIDA = os.path.join(BASE, 'fotos', 'salao-sem-ventilador.jpg')

# Região do ventilador na foto de 1600x1200
GRADE = (1126, 264, 116, 108)          # centro x, centro y, raio x, raio y
SUPORTE = (1180, 275, 1262, 362)       # braço e base presos na parede


def mascara(tamanho):
    m = Image.new('L', tamanho, 0)
    d = ImageDraw.Draw(m)
    cx, cy, rx, ry = GRADE
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    d.rectangle(SUPORTE, fill=255)
    # borda suave evita emenda dura no encontro com a parede
    return m.filter(ImageFilter.GaussianBlur(7))


def preenche(img, m, passos=3000):
    a = np.asarray(img, dtype=np.float64)
    buraco = np.asarray(m, dtype=np.float64)[..., None] / 255.0

    # começa com a média da parede em volta, para convergir mais rápido
    borda = (buraco[..., 0] > 0.02) & (buraco[..., 0] < 0.98)
    semente = a[borda].mean(axis=0) if borda.any() else a.mean(axis=(0, 1))
    x = a * (1 - buraco) + semente * buraco

    dentro = buraco[..., 0] > 0.02
    ys, xs = np.where(dentro)
    y0, y1 = ys.min() - 2, ys.max() + 3
    x0, x1 = xs.min() - 2, xs.max() + 3

    janela = x[y0:y1, x0:x1].copy()
    fixo = a[y0:y1, x0:x1]
    peso = buraco[y0:y1, x0:x1]

    for _ in range(passos):
        vizinhos = np.empty_like(janela)
        vizinhos[1:-1, 1:-1] = (
            janela[:-2, 1:-1] + janela[2:, 1:-1] +
            janela[1:-1, :-2] + janela[1:-1, 2:]
        ) / 4.0
        vizinhos[0] = janela[0]; vizinhos[-1] = janela[-1]
        vizinhos[:, 0] = janela[:, 0]; vizinhos[:, -1] = janela[:, -1]
        # fora do buraco a foto original manda; dentro, vale a média dos vizinhos
        janela = fixo * (1 - peso) + vizinhos * peso

    x[y0:y1, x0:x1] = janela
    return x, dentro


def grao(x, dentro, forca=2.2, seed=5):
    rng = random.Random(seed)
    h, w = dentro.shape
    ruido = np.array([[rng.gauss(0, forca) for _ in range(w)] for _ in range(h)])
    return x + ruido[..., None] * dentro[..., None]


def main():
    img = Image.open(ENTRADA).convert('RGB')
    m = mascara(img.size)
    x, dentro = preenche(img, m)
    x = grao(x, dentro)
    Image.fromarray(np.clip(x, 0, 255).astype(np.uint8)).save(SAIDA, quality=95, subsampling=0)
    print('gravado:', SAIDA)


if __name__ == '__main__':
    main()
