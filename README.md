# Agentes ao léu

Um time de agentes de IA pra você baixar, adaptar e colocar pra trabalhar. É o mesmo
esquema que eu uso no canal [LeuAoLeo](https://www.youtube.com/@leuaoleo): um agente
orquestrador que pensa e delega, especialistas que executam, e agentes de empresas
diferentes (Claude Code, OpenCode, Hermes) conversando entre si pelo
[herdr](https://herdr.dev).

O repositório cresce junto com o canal. Cada vídeo que monta uma peça nova do time
deixa ela aqui.

## O que tem aqui

| Pasta | Pra quê |
|---|---|
| `orquestrador/` | O agente que coordena o time. Recebe o pedido, manda pro especialista certo e junta as respostas |
| `_template_agente/` | Molde pra criar agente novo. Tem `CLAUDE.md` (lido pelo Claude Code) e `AGENTS.md` (lido pelo OpenCode e pelo Hermes), porque cada ferramenta lê um arquivo diferente |
| `catalogos/` | Três listas que o orquestrador consulta antes de criar qualquer coisa: agentes, skills e MCPs |
| `VIDEOS.md` | Qual vídeo do canal explica cada parte |

> As pastas entram conforme os vídeos saem. Se alguma ainda não existe, o vídeo dela está a caminho.

## Regras do time

1. **Manda e segue.** O orquestrador nunca fica parado esperando outro agente responder. Manda o pedido, faz outra coisa, e lê a resposta depois.
2. **Consulta o catálogo antes de criar.** Se já existe agente, skill ou MCP que resolve, reaproveita.
3. **Nunca instala agente cru.** Agente da internet é estudado primeiro: o orquestrador lê, aponta o que briga com as regras do time e adapta pro template.
4. **Segredo nunca em arquivo.** Chave, token e senha ficam só em variável de ambiente.

## Como começar

1. Instale o herdr: <https://herdr.dev>
2. Copie a pasta `orquestrador/` pra onde você quer que o time more.
3. Abra o Claude Code dentro dela e peça pra ele se apresentar.
4. Pra criar um especialista, copie `_template_agente/`, troque os marcadores `{{NOME_AGENTE}}`, `{{ESCOPO}}` e `{{FERRAMENTAS}}` e registre no catálogo.

O passo a passo completo, com os erros que aconteceram no caminho, está nos vídeos (ver `VIDEOS.md`).

## Licença

MIT. Pode usar, copiar, adaptar e usar em projeto comercial. Só mantenha o aviso de
licença junto (arquivo `LICENSE`).

## Contato

Dúvida, ideia ou quer um time desses na sua empresa: leogaraph@gmail.com
