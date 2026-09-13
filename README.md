# Agentes ao léu

Claude Code numa janela, OpenCode na outra, um Hermes no servidor. Você pede pra um, copia
a resposta, cola no outro e confere quem travou. No fim do dia virou o carteiro dos seus
próprios agentes.

Este repositório é o time que eu uso no canal [LeuAoLeo](https://www.youtube.com/@leuaoleo)
pra sair dessa, e ele cresce a cada vídeo: um orquestrador que recebe o pedido e delega,
especialistas que fazem o trabalho, e ferramentas diferentes conversando direto entre si
pelo [herdr](https://herdr.dev).

**Pra quem é:** quem já usa mais de uma ferramenta de IA (Claude Code, OpenCode, Hermes,
Codex, Pi ou outra), cansou de trocar de janela e quer um time com regra clara, sem instalar
coisa da internet no escuro.

## O que tem aqui

| Pasta | Pra quê |
|---|---|
| `orquestrador/` | O agente que coordena: recebe o pedido, delega e junta as respostas |
| `_template_agente/` | Molde de agente novo, com `CLAUDE.md` e `AGENTS.md` |
| `catalogos/` | Agentes, skills e MCPs do time. O orquestrador consulta antes de criar algo |
| `mcp/` | O mesmo servidor MCP configurado em cada ferramenta, com exemplos |
| `skills/` | Como escrever uma skill que todas entendem |
| `VIDEOS.md` | Qual vídeo explica cada parte |

As pastas entram conforme os vídeos saem.

## Regras do time

1. **Manda e segue.** Ninguém fica parado esperando outro agente. Manda, faz outra coisa, lê a resposta depois.
2. **Catálogo antes de criar.** Se já existe agente, skill ou MCP que resolve, reaproveita.
3. **Nunca instala agente cru.** O que vem da internet é estudado e adaptado ao template antes.
4. **Segredo só em variável de ambiente**, nunca em arquivo.
5. **Caveman no chat** (ver abaixo).

## Funciona com a sua ferramenta

A gente testa com Claude Code, OpenCode e Hermes, mas o herdr reconhece mais de 20
ferramentas ([lista oficial](https://herdr.dev/docs/agents/)), e as que não estão na lista
ainda rodam nele como terminal comum. Se o herdr reconhece, entra no time.
O que muda de uma pra outra é onde cada uma procura as coisas:

| Ferramenta | Identidade | Skills | MCP |
|---|---|---|---|
| Claude Code | `CLAUDE.md` | `.claude/skills/` | `.mcp.json` na pasta, `${VAR}` |
| OpenCode | `AGENTS.md` | `.claude/skills/`, `.opencode/skills/`, `.agents/skills/` | `opencode.json`, bloco `mcp`, `{env:VAR}` |
| Hermes | `SOUL.md`, `AGENTS.md`, `CLAUDE.md` | `~/.hermes/skills/` ou pasta extra no `config.yaml` | `~/.hermes/config.yaml`, global, `${VAR}` |
| Outras | Quase todas leem `AGENTS.md` | Muitas leem `.agents/skills/` | Veja a documentação dela |

Guarde a skill em `.claude/skills/<nome>/SKILL.md` na pasta do agente: Claude Code e
OpenCode já leem dali; pro Hermes, aponte a pasta no `config.yaml`. Exemplos e detalhes em
[`mcp/`](mcp/) e [`skills/`](skills/). Usa outra ferramenta? Abra uma issue contando onde
ela lê cada coisa.

## Caveman: menos token, mesma resposta

Todo agente responde no chat de forma comprimida, com o conteúdo técnico, o idioma e os
números intactos. Código, commit, documentação e texto pro público ficam normais, e aviso
de segurança sai sempre por extenso. Agente que só escreve conteúdo (roteiro, post) pode
ficar de fora. Níveis `lite`, `full` (padrão) e `ultra`; desliga com
`/caveman off`. A economia varia: o autor fala em ~65% do texto, testes em tarefa de agente
mediram bem menos. Skill original: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (MIT).

## Como começar: peça pro seu agente

Abra a sua ferramenta numa pasta vazia e cole um destes pedidos.

**Montar o time**
```text
Clone https://github.com/leogaraph/agentes-ao-leu e leia o README, principalmente "Regras
do time" e "Pulo do gato". Instale o herdr (https://herdr.dev) e a skill dele pra você
(npx skills add herdrdev/herdr --skill herdr -g). Copie orquestrador/ pra esta pasta e passe
a seguir o CLAUDE.md ou AGENTS.md dele. Crie catalogos/ com agentes.md, skills.md e mcps.md
e se registre. Me mostre a árvore e, em 5 linhas, como vai delegar. Não instale mais nada
sem perguntar.
```

**Criar um especialista**
```text
Crie um agente a partir de _template_agente/. Nome: <nome>. Escopo: <faz e não faz>.
Ferramenta: <qual>. Preencha CLAUDE.md e AGENTS.md iguais, registre no catálogo e me mostre
antes de ligar.
```

**Importar da internet sem instalar cru**
```text
Estude <link> sem instalar nada. Em 5 linhas: o que faz, o que aproveita, o que briga com
as nossas regras, se vira agente, skill ou MCP, e o que você mudaria. Depois do meu ok,
adapte ao template, registre e me mostre a diferença pro original.
```

**Ligar um MCP**
```text
Quero o MCP <nome> pro time. Siga mcp/README.md, declare no formato de cada ferramenta que
a gente usa, segredo só em variável de ambiente (me diga o nome, eu coloco o valor) e
registre em catalogos/mcps.md.
```

**Ligar o caveman num agente**
```text
Copie .claude/skills/caveman/ (com o LICENSE) do _template_agente/ pro agente <nome> e
acrescente a seção "Modo caveman (obrigatório)" no CLAUDE.md e no AGENTS.md dele.
```

Na mão: instale o herdr e a skill, copie `orquestrador/`, abra sua ferramenta dentro dela,
e pra cada especialista copie `_template_agente/`, troque `{{NOME_AGENTE}}`, `{{ESCOPO}}` e
`{{FERRAMENTAS}}` e registre no catálogo.

## Pulo do gato: problemas que já resolvemos

**Comunicação**
- `herdr agent prompt ... --wait` trava quem pediu. Mande sem `--wait` e leia depois com `herdr agent read <nome>`.
- Sem a skill do herdr, o agente usa o canal da própria ferramenta (lista de sessões do Claude Code, `opencode session list`), que só vê a mesma ferramenta, e jura que o time está desligado. Instale a skill em cada máquina e escreva no `CLAUDE.md` e no `AGENTS.md` que o canal é o herdr.
- Nome de agente some quando o painel fecha ou ele reinicia: `herdr agent list` e `herdr agent rename`.
- Agente parado pode estar só pedindo permissão (`herdr agent get` mostra `blocked`). Já vimos 45 minutos assim.
- Resposta de outro agente é hipótese. "Risco zero" e "domínio público" já vieram sem conferência.

**OpenCode**
- Não lê `.mcp.json`: declare o MCP no `opencode.json`.
- `external_directory` não libera `read`, `glob` nem `grep`. Declare todos.
- No Windows, escreve o caminho em minúscula. Declare as duas grafias.
- Mudou o `opencode.json`? Reinicie o agente.
- Permissão negada encerra o `opencode run` no meio. Retome com `opencode run -s <sessão>`.
- `opencode serve --hostname 0.0.0.0` sem `OPENCODE_SERVER_PASSWORD` abre um agente com terminal pra rede toda.

**Modelo, sessão e máquina**
- Modelo gratuito com limite de 50 imagens por pedido quebra a sessão. Leia recortes pequenos; quebrou, `/new`.
- Sessão restaurada depois de reiniciar a máquina pode dar erro de `reasoning encrypted_content`: `/new` e reenvie.
- Guarde o pedido num arquivo (brief). Se a máquina cair, reenvia em uma linha.
- Imagem e música na GPU ao mesmo tempo estouram a memória. Confira `nvidia-smi` antes e ligue offload.
- O Git Bash transforma `/new` em `C:/Git/new`. Use `MSYS_NO_PATHCONV=1` na frente.

## Licença e contato

MIT: pode usar, adaptar e usar em projeto comercial, mantendo o `LICENSE`. A skill caveman
é de terceiro (Copyright (c) 2026 Julius Brussee, MIT), com a licença original em
`.claude/skills/caveman/LICENSE`.

Dúvida, ideia ou quer um time desses na sua empresa: leogaraph@gmail.com
