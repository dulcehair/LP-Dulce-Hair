# Dulce Hair — Landing Page

Landing page de página única para o salão **Dulce Hair** (São Paulo), construída
para receber tráfego pago (Meta Ads e Google Ads) com conversão em **agendamento
pelo WhatsApp**.

As duas ofertas em foco são **progressiva sem formol** e **corte**. A página é
uma só, mas o topo se adapta ao anúncio que trouxe a visita — ver
[Uma página, duas campanhas](#uma-página-duas-campanhas).

HTML, CSS e JavaScript puros — sem build, sem framework, sem dependência externa.
É só subir a pasta em qualquer hospedagem estática.

---

## ⚠️ Antes de subir a campanha — o que precisa ser trocado

A página está completa, mas alguns dados são **placeholders**. Nada disso pode ir
ao ar como está.

| # | O quê | Onde |
|---|---|---|
| ~~1~~ | ~~**Número do WhatsApp**~~ — preenchido: `5511985969542` | `index.html` → bloco `window.DULCE`, no `<head>` |
| ~~2~~ | ~~**Endereço completo e CEP**~~ — preenchido: Estr. do M'Boi Mirim, 2207 — Jardim das Flores, São Paulo/SP, 04905-022 | `index.html` → seção `#localizacao`, rodapé e JSON-LD |
| ~~3~~ | ~~**Horário de atendimento**~~ — preenchido: terça a sábado, 09h às 18h | `index.html` → seção `#localizacao`, rodapé e JSON-LD |
| 4 | **Depoimentos** — hoje são caixas vazias marcadas | `index.html` → seção `#depoimentos` |
| 5 | **Números da faixa de credibilidade** (12 anos, nota 5,0, 5.000+ atendimentos) | `index.html` → seção `.credbar` e selos do hero |
| 5b | **Produto da progressiva**: linha/marca usada e número de registro na Anvisa (a duração — até 3 meses — já está confirmada) | `index.html` → seção `#progressiva` e FAQ |
| 6 | **Fotos reais** do salão, da equipe e dos trabalhos | `assets/img/` (ver abaixo) |
| 7 | **Domínio** nas tags `canonical`, `og:url`, `og:image` e no JSON-LD | `index.html` → `<head>` |
| 8 | **IDs de pixel** (Meta / GA4 / Google Ads) | `index.html` → bloco `window.DULCE` |
| ~~9~~ | ~~**Endereço do mapa**~~ — preenchido | `index.html` → seção `#localizacao` |

Os pontos que ainda faltam estão marcados no código com o comentário `⚠️`.
Buscar por `⚠️` no `index.html` encontra todos.

**Faltam:** depoimentos reais (4), conferir os números da faixa de
credibilidade (5), confirmar o produto da progressiva (5b), fotos reais (6),
domínio (7) e IDs de pixel (8).

> **Sobre a alegação "sem formol".** A página afirma que o alisamento é feito com
> ativos sem formol e com registro na Anvisa. Isso precisa corresponder exatamente
> ao produto aplicado no salão — tanto o Meta quanto o Google reprovam anúncio
> cuja promessa a página não sustenta, e a responsabilidade pela alegação é do
> anunciante. Confirme a linha usada e guarde o registro antes de subir.

---

## Uma página, duas campanhas

Anúncio de progressiva e anúncio de corte falam de coisas diferentes. Em vez de
manter duas páginas, o topo da página se ajusta à oferta que trouxe a visita —
é o parâmetro `?oferta=` na URL de destino do anúncio:

| URL de destino | O que muda |
|---|---|
| `.../` | Texto padrão, cobrindo as duas ofertas |
| `.../?oferta=progressiva` | Título, subtítulo, botão e mensagem do WhatsApp voltados à progressiva sem formol |
| `.../?oferta=corte` | Mesma coisa, voltado ao corte |

Exemplo de URL para o anúncio de progressiva no Meta:

```
https://www.dulcehair.com.br/?oferta=progressiva&utm_source=meta&utm_medium=cpc&utm_campaign=progressiva-sem-formol
```

O restante da página (comparativo com formol × sem formol, corte, serviços, FAQ)
continua igual nos dois casos — quem clicou no anúncio de progressiva encontra a
seção dela logo abaixo do hero, e quem veio pelo corte encontra a dele em seguida.

Um valor desconhecido em `?oferta=` é ignorado e a página mostra o texto padrão.
Para criar ou editar as variações, mexa na lista `OFERTAS` no início de
`assets/js/main.js`.

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

Os identificadores de origem (`data-cta`) são: `header`, `hero`,
`hero-progressiva`, `hero-corte`, `progressiva`, `corte`, `servicos`,
`banda-central`, `localizacao`, `mapa`, `final`, `rodape`, `rodape-link`,
`flutuante` e `barra-mobile`.

Os botões dentro das seções de progressiva e de corte já abrem a conversa no
assunto certo, mesmo que a visita não tenha vindo pelo link da campanha.

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
| `progressiva.jpg` | 4:5 (retrato) | **Resultado de progressiva** — é a foto da seção principal da oferta |
| `servico-progressiva.jpg` | 1:1 | Detalhe de fio alinhado (aparece na galeria) |
| `servico-corte.jpg` | 1:1 | Detalhe de corte / tesoura em ação |
| `servico-cor.jpg` | 1:1 | Resultado de coloração ou mechas |
| `servico-tratamento.jpg` | 1:1 | Brilho do fio após tratamento |
| `ambiente.jpg` | 4:5 (retrato) | Interior do salão |
| `galeria-1.jpg` | 3:4 | Trabalho realizado |
| `galeria-2.jpg` | 3:4 | Trabalho realizado |
| `galeria-3.jpg` | 3:5 (mais alta) | Trabalho realizado — é a foto grande do mosaico |
| `og-image.jpg` | 1200×630 | Imagem de compartilhamento (WhatsApp, Facebook) |

Para a progressiva, foto de **antes e depois** converte bem mais do que foto só do
depois — vale usar uma dessas em `progressiva.jpg` e outra na galeria.

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
- [ ] As URLs `?oferta=progressiva` e `?oferta=corte` trocam o topo da página
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

1. **Hero** — promessa + prova social + CTA acima da dobra (muda por campanha)
2. **Faixa de números** — credibilidade em três segundos
3. **Progressiva sem formol** — a oferta principal, com o comparativo
   *com formol × sem formol* que resolve a objeção central, e as pílulas de
   "indicada para" (cacheado, com luzes, com química…) que dizem à leitora que
   o serviço serve para o cabelo dela
4. **Corte** — a segunda oferta, entrando pela dor (framework PAS)
5. **Serviços** — o resto do cardápio, com as duas especialidades no topo
6. **Método** — inclui o teste de mecha, que é o que sustenta a promessa da
   progressiva; quebra a objeção de "e se estragar meu cabelo?"
7. **Resultados** — prova visual
8. **Diferenciais** — por que aqui e não no salão da esquina
9. **Depoimentos** — prova social de terceiros
10. **CTA intermediário** — escassez real (agenda por horário)
11. **Localização** — quebra a objeção de distância
12. **FAQ** — objeções restantes: alisa mesmo? quanto dura? funciona no meu
    cabelo? posso fazer grávida? e o preço?
13. **CTA final** — última chamada

O botão de WhatsApp aparece 11 vezes ao longo da rolagem, mais o botão flutuante
no desktop e a barra fixa no mobile.
