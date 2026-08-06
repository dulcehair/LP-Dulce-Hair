/* ==========================================================================
   Dulce Hair — comportamento da landing page
   Sem dependências. Tudo lê a configuração de window.DULCE (definida no HTML).
   ========================================================================== */
(function () {
  'use strict';

  var CFG = window.DULCE || {};
  var doc = document;

  /* ------------------------------------------------------------------------
     0. Ofertas — message match entre o anúncio e o topo da página
     ------------------------------------------------------------------------
     A campanha manda o tráfego com ?oferta=progressiva ou ?oferta=corte e o
     hero se ajusta ao que o anúncio prometeu. Sem o parâmetro, fica o texto
     padrão que está no HTML (que cobre as duas ofertas).
     ------------------------------------------------------------------------ */
  var OFERTAS = {
    progressiva: {
      eyebrow: 'Progressiva sem formol · São Paulo',
      titulo: 'Liso sem cheiro,<br><span class="gold">sem formol.</span>',
      lead: 'Alisamento com ativos registrados na Anvisa e teste de mecha antes de qualquer aplicação. Você escolhe o resultado, do liso total ao só-tirar-o-volume, e leva um cabelo que continua saudável no fim.',
      cta: 'Quero minha progressiva',
      mensagem: 'Olá! Vim pelo site da Dulce Hair e quero saber sobre a progressiva sem formol.'
    },
    corte: {
      eyebrow: 'Corte assinatura · São Paulo',
      titulo: 'O corte certo<br><span class="gold">muda tudo.</span>',
      lead: 'Na Dulce Hair, o corte é desenhado para o seu rosto, o seu tipo de fio e a sua rotina, não para a foto que viralizou. Você sai daqui com um cabelo que continua bonito na segunda-feira de manhã.',
      cta: 'Quero agendar meu corte',
      mensagem: 'Olá! Vim pelo site da Dulce Hair e gostaria de agendar um corte.'
    }
  };

  var ofertaAtiva = null;

  function aplicaOferta(q) {
    var chave = String(q.oferta || '').toLowerCase();
    var o = OFERTAS[chave];
    if (!o) return;

    ofertaAtiva = chave;

    var alvos = {
      heroEyebrow: o.eyebrow,
      heroTitulo: o.titulo,
      heroLead: o.lead,
      heroCtaTexto: o.cta
    };
    Object.keys(alvos).forEach(function (id) {
      var el = doc.getElementById(id);
      if (el) el.innerHTML = alvos[id];
    });

    // o botão do hero passa a identificar a campanha no rastreamento
    var cta = doc.getElementById('heroCta');
    if (cta) cta.setAttribute('data-cta', 'hero-' + chave);
  }

  /* ------------------------------------------------------------------------
     1. Rastreamento — carrega só os pixels que tiverem ID preenchido
     ------------------------------------------------------------------------ */
  function loadScript(src, onload) {
    var s = doc.createElement('script');
    s.async = true;
    s.src = src;
    if (onload) s.onload = onload;
    doc.head.appendChild(s);
  }

  function initTracking() {
    // Meta Pixel (Facebook / Instagram Ads)
    if (CFG.metaPixelId) {
      /* eslint-disable */
      !(function (f, b, e, v, n, t, s) {
        if (f.fbq) return;
        n = f.fbq = function () {
          n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
        };
        if (!f._fbq) f._fbq = n;
        n.push = n; n.loaded = true; n.version = '2.0'; n.queue = [];
        t = b.createElement(e); t.async = true; t.src = v;
        s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
      })(window, doc, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      /* eslint-enable */
      window.fbq('init', CFG.metaPixelId);
      window.fbq('track', 'PageView');
    }

    // Google (GA4 e/ou Google Ads) — um único gtag.js atende os dois
    var gtagId = CFG.ga4Id || CFG.googleAdsId;
    if (gtagId) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag('js', new Date());
      if (CFG.ga4Id) window.gtag('config', CFG.ga4Id);
      if (CFG.googleAdsId) window.gtag('config', CFG.googleAdsId);
      loadScript('https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(gtagId));
    }
  }

  /** Dispara a conversão nas plataformas configuradas. */
  function trackLead(origem) {
    try {
      if (window.fbq) window.fbq('track', 'Contact', { content_name: origem });
      if (window.gtag) {
        window.gtag('event', 'generate_lead', { method: 'whatsapp', origem: origem });
        if (CFG.googleAdsId && CFG.googleAdsConversionLabel) {
          window.gtag('event', 'conversion', {
            send_to: CFG.googleAdsId + '/' + CFG.googleAdsConversionLabel
          });
        }
      }
      if (window.dataLayer) {
        window.dataLayer.push({ event: 'clique_whatsapp', origem: origem });
      }
    } catch (e) { /* rastreamento nunca pode quebrar a página */ }
  }

  /* ------------------------------------------------------------------------
     2. Links de WhatsApp — monta a URL e carrega a origem do clique
     ------------------------------------------------------------------------ */
  function paramsDaUrl() {
    var out = {};
    try {
      new URLSearchParams(location.search).forEach(function (v, k) { out[k] = v; });
    } catch (e) { /* navegador antigo */ }
    return out;
  }

  function montaLinks() {
    var numero = String(CFG.whatsapp || '').replace(/\D/g, '');
    if (!numero) return;

    var q = paramsDaUrl();
    // Anexa a origem do anúncio na mensagem — ajuda a saber de onde veio o lead
    var rastro = [];
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
      if (q[k]) rastro.push(k.replace('utm_', '') + ': ' + q[k]);
    });
    if (q.gclid) rastro.push('gclid: ' + q.gclid);
    if (q.fbclid) rastro.push('fbclid: ' + q.fbclid);

    // a mensagem padrão cede lugar à da oferta que trouxe a visita
    var base = (ofertaAtiva && OFERTAS[ofertaAtiva].mensagem) ||
      CFG.mensagem || 'Olá! Gostaria de agendar um horário.';

    Array.prototype.forEach.call(doc.querySelectorAll('[data-wa]'), function (el) {
      var origem = el.getAttribute('data-cta') || 'site';

      // Botão dentro de uma oferta específica já abre a conversa no assunto
      // certo, mesmo que a visita não tenha vindo pelo link da campanha.
      var doBotao = OFERTAS[origem.replace('hero-', '')];
      var texto = (doBotao ? doBotao.mensagem : base) +
        (rastro.length ? '\n\n(origem: ' + origem + ' · ' + rastro.join(' · ') + ')' : '');
      el.setAttribute('href', 'https://wa.me/' + numero + '?text=' + encodeURIComponent(texto));
      el.setAttribute('target', '_blank');
      el.setAttribute('rel', 'noopener');
      el.addEventListener('click', function () { trackLead(origem); });
    });
  }

  /* ------------------------------------------------------------------------
     3. Header fixo + barra mobile
     ------------------------------------------------------------------------ */
  function initScrollUI() {
    var header = doc.getElementById('header');
    var bar = doc.getElementById('mobileBar');
    var gatilho = Math.max(320, window.innerHeight * 0.6);
    var ticking = false;

    function atualiza() {
      var y = window.pageYOffset || doc.documentElement.scrollTop;
      if (header) header.classList.toggle('is-stuck', y > 40);
      if (bar) bar.classList.toggle('is-visible', y > gatilho);
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(atualiza); ticking = true; }
    }, { passive: true });

    window.addEventListener('resize', function () {
      gatilho = Math.max(320, window.innerHeight * 0.6);
    }, { passive: true });

    atualiza();
  }

  /* ------------------------------------------------------------------------
     4. Animação de entrada
     ------------------------------------------------------------------------ */
  function initReveal() {
    var itens = doc.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(itens, function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0 });

    Array.prototype.forEach.call(itens, function (el) { io.observe(el); });

    // Rede de segurança: num scroll muito rápido (ou num salto direto por
    // âncora) o observer pode não alcançar um bloco. Aqui garantimos que nada
    // fique invisível acima da dobra atual.
    function varreDobra() {
      Array.prototype.forEach.call(doc.querySelectorAll('.reveal:not(.is-in)'), function (el) {
        if (el.getBoundingClientRect().top < window.innerHeight) {
          el.classList.add('is-in');
          io.unobserve(el);
        }
      });
    }
    window.addEventListener('scroll', varreDobra, { passive: true });
    window.addEventListener('load', varreDobra);
  }

  /* ------------------------------------------------------------------------
     5. Contadores da faixa de credibilidade
     ------------------------------------------------------------------------ */
  function initContadores() {
    var nums = doc.querySelectorAll('[data-count]');
    if (!nums.length || !('IntersectionObserver' in window)) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var fmt = new Intl.NumberFormat('pt-BR');

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);

        var el = entry.target;
        var alvo = parseFloat(el.getAttribute('data-count'));
        var casas = parseInt(el.getAttribute('data-decimals') || '0', 10);
        var prefixo = el.getAttribute('data-prefix') || '';
        var sufixo = el.getAttribute('data-suffix') || '';
        var inicio = performance.now();
        var dur = 1400;

        function passo(agora) {
          var p = Math.min(1, (agora - inicio) / dur);
          var eased = 1 - Math.pow(1 - p, 3);
          var v = alvo * eased;
          el.textContent = prefixo +
            (casas ? v.toFixed(casas).replace('.', ',') : fmt.format(Math.round(v))) + sufixo;
          if (p < 1) requestAnimationFrame(passo);
        }
        requestAnimationFrame(passo);
      });
    }, { threshold: 0.5 });

    Array.prototype.forEach.call(nums, function (el) { io.observe(el); });
  }

  /* ------------------------------------------------------------------------
     6. FAQ (acordeão acessível)
     ------------------------------------------------------------------------ */
  function initFaq() {
    Array.prototype.forEach.call(doc.querySelectorAll('.faq__item'), function (item) {
      var btn = item.querySelector('.faq__q');
      var painel = item.querySelector('.faq__a');
      if (!btn || !painel) return;

      btn.addEventListener('click', function () {
        var aberto = item.classList.contains('is-open');

        // fecha os demais — mantém a leitura focada
        Array.prototype.forEach.call(doc.querySelectorAll('.faq__item.is-open'), function (outro) {
          if (outro === item) return;
          outro.classList.remove('is-open');
          outro.querySelector('.faq__q').setAttribute('aria-expanded', 'false');
          outro.querySelector('.faq__a').style.height = '0px';
        });

        item.classList.toggle('is-open', !aberto);
        btn.setAttribute('aria-expanded', String(!aberto));
        painel.style.height = aberto ? '0px' : painel.scrollHeight + 'px';
      });
    });

    // recalcula a altura do item aberto quando a tela muda de tamanho
    window.addEventListener('resize', function () {
      var aberto = doc.querySelector('.faq__item.is-open .faq__a');
      if (aberto) aberto.style.height = aberto.scrollHeight + 'px';
    }, { passive: true });
  }

  /* ------------------------------------------------------------------------
     6b. Mapa
     ------------------------------------------------------------------------
     O embed do Google só é carregado quando a seção se aproxima da tela e
     depois de um teste de alcance. Onde o Google está bloqueado (extensão de
     privacidade, rede corporativa, prévia), o iframe desenharia uma página de
     erro cinza por cima de tudo — melhor manter o endereço e o botão de rota.
     De quebra, a página não paga o embed do Google no carregamento inicial.
     ------------------------------------------------------------------------ */
  function initMapa() {
    var box = doc.querySelector('[data-mapa-src]');
    if (!box) return;

    function carrega() {
      if (box.querySelector('iframe')) return;
      var f = doc.createElement('iframe');
      f.title = 'Mapa da localização da Dulce Hair';
      f.loading = 'lazy';
      f.referrerPolicy = 'no-referrer-when-downgrade';
      f.allowFullscreen = true;
      f.src = box.getAttribute('data-mapa-src');
      box.appendChild(f);
      box.classList.add('mapa-carregado');
    }

    // Caminho manual: vale mesmo que o teste de alcance abaixo se engane.
    var botao = box.querySelector('[data-mapa-abrir]');
    if (botao) botao.addEventListener('click', carrega);

    function tenta() {
      try {
        fetch('https://maps.google.com/favicon.ico', { mode: 'no-cors', cache: 'no-store' })
          .then(carrega)
          .catch(function () { /* sem alcance: fica o endereço */ });
      } catch (e) { /* política de segurança estrita */ }
    }

    if (!('IntersectionObserver' in window)) { tenta(); return; }
    var io = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { io.disconnect(); tenta(); }
    }, { rootMargin: '400px' });
    io.observe(box);
  }

  /* ------------------------------------------------------------------------
     7. Âncoras com compensação do header fixo
     ------------------------------------------------------------------------ */
  function initAncoras() {
    Array.prototype.forEach.call(doc.querySelectorAll('a[href^="#"]'), function (link) {
      link.addEventListener('click', function (ev) {
        var id = link.getAttribute('href');
        if (!id || id === '#') return;
        var alvo = doc.querySelector(id);
        if (!alvo) return;
        ev.preventDefault();
        var header = doc.getElementById('header');
        var offset = header ? header.offsetHeight + 12 : 0;
        var y = alvo.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({
          top: y,
          behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
        });
      });
    });
  }

  /* ------------------------------------------------------------------------
     8. Início
     ------------------------------------------------------------------------ */
  function init() {
    var ano = doc.getElementById('ano');
    if (ano) ano.textContent = new Date().getFullYear();

    initTracking();
    aplicaOferta(paramsDaUrl());
    montaLinks();
    initScrollUI();
    initReveal();
    initContadores();
    initFaq();
    initMapa();
    initAncoras();
  }

  if (doc.readyState === 'loading') {
    doc.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
