# Dulce Hair — Landing Page

Landing page de página única para o salão **Dulce Hair** (São Paulo), construída
para receber tráfego pago (Meta Ads e Google Ads) com conversão em **agendamento
pelo WhatsApp**.

HTML, CSS e JavaScript puros — sem build, sem framework, sem dependência externa.
É só subir a pasta em qualquer hospedagem estática.

---

## ⚠️ Antes de subir a campanha — o que precisa ser trocado

A página está completa, mas alguns dados são **placeholders**. Nada disso pode ir
ao ar como está.

| # | O quê | Onde |
|---|---|---|
| 1 | **Número do WhatsApp** (`5511999999999`) | `index.html` → bloco `window.DULCE`, no `<head>` |
| 2 | **Endereço completo e CEP** | `index.html` → seção `#localizacao`, rodapé e JSON-LD |
| 3 | **Horário de atendimento** | `index.html` → seção `#localizacao`, rodapé e JSON-LD |
| 4 | **Depoimentos** — hoje são caixas vazias marcadas | `index.html` → seção `#depoimentos` |
| 5 | **Números da faixa de credibilidade** (5.000+ cortes, 12 anos, nota 5,0, 90% de retorno) | `index.html` → seção `.credbar` e selos do hero |
| 6 | **Fotos reais** do salão, da equipe e dos trabalhos | `assets/img/` (ver abaixo) |
| 7 | **Domínio** nas tags `canonical`, `og:url`, `og:image` e no JSON-LD | `index.html` → `<head>` |
| 8 | **IDs de pixel** (Meta / GA4 / Google Ads) | `index.html` → bloco `window.DULCE` |
| 9 | **Endereço do mapa** (parâmetro `q=` do iframe e do link) | `index.html` → seção `#localizacao` |

Todos esses pontos estão marcados no código com o comentário `⚠️ TROCAR`.
Buscar por `TROCAR` no `index.html` encontra tudo.

---

## Configuração

Tudo que a página precisa saber está num único bloco no `<head>` do `index.html`:

```js
window.DULCE = {
  whatsapp: '5511999999999',   // DDI + DDD + número, só dígitos
  mensagem: 'Olá! Vim pelo site da Dulce Hair e gostaria de agendar um horário.',
  metaPixelId: '',             // '123456789012345'
  ga4Id: '',                   // 'G-XXXXXXXXXX'
  googleAdsId: '',             // 'AW-XXXXXXXXX'
  googleAdsConversionLabel: '' // 'abcDEFghIJklMNop'
};
```

Os campos de rastreamento vazios simplesmente não carregam nada — a página
funciona normalmente sem eles.

### Como os links de WhatsApp funcionam

O JavaScript monta o `https://wa.me/...` de todos os botões a partir do número
configurado e ainda **anexa a origem do clique e os parâmetros da campanha** na
mensagem. Um lead que veio de um anúncio chega assim:

```
Olá! Vim pelo site da Dulce Hair e gostaria de agendar um horário.

(origem: hero · source: meta · campaign: cortes-jul · fbclid: IwAR...)
```

Dá para saber, direto na conversa, qual anúncio e qual botão trouxeram a cliente.

---

## Rastreamento e conversões

Cada clique em botão de WhatsApp dispara, nas plataformas configuradas:

- **Meta Pixel** → evento `Contact`, com o nome do botão em `content_name`
- **GA4** → evento `generate_lead` (`method: whatsapp`, `origem: <botão>`)
- **Google Ads** → evento `conversion` (só se `googleAdsConversionLabel` estiver preenchido)
- **dataLayer** → `clique_whatsapp` (para quem usa Google Tag Manager)

Os identificadores de origem (`data-cta`) são: `header`, `hero`, `servicos`,
`banda-central`, `localizacao`, `mapa`, `final`, `rodape`, `rodape-link`,
`flutuante` e `barra-mobile`.

> Para Meta, o ideal é complementar com a **API de Conversões** no lado do
> servidor — o pixel sozinho perde eventos no iOS.

---

## Imagens

As imagens em `assets/img/` (exceto o logo) são **texturas provisórias** geradas
por código: fios de cabelo iluminados em luz dourada, no tom da marca. Elas
existem para a página não ter buracos até as fotos reais entrarem.

**Substitua todas por fotos reais do salão.** Mantenha os mesmos nomes de arquivo
e proporções aproximadas e nada mais precisa ser mexido:

| Arquivo | Proporção | O que deve ser |
|---|---|---|
| `hero.jpg` / `.webp` | 3:4 (retrato) | Foto principal — cliente com o cabelo pronto, luz quente, fundo escuro |
| `servico-corte.jpg` | 1:1 | Detalhe de corte / tesoura em ação |
| `servico-cor.jpg` | 1:1 | Resultado de coloração ou mechas |
| `servico-tratamento.jpg` | 1:1 | Brilho do fio após tratamento |
| `ambiente.jpg` | 4:5 (retrato) | Interior do salão |
| `galeria-1.jpg` | 3:4 | Trabalho realizado |
| `galeria-2.jpg` | 3:4 | Trabalho realizado |
| `galeria-3.jpg` | 3:5 (mais alta) | Trabalho realizado — é a foto grande do mosaico |
| `og-image.jpg` | 1200×630 | Imagem de compartilhamento (WhatsApp, Facebook) |

Cada `<picture>` no HTML busca o `.webp` primeiro e cai para o `.jpg`. Se você só
tiver JPG, apague a linha `<source ... type="image/webp">` correspondente — ou
converta as fotos para WebP, que carrega mais rápido e ajuda o custo por clique.

Para regenerar as texturas provisórias (precisa de Python e Pillow):

```bash
python3 scripts/generate-textures.py
```

---

## Como rodar localmente

```bash
python3 -m http.server 8000
# abra http://localhost:8000
```

Abrir o `index.html` direto pelo `file://` também funciona, mas o mapa e as
fontes se comportam melhor servidos por HTTP.

## Como publicar

É um site estático. Sobe em qualquer lugar — Vercel, Netlify, Cloudflare Pages,
GitHub Pages ou hospedagem tradicional via FTP. Basta enviar a pasta inteira
(`index.html` + `assets/`) para a raiz do domínio.

Depois de publicar, vale conferir:

- [ ] Todos os botões abrem a conversa certa no WhatsApp (teste pelo celular)
- [ ] O pixel dispara (Meta Events Manager / GA4 DebugView / Tag Assistant)
- [ ] O mapa carrega no endereço correto
- [ ] A imagem de compartilhamento aparece — teste em
      [developers.facebook.com/tools/debug](https://developers.facebook.com/tools/debug/)
- [ ] Nota do PageSpeed Insights no mobile

---

## Estrutura

```
index.html                    página inteira + configuração + dados estruturados
assets/
  css/style.css               design system e todos os estilos
  js/main.js                  WhatsApp, rastreamento, FAQ, animações
  fonts/                      Jost, Inter e Cormorant Garamond (self-hosted)
  img/                        logo, hero, serviços, galeria, og-image
scripts/
  generate-textures.py        gerador das texturas provisórias
```

## Decisões técnicas

- **Fontes self-hosted.** Nada de Google Fonts em produção: elimina duas
  conexões externas e melhora o LCP, que é o que mais pesa no custo de tráfego pago.
- **Sem framework.** A página inteira são três arquivos. Menos JavaScript é menos
  tempo até o primeiro clique no botão.
- **Imagem do hero com `preload` e `fetchpriority="high"`**, o resto com
  `loading="lazy"`.
- **Dados estruturados** `HairSalon` e `FAQPage` — a página também trabalha para
  o resultado orgânico e para o perfil do Google.
- **Acessibilidade**: navegação por teclado, `aria-expanded` no FAQ, link de pular
  para o conteúdo e respeito a `prefers-reduced-motion`.

## Estrutura da página (e por que ela é assim)

1. **Hero** — promessa + prova social + CTA acima da dobra
2. **Faixa de números** — credibilidade em três segundos
3. **Problema** — identificação com a dor (framework PAS)
4. **Serviços** — o que é oferecido, com a especialidade em destaque
5. **Método** — quebra a objeção de "e se eu não gostar?"
6. **Resultados** — prova visual
7. **Diferenciais** — por que aqui e não no salão da esquina
8. **Depoimentos** — prova social de terceiros
9. **CTA intermediário** — escassez real (agenda por horário)
10. **Localização** — quebra a objeção de distância
11. **FAQ** — quebra as objeções que sobraram, inclusive preço
12. **CTA final** — última chamada

O botão de WhatsApp aparece 11 vezes ao longo da rolagem, mais o botão flutuante
no desktop e a barra fixa no mobile.
