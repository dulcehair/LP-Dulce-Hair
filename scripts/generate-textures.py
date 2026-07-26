#!/usr/bin/env python3
"""
Gera as texturas provisorias da landing page (fios de cabelo / seda em luz dourada).

Sao imagens de apoio, feitas para a pagina nao ficar com buracos enquanto as
fotos reais do salao nao entram. Substitua os arquivos em assets/img/ mantendo
os mesmos nomes e proporcoes e a pagina continua funcionando.

Uso:  python3 scripts/generate-textures.py
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")

INK = (11, 10, 9)

# Paleta de fios: do espresso ao champanhe
PALETTE = [
    (26, 18, 15),
    (46, 32, 24),
    (74, 52, 36),
    (110, 79, 50),
    (152, 113, 71),
    (193, 154, 102),
    (222, 190, 141),
    (243, 224, 190),
]


def flow(x, y, seed, scale):
    """Campo de direcao suave (soma de senoides) — da o balanco organico dos fios."""
    a = math.sin((x * 0.7 + seed * 13.1) / scale) * 1.15
    b = math.cos((y * 1.3 - seed * 7.7) / (scale * 1.7)) * 0.85
    c = math.sin((x * 0.35 + y * 0.55 + seed * 3.3) / (scale * 2.4)) * 1.4
    return a + b + c


def strands(
    w,
    h,
    count,
    seed=7,
    scale=260,
    direction="down",
    bright=1.0,
    spread=1.0,
    thickness=(1, 3),
):
    """Desenha um feixe de fios seguindo o campo de direcao."""
    rng = random.Random(seed)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    for i in range(count):
        # ponto de partida
        if direction == "down":
            x = rng.uniform(-w * 0.15, w * 1.15)
            y = rng.uniform(-h * 0.25, h * 0.35)
            step_x, step_y = 0.0, rng.uniform(5.0, 8.0)
        else:  # "right"
            x = rng.uniform(-w * 0.25, w * 0.35)
            y = rng.uniform(-h * 0.15, h * 1.15)
            step_x, step_y = rng.uniform(5.0, 8.0), 0.0

        # fios mais claros sao raros — sao eles que criam o brilho
        t = rng.random() ** 2.1
        idx = min(len(PALETTE) - 1, int(t * len(PALETTE)))
        r, g, b = PALETTE[idx]
        boost = bright * (0.55 + 0.45 * t)
        color = (
            min(255, int(r * boost)),
            min(255, int(g * boost)),
            min(255, int(b * boost)),
        )
        alpha = int(28 + 150 * (t ** 1.4))
        width = rng.randint(*thickness)

        length = rng.randint(int(max(w, h) * 0.45), int(max(w, h) * 1.25))
        pts = [(x, y)]
        drift = rng.uniform(-1.0, 1.0)
        steps = int(length / 6)

        for _ in range(steps):
            ang = flow(x, y, seed + i * 0.017, scale) * 0.36 * spread + drift * 0.05
            if direction == "down":
                x += math.sin(ang) * 6.0 + step_x
                y += step_y
            else:
                x += step_x
                y += math.sin(ang) * 6.0 + step_y
            pts.append((x, y))
            if x < -w * 0.4 or x > w * 1.4 or y < -h * 0.4 or y > h * 1.4:
                break

        if len(pts) > 1:
            draw.line(pts, fill=color + (alpha,), width=width, joint="curve")

    return layer


def radial(w, h, cx, cy, radius, color, strength=1.0):
    """Halo radial suave (usado como luz de recorte dourada)."""
    small = max(2, int(min(w, h) / 6))
    sw, sh = max(2, w // 6), max(2, h // 6)
    g = Image.new("L", (sw, sh), 0)
    px = g.load()
    rx, ry = cx * sw, cy * sh
    rr = radius * max(sw, sh)
    for yy in range(sh):
        for xx in range(sw):
            d = math.hypot(xx - rx, yy - ry) / rr
            v = max(0.0, 1.0 - d) ** 2.4
            px[xx, yy] = int(255 * v * strength)
    g = g.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(small / 8))
    tint = Image.new("RGB", (w, h), color)
    return tint, g


def vignette(img, strength=0.85):
    w, h = img.size
    sw, sh = max(2, w // 8), max(2, h // 8)
    mask = Image.new("L", (sw, sh), 0)
    px = mask.load()
    for yy in range(sh):
        for xx in range(sw):
            dx = (xx / sw - 0.5) * 2
            dy = (yy / sh - 0.5) * 2
            d = math.hypot(dx, dy) / 1.42
            px[xx, yy] = int(255 * min(1.0, d ** 2.1) * strength)
    mask = mask.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(w / 40))
    dark = Image.new("RGB", (w, h), INK)
    return Image.composite(dark, img, mask)


def grain(img, amount=7, seed=3):
    rng = random.Random(seed)
    w, h = img.size
    noise = Image.new("L", (w // 2, h // 2))
    noise.putdata([rng.randint(128 - amount, 128 + amount) for _ in range((w // 2) * (h // 2))])
    noise = noise.resize((w, h), Image.BILINEAR)
    return Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.09)


def compose(w, h, *, seed, count, glow, direction="down", scale=260, bright=1.0, blur_bloom=26):
    base = Image.new("RGB", (w, h), INK)

    # luz de fundo
    for cx, cy, radius, color, strength in glow:
        tint, mask = radial(w, h, cx, cy, radius, color, strength)
        base = Image.composite(tint, base, mask)

    base = base.convert("RGBA")

    # camada de fundo desfocada (profundidade)
    back = strands(w, h, int(count * 0.45), seed=seed + 91, scale=scale * 1.5,
                   direction=direction, bright=bright * 0.6, spread=1.25, thickness=(2, 5))
    base.alpha_composite(back.filter(ImageFilter.GaussianBlur(w / 90)))

    # camada nitida
    front = strands(w, h, count, seed=seed, scale=scale, direction=direction,
                    bright=bright, spread=1.0, thickness=(1, 3))
    bloom = front.filter(ImageFilter.GaussianBlur(blur_bloom))
    base.alpha_composite(bloom)
    base.alpha_composite(front)

    # detalhe fino por cima
    fine = strands(w, h, int(count * 0.3), seed=seed + 404, scale=scale * 0.8,
                   direction=direction, bright=bright * 1.25, spread=0.85, thickness=(1, 1))
    base.alpha_composite(fine)

    out = base.convert("RGB")
    out = vignette(out, 0.8)
    return grain(out, seed=seed)


JOBS = [
    # hero — retrato, fios caindo com luz quente vinda da direita
    dict(name="hero", size=(1400, 1900), seed=11, count=1300, direction="down", scale=300,
         bright=1.05, glow=[(0.72, 0.24, 0.62, (150, 106, 58), 0.62),
                            (0.34, 0.78, 0.55, (60, 40, 28), 0.45)]),
    # servicos — quadrados
    dict(name="servico-corte", size=(1100, 1100), seed=23, count=620, direction="down", scale=210,
         bright=0.92, glow=[(0.62, 0.35, 0.66, (132, 92, 52), 0.55)]),
    dict(name="servico-cor", size=(1100, 1100), seed=37, count=680, direction="down", scale=245,
         bright=1.18, glow=[(0.4, 0.42, 0.72, (168, 124, 72), 0.6)]),
    dict(name="servico-tratamento", size=(1100, 1100), seed=59, count=760, direction="right",
         scale=230, bright=1.0,
         glow=[(0.5, 0.5, 0.7, (120, 86, 52), 0.55)]),
    # ambiente — retrato (equilibra a coluna de texto ao lado)
    dict(name="ambiente", size=(1280, 1600), seed=71, count=900, direction="right", scale=320,
         bright=0.88, glow=[(0.28, 0.4, 0.6, (128, 90, 52), 0.5),
                            (0.82, 0.62, 0.5, (92, 64, 40), 0.4)]),
    # galeria — 3 retratos
    dict(name="galeria-1", size=(1000, 1340), seed=83, count=620, direction="down", scale=260,
         bright=0.95, glow=[(0.55, 0.3, 0.62, (130, 92, 54), 0.55)]),
    dict(name="galeria-2", size=(1000, 1340), seed=97, count=680, direction="down", scale=200,
         bright=1.15, glow=[(0.44, 0.5, 0.66, (170, 126, 74), 0.58)]),
    dict(name="galeria-3", size=(1000, 1670), seed=113, count=820, direction="down", scale=290,
         bright=1.0, glow=[(0.62, 0.36, 0.68, (140, 100, 58), 0.55)]),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for job in JOBS:
        w, h = job["size"]
        print(f"  gerando {job['name']} ({w}x{h})…")
        img = compose(w, h, seed=job["seed"], count=job["count"], glow=job["glow"],
                      direction=job["direction"], scale=job["scale"], bright=job["bright"])
        img.save(os.path.join(OUT, f"{job['name']}.jpg"), quality=86, optimize=True, progressive=True)
        img.save(os.path.join(OUT, f"{job['name']}.webp"), quality=82, method=6)

    # og:image (1200x630) recortado do hero
    hero = Image.open(os.path.join(OUT, "hero.jpg"))
    hw, hh = hero.size
    crop_h = int(hw * 630 / 1200)
    top = int(hh * 0.22)
    og = hero.crop((0, top, hw, top + crop_h)).resize((1200, 630), Image.LANCZOS)
    logo = Image.open(os.path.join(OUT, "logo-dulce-hair.png")).convert("RGBA")
    lw = 520
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    og = og.convert("RGBA")
    og.alpha_composite(logo, ((1200 - lw) // 2, (630 - logo.height) // 2))
    og.convert("RGB").save(os.path.join(OUT, "og-image.jpg"), quality=88, optimize=True)
    print("  gerando og-image (1200x630)…")
    print("pronto.")


if __name__ == "__main__":
    main()
