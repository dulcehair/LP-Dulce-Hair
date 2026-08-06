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
| ~~4~~ | ~~**Depoimentos**~~ — três avaliações reais do Google no ar | `index.html` → seção `#depoimentos` |
| ~~5~~ | ~~**Números da faixa**~~ — +7 anos e 5.000+ atendimentos informados pelo salão; nota 4,8 e 29 avaliações conferem com o Perfil da Empresa | `index.html` → seção `.credbar` |
| 5c | **Serviços de unha** — confirmar quais entram no cartão de nail design (alongamento? gel? fibra?) e ajustar o texto | `index.html` → seção `#servicos` |
| 5b | **Produto da progressiva**: linha/marca usada e número de registro na Anvisa (a duração — até 3 meses — já está confirmada) | `index.html` → seção `#progressiva` e FAQ |
| ~~6~~ | ~~**Fotos reais**~~ — três trabalhos já no ar; falta foto do interior do salão | `assets/img/` (ver abaixo) |
| 7 | **Domínio** nas tags `canonical`, `og:url`, `og:image` e no JSON-LD | `index.html` → `<head>` |
| 8 | **IDs de pixel** (Meta / GA4 / Google Ads) | `index.html` → bloco `window.DULCE` |
| ~~9~~ | ~~**Endereço do mapa**~~ — preenchido | `index.html` → seção `#localizacao` |

Os pontos que ainda faltam estão marcados no código com o comentário `⚠️`.
Buscar por `⚠️` no `index.html` encontra todos.

**Faltam:** confirmar o produto da progressiva (5b), os serviços de unha (5c),
foto do interior do salão (6), o domínio (7) e os IDs de pixel (8).

### O bloco do mapa

Sobre o mapa fica um cartão fixo com o nome do salão, o endereço, a nota do
Google e dois botões: **Como chegar** (abre o Google Maps) e **Chamar Uber**.

O embed do Google não é carregado junto com a página. Quando a seção se aproxima
da tela, o JavaScript testa se o navegador alcança o Google:

- **Alcança** (caso normal): o mapa é inserido e aparece sozinho, sem clique.
- **Não alcança** (extensão de privacidade, rede corporativa, prévia): fica o
  fundo quadriculado com o cartão por cima e um botão "Ver o mapa", que carrega
  o embed na marra. Assim existe sempre um caminho manual, e ninguém vê a tela
  de erro cinza que o iframe desenha quando é bloqueado.

De quebra, a página não paga o peso do Google Maps no carregamento inicial, o
que ajuda no custo por clique.

### Como chegar e Chamar Uber

As coordenadas do salão ficam em `window.DULCE.local` e alimentam os dois
botões, para nunca apontarem para pontos diferentes:

- **Como chegar** abre a rota no Google Maps já traçada até o ponto exato.
- **Chamar Uber** usa o link universal (`m.uber.com/ul/`): abre o app com o
  destino preenchido e cai no site quando o app não está instalado.

Se o ponto mudar, troque só as coordenadas na configuração. Para pegá-las de
novo: no Google Maps, clique com o botão direito sobre o ponto e o primeiro item
do menu são as coordenadas.

Os dois cliques são rastreados como conversão, com origem `mapa-rota` e `uber`.

### Sobre as avaliações

A nota (4,8) e o número de avaliações (29) vêm do Perfil da Empresa no Google e
aparecem no topo e na faixa de credibilidade. Se esses números mudarem, atualize
os dois lugares.

Os três depoimentos são avaliações reais, copiadas na íntegra. **Ao trocar ou
acrescentar, mantenha o texto exatamente como a cliente escreveu.**

Não há marcação `aggregateRating` nos dados estruturados, e isso é proposital: o
Google não aceita que um site marque a própria nota vinda de avaliações de
terceiros, e fazer isso pode render uma ação manual.

### Uma tarefa fora do código

O Perfil da Empresa no Google hoje aponta o campo "site" para
`sites.appbeleza.com.br`. Quando esta página estiver no ar, troque o link lá —
é tráfego qualificado e gratuito caindo na página errada.

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
  whatsapp: '5511985969542',   // DDI + DDD + número, só dígitos
  mensagem: 'Olá! Vim pelo site da Dulce Hair e gostaria de agendar um horário.',
  local: {                     // alimenta "Como chegar" e "Chamar Uber"
    lat: '-23.675781',
    lng: '-46.752993',
    nome: 'Dulce Hair',
    endereco: "Estrada do M'Boi Mirim, 2207 - Jardim das Flores, São Paulo - SP, 04905-022"
  },
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

A página usa **fotos reais do salão**, recortadas a partir de três originais:
o bob (duas fotos num arquivo só, de frente e de perfil), o chanel de bico e a
progressiva.

| Arquivo | Proporção | Onde aparece | Origem |
|---|---|---|---|
| `hero.jpg` / `.webp` | 1448×1086 | Fundo do topo, no desktop | progressiva |
| `hero-mobile.jpg` | 815×1086 | Fundo do topo, no celular | progressiva |
| `progressiva.jpg` | 4:5 | Seção da progressiva | progressiva |
| `corte.jpg` | 4:5 | Seção do corte | bob, de frente |
| `experiencia.jpg` | 4:5 | Seção "uma cliente por vez" | chanel de bico |
| `galeria-bob.jpg` | 3:5 | Galeria de resultados | bob, de perfil |
| `galeria-chanel.jpg` | 3:5 | Galeria de resultados | chanel de bico |
| `galeria-progressiva.jpg` | 1,15:1 | Galeria de resultados | progressiva |
| `og-image.jpg` | 1200×630 | Compartilhamento (WhatsApp, Facebook) | derivada do hero |

Com três originais, cada foto aparece em dois lugares da página, sempre em
enquadramentos diferentes e distantes um do outro. **Fotos novas resolvem isso** —
as que fariam mais diferença, em ordem:

1. **Interior do salão vazio.** É a única coisa que nenhuma das três mostra.
2. **Antes e depois de progressiva.** Converte bem mais do que foto só do depois.
3. **Um cacheado e uma coloração**, para a galeria ter tipos de cabelo diferentes.

Cada `<picture>` no HTML busca o `.webp` primeiro e cai para o `.jpg`. Se você só
tiver JPG, apague a linha `<source ... type="image/webp">` correspondente — ou
converta as fotos para WebP, que carrega mais rápido e ajuda o custo por clique.

O hero usa **duas versões da mesma foto**: uma deitada no desktop e uma em pé no
celular. Cortar uma foto deitada para uma tela em pé perderia justamente o cabelo.
Se trocar o hero, gere as duas.

O `scripts/generate-textures.py` ficou como reserva: gera fundos abstratos de fios
em luz dourada para quando faltar foto em algum espaço novo. Os arquivos saem com
o prefixo `textura-`, então rodar o script nunca sobrescreve uma foto real.

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
