<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licença MIT (ver o arquivo LICENSE) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-fold.png" alt="Omega-Fold" width="512">
</div>

#  OMEGA-FOLD

**Analisador de estrutura de sites/diretórios (local e remoto)**

> Desenvolvido por [kraynux](https://github.com/kraynux) para [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Página oficial: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Capturas de tela: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-uso)

🌐 Interface e relatórios exportados disponíveis em **17 idiomas** — veja [Idiomas da interface](#idiomas-da-interface).  
**Idiomas:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** é uma ferramenta TUI + CLI que analisa a estrutura de um diretório local ou de um site remoto (rastreamento HTTP limitado por salvaguardas): árvore completa, estatísticas por extensão/família de arquivo, mapa de links (internos/externos, de todos os tipos), detecção de links quebrados. Ferramenta da suíte `omega-`, estruturada em Clean Architecture — veja `docs/ARCHITECTURE.md` para todos os detalhes técnicos.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pt-BR/omega-fold/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pt-BR/omega-fold/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pt-BR/omega-fold/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pt-BR/omega-fold/D.png" width="24%" />
</p>

## 1. Visão e escopo

### O que o Omega-fold faz

- Escaneia um diretório local (`os.walk` real) ou rastreia um site remoto em largura (BFS), limitado por salvaguardas rígidas.
- Monta a árvore completa (arquivos/diretórios, profundidade, tamanho) e a classifica por família (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — veja [§4](#4-famílias-de-arquivos).
- Extrai todos os links (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) de cada página/arquivo HTML, classifica-os (interno absoluto/relativo, externo, âncora, `mailto:`/`tel:`/`javascript:`/`data:`) e verifica se existem — veja [§5](#5-links-e-verificação).
- Calcula estatísticas: distribuição por extensão/família, maiores arquivos, arquivos com mais links de saída, domínios externos mais referenciados.
- Apresenta o resultado em TUI (Textual) ou em CLI scriptável, com três exportações (JSON, texto, HTML com 5 temas).
- Mantém um histórico persistente de escaneamentos (SQLite), consultável e repetível.

### O que o Omega-fold não faz

- Análise de conteúdo ou de SEO (títulos, meta descrições, densidade de palavras-chave).
- Rastreamento sem salvaguardas — profundidade, número de páginas e intervalo entre requisições sempre ativos.
- Renderização de JavaScript no lado do cliente (a página é obtida como servida, não executada em um navegador headless).
- Varredura ativa de vulnerabilidades, fuzzing, força bruta.
- Painel web.

## 2. Instalação

### Pré-requisitos

- Python 3.10+
- Conexão com a Internet, para as dependências
- Para a TUI: uma fonte [Nerd Font](https://www.nerdfonts.com/) instalada no terminal, para o ícone do cabeçalho — sem ela, esse caractere aparece como um quadrado vazio (mesma limitação de um emoji, mas muito mais disponível entre os usuários de terminal). A ausência não afeta o funcionamento; é puramente estética.

### Instalação

```bash
[ -d omega-fold ] && echo "ℹ️ Já extraído aqui, etapa ignorada." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Cria o ambiente virtual `.venv` se ele ainda não existir.
2. Instala as dependências (`vendor/omega-lib/` e depois `pip install -e .`; `pyproject.toml` continua sendo a única fonte de verdade).
3. Torna `omega-fold.sh` e `install.sh` executáveis.
4. Adiciona o alias `fold` a `~/.bashrc` e `~/.zshrc` (sem duplicar se já existir).

### Dependências

Declaradas em `pyproject.toml` (sem `requirements.txt`):
- `omega-lib`: biblioteca compartilhada da suíte (temas de exportação, `ConfidenceLevel`) — incluída em `vendor/omega-lib/`
- `httpx`: verificação síncrona dos links externos (`LinkChecker`)
- `aiohttp`: rastreamento HTTP assíncrono (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: extração de links HTML
- `jinja2`: templates para a exportação HTML
- Dependências de desenvolvimento (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Uso

### Modo interativo (TUI)

Recomendado para o uso diário — iniciado sem argumentos:

```bash
./omega-fold.sh
```
se você criou o alias, basta digitar `fold` no terminal:
```bash
fold
```

Percurso: tela de abertura (fecha com uma tecla ou um clique) → menu principal (Escanear / Histórico / Configurações / Ajuda) → informar o alvo, o tipo (local/remoto), o modo (estático/dinâmico) e as salvaguardas do rastreamento remoto, cada campo com seu rótulo explícito → escaneamento (indicador indeterminado, registro das operações ao vivo, botão Cancelar a qualquer momento) → detalhe do escaneamento (distribuição por família e por extensão, árvore, links quebrados, exportação) → histórico (ver detalhe, **exportar diretamente** sem passar pelo detalhe, repetir) e configurações a partir do menu principal. A adaptação ao terminal (cores, tamanho, degradação estrutural) é automática.

#### Atalhos de teclado

| Tecla | Ação |
|---|---|
| `↑` / `↓` | Navegar entre os itens de uma tela |
| `Tab` / `Shift+Tab` | Navegar entre os campos de um formulário |
| `Esc` | Voltar à tela anterior (confirmação de saída na tela inicial) |
| `t` | Próximo tema (aplicado na hora, sem confirmação) |
| `r` | Atualizar a detecção do terminal |
| `a` | Mostrar a ajuda |
| `q` | Sair (com confirmação) |

### Idiomas da interface

A interface está disponível em 17 idiomas: francês, inglês, espanhol, português (Brasil), italiano, alemão, holandês, polonês, russo, chinês simplificado, vietnamita, tailandês, indonésio, japonês, coreano, hindi e árabe. A escolha é feita em Configurações («Langue / Language») e vale após reiniciar a interface; a variável `OMEGA_FOLD_LANG` (por exemplo `OMEGA_FOLD_LANG=pt-BR ./omega-fold.sh`) força um idioma durante uma sessão. Iniciado pelo omega-suite, o omega-fold usa o idioma da suíte. Em um console de texto Linux (TTY), os idiomas de escrita não latina aparecem em inglês durante a sessão. A linha de comando continua em francês.

### Contato e suporte

A ajuda (tecla `a`) oferece uma tela **Contato e suporte**: *Pagar um café* (página PayPal do desenvolvedor), *Contatar o suporte* (endereço de e-mail e formulário de contato do site, exibidos em claro), *Declarar-me usuário (anônimo)* e *Verificar atualizações*. A declaração é voluntária, desativada por padrão e enviada uma única vez: serve apenas para contar os usuários e, se desejado, seu continente ou país (listas fechadas, nunca texto livre). Ela envia uma chave sorteada ao acaso, o nome do software (`omega-fold`) e sua versão; nunca um nome, um nome de máquina, uma configuração, um alvo ou um resultado. O endereço IP não é registrado nas declarações, mas, como em qualquer visita, passa pelos controles de segurança e pelo registro do servidor de recepção. Retirada a qualquer momento na mesma tela (*Não me declarar mais*). A verificação de atualizações apenas lê a lista de versões publicadas no site, e nunca sem um clique.

### Modo scriptável (CLI)

Qualquer subcomando ativa o modo CLI:

```bash
# Escaneamento local (árvore + links internos)
./omega-fold.sh scan /var/www/meusite --type local

# Escaneamento local em modo dinâmico (verifica também os links externos por HTTP)
./omega-fold.sh scan /var/www/meusite --type local --mode dynamic

# Escaneamento remoto (rastreamento BFS a partir da URL inicial)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# Histórico (filtrável por alvo)
./omega-fold.sh history --target /var/www/meusite --limit 20

# Detalhe de um escaneamento (texto, JSON ou HTML) — 5 temas de exportação à escolha
./omega-fold.sh show <scan_id> --format html --theme omega-base --output relatorio.html
```

Opções de `scan`:

| Opção | Padrão | Efeito |
|---|---|---|
| `--type` | *(obrigatório)* | `local` ou `distant` (remoto) |
| `--mode` | `static` | `static` (links externos não verificados) ou `dynamic` (verificados por HTTP) |
| `--max-depth` | `5` | Profundidade máxima seguida (escaneamento remoto) |
| `--max-pages` | `1000` | Número máximo de páginas rastreadas (escaneamento remoto) |
| `--delay` | `100` | Intervalo (ms) entre duas requisições (escaneamento remoto) |
| `--user-agent` | `omega-fold/0.1` | Cabeçalho `User-Agent` enviado (escaneamento remoto) |
| `--respect-robots` | desativado | Respeita o `robots.txt` (escaneamento remoto) |

Em um escaneamento remoto, um alvo sem esquema (`example.org`) é completado automaticamente como `https://example.org` — não é preciso indicá-lo, exceto para forçar `http://` explicitamente.

Se o site tiver mais páginas que `--max-pages` (1000 por padrão), o escaneamento para no limite mas informa isso explicitamente: `scan.status` vale `completed_truncated` em vez de `completed`, com um aviso visível no resumo da CLI, na tela de detalhe da TUI e na exportação HTML — o número de arquivos informado não é então o tamanho real do site; execute de novo com um `--max-pages` maior para uma cobertura completa.

Se o alias foi criado pelo `install.sh`, `fold scan ...` funciona de qualquer lugar do terminal, sem o prefixo `./omega-fold.sh`.

## 4. Famílias de arquivos

Cada arquivo é classificado em uma família conforme sua extensão (vence a primeira correspondência) — detalhe completo e tabela extensão por extensão: `docs/FAMILIES.md`.

| Família | Exemplos de extensões |
|---|---|
| `images` | `.jpg`, `.png`, `.svg`, `.webp`, `.ico`... |
| `documents` | `.pdf`, `.doc`, `.xlsx`, `.odt`... |
| `code` | `.html`, `.php`, `.js`, `.ts`, `.py`, `.css`... |
| `data` | `.json`, `.xml`, `.yaml`, `.csv`, `.sql`... |
| `archives` | `.zip`, `.tar`, `.gz`, `.7z`... |
| `fonts` | `.ttf`, `.otf`, `.woff`, `.woff2`... |
| `video` | `.mp4`, `.webm`, `.mkv`... |
| `audio` | `.mp3`, `.wav`, `.flac`... |
| `text` | `.txt`, `.md`, `.rst`, `.log` |
| `other` | todo o resto |

## 5. Links e verificação

### Classificação

Cada link encontrado (`href`/`src`/`action`) é classificado, nesta ordem de prioridade:

| Tipo | Reconhecido quando | Exemplo |
|---|---|---|
| `empty` | String vazia | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Esquema especial | `mailto:x@y.z` |
| `anchor` | Começa diretamente com `#` (âncora pura) | `#section` |
| `external` | `http://`, `https://` ou `//` (relativo ao protocolo) | `https://example.org` |
| `absolute` | Começa com `/` | `/img/logo.png` |
| `relative` | Todo o resto | `img/logo.png`, `../page.html` |

`absolute` e `relative` são as duas formas de um link **interno** — um link `page.html#section` continua `relative` (o fragmento final não o transforma em simples âncora; ele navega de fato para outro recurso).

### Verificação

- **Link interno**: sempre verificado contra o conjunto de caminhos realmente encontrados durante o escaneamento (sem requisição de rede) — `absolute` resolvido a partir da raiz do escaneamento, `relative` com separador resolvido a partir do diretório do arquivo de origem, `relative` sem separador (só o nome do arquivo) procurado em toda a árvore. Em um escaneamento remoto, a verificação é feita em uma segunda passagem depois do rastreamento, contra o conjunto de páginas realmente visitadas com sucesso — uma página fora das salvaguardas ou bloqueada pelo `robots.txt` fica `unchecked`, nunca `broken` por suposição.
- **Link externo**: verificado por uma requisição HTTP (HEAD e depois GET se o HEAD falhar) somente no modo `dynamic` — no modo `static`, fica `unchecked`.

## 6. Salvaguardas do rastreamento remoto

Sempre ativas, nunca desativáveis — apenas seus limites são ajustáveis:

- **Profundidade** (`--max-depth`): limita apenas o enfileiramento de novas páginas a rastrear; os links encontrados em uma página já visitada sempre aparecem no resultado, mesmo que a página para a qual apontam não seja seguida.
- **Número de páginas** (`--max-pages`): limita o número total de páginas visitadas, em todas as profundidades.
- **Intervalo** (`--delay`): pausa entre duas requisições HTTP consecutivas.
- **Mesmo domínio**: só são seguidos os links internos para o mesmo `netloc` da URL inicial — verificado tanto no caminho do link quanto na URL **realmente carregada após o redirecionamento**: um permalink cujo caminho parece uma pasta interna (`/go/xyz`, `/public/nome/`) mas que na verdade redireciona para um domínio externo nunca é tratado como página do site escaneado (o conteúdo não seria o seu).
- **`robots.txt`** (`--respect-robots`): reforça as salvaguardas em vez de enfraquecê-las — uma página proibida nunca é visitada, seus links de saída ficam `unchecked`.

## 7. Arquitetura

O Omega-fold é estruturado em **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alinhada ao modelo da suíte `omega-` (veja `omega-scan`/`omega-check`/`omega-deep`) e verificada pelo `import-linter` a cada alteração. Todos os detalhes estão em **`docs/ARCHITECTURE.md`**.

Visão geral bem curta:

```text
src/omega_fold/
├── domain/          Lógica de negócio pura: escaneamentos, árvore (tree), links, estatísticas, relatórios
├── application/     Casos de uso (commands/queries) — run_scan (local/remoto), export_scan_report...
├── ports/           Contratos esperados pela aplicação (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Implementações concretas (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    exportadores Jinja2 — o Textual NÃO está aqui)
├── interfaces/      tui/ (Textual) e cli/ (scriptável), com paridade funcional estrita
├── app/             Montagem (DependencyContainer, bootstrap, ciclo de vida)
├── core/, shared/   Vocabulário transversal, utilitários fora do negócio
└── plugins/         Estrutura pronta, vazia (nenhum eixo de extensão confirmado)
```

Regras de design:
- `domain/tree/service.py`: agrega em árvore uma lista plana de arquivos já conhecida, nunca faz E/S — o percurso real (`os.walk`) fica em `infrastructure/filesystem/`.
- `domain/scans/policies.py`: salvaguardas de rastreamento (profundidade/páginas/domínio), lógica pura testável sem rede.
- `infrastructure/filesystem/` e `infrastructure/network/`: fazem a E/S (disco, HTTP), nunca julgam.
- `infrastructure/exporters/`: leem o resultado do escaneamento já montado, nunca recalculam uma estatística.
- `infrastructure/storage/sqlite/`: só armazena os dados de origem (`scans`/`files`/`links`) — a árvore e as estatísticas são recalculadas na leitura pelas mesmas funções puras do escaneamento inicial (veja `DECISIONS_ARCHITECTURE.md`, D-011), nunca duplicadas no banco.

## 8. Exportações

Os relatórios de texto e HTML são escritos no idioma escolhido em Configurações («Idioma das exportações», por padrão o da interface); o JSON continua sendo um dado, não traduzido. Os relatórios são gerados em `var/exports/` por padrão (caminho de execução ancorado na pasta do projeto, `$OMEGA_FOLD_VAR_DIR` para alterá-lo), ou no caminho indicado (`--output`).

### JSON, fonte de verdade

Estrutura completa do resultado (`Scan` + árvore + links + estatísticas), estritamente serializável em JSON.

### Texto, relatório legível compacto

Resumo, distribuição por família, árvore ASCII (limitada a 6 níveis de profundidade — um relatório de texto não foi feito para listar uma árvore de milhares de arquivos), lista de links quebrados.

### HTML, relatório web autônomo

5 temas à escolha (`--theme`). O tamanho total do site aparece em destaque primeiro (é o objetivo principal de um relatório de escaneamento) e é exibido em formato legível (KB/MB/GB...) em todo lugar — CLI, TUI, exportações — em vez de bytes brutos. Layout próprio: contêiner, grade de estatísticas, histograma SVG da distribuição por família (desenhado à mão, sem dependência pesada de gráficos — mesma técnica do diagrama de arquitetura do `omega-deep`), tabelas de extensões/maiores arquivos. Os domínios externos referenciados mostram os 20 primeiros diretamente e o restante em um painel recolhível (útil em um site com centenas de redirecionamentos externos); a lista de links quebrados aparece recolhida por padrão.

A árvore é renderizada em HTML nativo **multinível**: um `<details>` por diretório, só a raiz aberta por padrão, cada subpasta se expande de forma independente ao clicar (inspirado em um script de geração de índices do usuário) — um navegador só faz o layout do conteúdo aberto, então continua utilizável mesmo para um site com dezenas de milhares de arquivos, sem JavaScript.

## 9. Histórico

Cada escaneamento é salvo (SQLite, `var/db/omega-fold.db`). Histórico consultável por alvo (`omega-fold history --target ...`), detalhe de um escaneamento anterior (`omega-fold show <scan_id>`), ou pelo menu Histórico da TUI (repetição incluída).

## 10. Compatibilidade com terminais

A TUI (Textual) detecta automaticamente as capacidades do terminal (emulador, tamanho) e adapta sua folha de estilo estrutural de acordo (`complete`/`standard`/`reduced`/`mono`), sem opção manual. O modo CLI continua sempre em texto simples, independente do terminal. Política compartilhada por toda a suíte `omega-` (`omega-lib`, `terminal/policies.py`).

### Perfil conforme o emulador detectado

| Emulador | Perfil inicial |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH moderno | `reduced` |
| TTY Linux, SSH antigo | `mono` |
| Emulador não reconhecido | `reduced` (alternativa padrão) |

### Perfil conforme o tamanho do terminal

| Tamanho mínimo (colunas × linhas) | Teto de perfil |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| abaixo | `mono` |

O perfil final é **o mais restritivo dos dois** (emulador e tamanho) — atualizável ao vivo com a tecla `r`.

## 11. Testes

```bash
source .venv/bin/activate
lint-imports        # verifica a Dependency Rule (6 contratos)
pytest -q           # 186 testes
ruff check src tests
mypy -p omega_fold
```

Estrutura: `tests/unit/` (domínio e infraestrutura sem E/S real — exportadores, gráfico SVG, marcação da tela de abertura da TUI), `tests/integration/` (sistema de arquivos real via `tmp_path`, servidor HTTP falso `pytest-httpserver`, banco SQLite real, CLI de ponta a ponta), `tests/tui/` (navegação via `Pilot`, estrutural — sem verificação visual autodeclarada, veja `docs/ARCHITECTURE.md` §Interface TUI).

## 12. Fora do escopo

- Análise de conteúdo/SEO
- Renderização de JavaScript no lado do cliente
- Rastreamento sem salvaguardas
- Varredura ativa de vulnerabilidades, fuzzing, força bruta
- Painel web

---

> Omega-fold — Mapear uma estrutura, verificar seus links, nunca adivinhar o que não foi visitado.
