#!/usr/bin/env python3
"""
Recorta as fotos reais do salão nos formatos que a página usa.

Os arquivos originais (fotos de câmera, sem tratamento) NÃO ficam neste
repositório — são pesados e não precisam de controle de versão. Este script
espera achá-los numa pasta `fotos/` ao lado dele; coloque ali os originais
antes de rodar. O resultado (os recortes já prontos) é o que fica versionado,
em assets/img/.
"""

import os
from PIL import Image

ORIG = os.path.dirname(os.path.abspath(__file__)) + '/fotos'
DEST = '/home/user/LP-Dulce-Hair/assets/img'

# (arquivo de origem, caixa de recorte, nome de saída)
CORTES = [
    # hero: o salão. Paisagem no desktop, retrato no celular.
    ('salao-sem-ventilador.jpg', None,            'hero'),
    ('salao-sem-ventilador.jpg', (700, 0, 1600, 1200), 'hero-mobile'),
    # seção da progressiva: foto de estúdio, painel direito (sorrindo, perfil)
    ('progressiva-estudio-dir.jpg', (0, 30, 640, 830),      'progressiva'),
    # galeria: painel central (olhar direto, sem marca d'água na área usada)
    ('progressiva-estudio-centro.jpg', (0, 0, 640, 830),    'galeria-progressiva'),
    # seção do corte: quadrado no rosto
    ('_esq.png',        (0, 0, 692, 865),         'corte'),
    # galeria: perfil do bob, 3:4
    ('_dir.png',        (0, 40, 670, 933),        'galeria-bob'),
    # seção "quem vai cuidar do seu cabelo": a profissional com a cliente
    ('profissional.jpg', (0, 0, 683, 854),        'equipe'),
    # galeria: chanel de bico, 3:4
    ('chanel.png',      (110, 40, 898, 1091),     'galeria-chanel'),
]


def separa_triptico():
    """O arquivo progressiva-estudio.jpg tem três fotos lado a lado, sem
    espaçamento entre elas. Recorta cada terço para um arquivo próprio antes
    dos cortes de CORTES poderem usá-los."""
    caminho = os.path.join(ORIG, 'progressiva-estudio.jpg')
    if not os.path.exists(caminho):
        return
    im = Image.open(caminho).convert('RGB')
    w, h = im.size
    terco = w // 3
    nomes = ('progressiva-estudio-esq.jpg', 'progressiva-estudio-centro.jpg', 'progressiva-estudio-dir.jpg')
    for i, nome in enumerate(nomes):
        im.crop((i * terco, 0, (i + 1) * terco, h)).save(os.path.join(ORIG, nome), quality=95)


def main():
    separa_triptico()
    for origem, caixa, nome in CORTES:
        im = Image.open(os.path.join(ORIG, origem)).convert('RGB')
        if caixa:
            im = im.crop(caixa)
        im.save(os.path.join(DEST, nome + '.jpg'), quality=88, optimize=True, progressive=True)
        im.save(os.path.join(DEST, nome + '.webp'), quality=82, method=6)
        print('  %-22s %s  (de %s)' % (nome, im.size, origem))

    # og:image — recorte do hero com o logo por cima
    hero = Image.open(os.path.join(DEST, 'hero.jpg'))
    hw, hh = hero.size
    alvo_h = int(hw * 630 / 1200)
    topo = max(0, (hh - alvo_h) // 2)
    og = hero.crop((0, topo, hw, topo + alvo_h)).resize((1200, 630), Image.LANCZOS)
    # escurece para o logo branco aparecer
    escuro = Image.new('RGB', (1200, 630), (11, 10, 9))
    og = Image.blend(og, escuro, 0.66)
    logo = Image.open(os.path.join(DEST, 'logo-dulce-hair.png')).convert('RGBA')
    lw = 480
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    og = og.convert('RGBA')
    og.alpha_composite(logo, ((1200 - lw) // 2, (630 - logo.height) // 2))
    og.convert('RGB').save(os.path.join(DEST, 'og-image.jpg'), quality=88, optimize=True)
    print('  %-22s (1200, 630)' % 'og-image')


if __name__ == '__main__':
    main()
