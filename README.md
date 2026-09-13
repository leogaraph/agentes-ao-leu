# Agentes ao léu

Um time de agentes de IA pra você baixar, adaptar e colocar pra trabalhar. É o mesmo
esquema que eu uso no canal [LeuAoLeo](https://www.youtube.com/@leuaoleo): um agente
orquestrador que pensa e delega, especialistas que executam, e agentes de harness diferentes (Claude Code, OpenCode, Hermes) conversando entre si pelo
[herdr](https://herdr.dev).

O repositório cresce junto com o canal. Cada vídeo que monta uma peça nova do time
deixa ela aqui.

## O que tem aqui

| Pasta | Pra quê |
|---|---|
| `orquestrador/` | O agente que coordena o time. Recebe o pedido, manda pro especialista certo e junta as respostas |
| `_template_agente/` | Molde pra criar agente novo. Tem `CLAUDE.md` (lido pelo Claude Code) e `AGENTS.md` (lido pelo OpenCode e pelo Hermes), porque cada ferramenta lê um arquivo diferente |
| `catalogos/` | Três listas que o orquestrador consulta antes de criar qualquer coisa: agentes, skills e MCPs |
| `mcp/` | Como ligar o mesmo servidor MCP no Claude Code, no OpenCode e no Hermes, com um exemplo pronto pra cada um |
| `skills/` | Como escrever uma skill que as três ferramentas entendem, e onde cada uma procura |
| `VIDEOS.md` | Qual vídeo do canal explica cada parte |

> As pastas entram conforme os vídeos saem. Se alguma ainda não existe, o vídeo dela está a caminho.

## Regras do time

1. **Manda e segue.** O orquestrador nunca fica parado esperando outro agente responder. Manda o pedido, faz outra coisa, e lê a resposta depois.
2. **Consulta o catálogo antes de criar.** Se já existe agente, skill ou MCP que resolve, reaproveita.
3. **Nunca instala agente cru.** Agente da internet é estudado primeiro: o orquestrador lê, aponta o que briga com as regras do time e adapta pro template.
4. **Segredo nunca em arquivo.** Chave, token e senha ficam só em variável de ambiente.
5. **Modo caveman obrigatório no chat.** Todo agente do time responde comprimido (skill `caveman` em `.claude/skills/`, regras espelhadas no `AGENTS.md` pra OpenCode e Hermes). Comprime o estilo, nunca o idioma nem a exatidão técnica. Texto fora do chat (código, commit, documentação) fica normal. Detalhes na seção [Caveman](#caveman-menos-token-mesma-resposta).

## MCP: o mesmo servidor nas três ferramentas

Um servidor MCP liga o agente num sistema de fora (GitHub, YouTube, Trello, pasta de
arquivos). O servidor é o mesmo pra todo mundo. O que muda é onde cada ferramenta procura
a configuração e como ela escreve a variável de ambiente.

| Ferramenta | Arquivo | Onde fica | Variável de ambiente |
|---|---|---|---|
| Claude Code | `.mcp.json` | Na pasta do agente | `${VAR}` |
| OpenCode | `opencode.json` (bloco `mcp`) | Na pasta do agente | `{env:VAR}` |
| Hermes | `config.yaml` (bloco `mcp_servers`) | Global, em `~/.hermes/` | `${VAR}` |

- O OpenCode não lê `.mcp.json`: agente que roda nas duas ferramentas declara o servidor nos dois arquivos, com a mesma variável.
- O Hermes não tem configuração por pasta. Pra separar agentes, filtre as ferramentas de cada servidor com `tools.include`.
- No OpenCode, liberar `external_directory` não libera o `read`. Declare os dois.

Exemplos prontos pras três ferramentas em [`mcp/`](mcp/).

## Skills: uma receita que as três ferramentas entendem

Skill é um passo a passo que o agente carrega só quando precisa. O formato é o mesmo nas
três: uma pasta com um `SKILL.md` e um cabeçalho com `name` (minúsculas e hífen) e
`description` (quando usar).

| Ferramenta | Onde procura skill | Arquivo de identidade |
|---|---|---|
| Claude Code | `.claude/skills/` | `CLAUDE.md` |
| OpenCode | `.claude/skills/`, `.opencode/skills/`, `.agents/skills/` | `AGENTS.md` |
| Hermes | `~/.hermes/skills/` e pastas extras do `config.yaml` | `SOUL.md`, `AGENTS.md`, `CLAUDE.md` |

Guardando a skill em `.claude/skills/<nome>/SKILL.md` dentro da pasta do agente, o Claude
Code e o OpenCode já enxergam. Pro Hermes, aponte essa pasta no `config.yaml` ou copie a
skill pra `~/.hermes/skills/`. Detalhes e exemplo em [`skills/`](skills/).

## Caveman: menos token, mesma resposta

Todo agente do time vem com a skill **caveman** ligada. Ela faz o agente responder no chat
de forma comprimida, sem enrolação, mantendo o conteúdo técnico, o idioma e os números
exatos. Com vários agentes rodando o dia inteiro, cada palavra a menos conta.

- Comprime só a conversa. Código, commit, documentação e mensagem pra outra pessoa continuam em texto normal.
- Aviso de segurança e confirmação de ação irreversível saem sempre por extenso.
- Níveis: `lite`, `full` (padrão) e `ultra`. Desliga com `/caveman off` ou "modo normal".
- Agente que escreve conteúdo pro público (roteiro, legenda, post) pode ficar de fora: a skill é pra conversa entre agentes e com você, não pro texto final.
- A economia varia com a tarefa. O autor fala em cerca de 65% da saída de texto; testes independentes em tarefa de agente, que tem muito código e chamada de ferramenta (que o caveman não mexe), mediram bem menos.

Skill original: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman), licença
MIT. A cópia deste repositório fica em `.claude/skills/caveman/`, com o aviso de licença do
autor no arquivo `LICENSE` da própria pasta.

## Como começar

1. Instale o herdr: <https://herdr.dev>
2. Copie a pasta `orquestrador/` pra onde você quer que o time more.
3. Abra o Claude Code dentro dela e peça pra ele se apresentar.
4. Pra criar um especialista, copie `_template_agente/`, troque os marcadores `{{NOME_AGENTE}}`, `{{ESCOPO}}` e `{{FERRAMENTAS}}` e registre no catálogo.

O passo a passo completo, com os erros que aconteceram no caminho, está nos vídeos (ver `VIDEOS.md`).

## Licença

MIT. Pode usar, copiar, adaptar e usar em projeto comercial. Só mantenha o aviso de
licença junto (arquivo `LICENSE`).

A skill `caveman` é de terceiro ([JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman),
MIT, Copyright (c) 2026 Julius Brussee) e mantém a licença original em
`.claude/skills/caveman/LICENSE`.

## Contato

Dúvida, ideia ou quer um time desses na sua empresa: leogaraph@gmail.com
