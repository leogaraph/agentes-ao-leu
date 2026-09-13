# Agentes ao léu

Cansou de ser o carteiro entre as suas ferramentas de IA, copiando resposta de uma pra
colar na outra? Aqui os agentes conversam direto entre si, e você só dá a ordem.

É o time que eu uso e mostro funcionando no canal **[LeuAoLeo](https://www.youtube.com/@leuaoleo)**:
um orquestrador que delega, especialistas que executam, e ferramentas diferentes
conversando pelo [herdr](https://herdr.dev). O repositório cresce a cada vídeo.

Deixe uma estrela aqui pra acompanhar as novas peças, e [se inscreva no canal](https://www.youtube.com/@leuaoleo?sub_confirmation=1) pra ver cada uma sendo montada.

## Como começar: peça pro seu agente

Abra a sua ferramenta de IA numa pasta vazia e cole um destes pedidos.

**Montar o time**
```text
Clone https://github.com/leogaraph/agentes-ao-leu e leia o README, principalmente "Regras
do time" e "Pulo do gato". Instale o herdr (https://herdr.dev) e a skill dele pra você
(npx skills add herdrdev/herdr --skill herdr -g). Copie a pasta orquestrador/ da raiz do
repositório pra esta pasta e siga o CLAUDE.md ou AGENTS.md dela. Crie catalogos/ com
agentes.md, skills.md e mcps.md e se registre. Me mostre a árvore e, em 5 linhas, como vai
delegar. Não instale mais nada sem me perguntar.
```

**Criar um especialista**
```text
Crie um agente a partir de _template_agente/ (na raiz do repositório). Nome: <nome>.
Escopo: <faz e não faz>. Ferramenta: <qual>. Preencha CLAUDE.md e AGENTS.md iguais,
registre no catálogo e me mostre antes de ligar.
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

Na mão: instale o herdr e a skill, copie `orquestrador/` e, pra cada especialista, copie
`_template_agente/`, troque `{{NOME_AGENTE}}`, `{{ESCOPO}}` e `{{FERRAMENTAS}}` e registre no
catálogo.

Travou em algum passo ou quer esse time na sua empresa? leogaraph@gmail.com

## O que tem aqui

| Pasta | Pra quê |
|---|---|
| `orquestrador/` | Recebe o pedido, delega, junta as respostas |
| `_template_agente/` | Molde de agente novo |
| `catalogos/` | Agentes, skills e MCPs do time |
| `mcp/` | MCP em cada ferramenta, com exemplos |
| `skills/` | Skill que todas as ferramentas entendem |
| `VIDEOS.md` | Qual vídeo explica cada parte |

Não sabe o que é MCP? [Tem vídeo de 1 minuto](https://www.youtube.com/watch?v=0Lb6fxu4Vn0).

## Regras do time

1. **Manda e segue.** Ninguém fica parado esperando outro agente.
2. **Catálogo antes de criar.** Se já existe, reaproveita.
3. **Nunca instala agente cru.** O que vem da internet é estudado e adaptado antes.
4. **Segredo só em variável de ambiente.**
5. **[Caveman](https://github.com/JuliusBrussee/caveman) no chat**, pra gastar menos token.

## Funciona com a sua ferramenta

Testado com Claude Code, OpenCode e Hermes. O herdr reconhece mais de 20 ferramentas
([lista oficial](https://herdr.dev/docs/agents/)) e roda as outras como terminal comum.

| Ferramenta | Identidade | MCP |
|---|---|---|
| Claude Code | `CLAUDE.md` | `.mcp.json` |
| OpenCode | `AGENTS.md` | `opencode.json` |
| Hermes | `AGENTS.md` | `~/.hermes/config.yaml` |
| Outras | quase sempre `AGENTS.md` | ver a documentação |

Skills: guarde em `.claude/skills/<nome>/`. Claude Code e OpenCode leem dali; no Hermes,
aponte essa pasta no `config.yaml`. Detalhes em [`mcp/`](mcp/) e [`skills/`](skills/).

Usa outra ferramenta ou tem um caso que o repositório não cobre? [Abra uma issue](https://github.com/leogaraph/agentes-ao-leu/issues).

## Pulo do gato

**No primeiro dia**
- Sem a skill do herdr, o agente usa o canal da própria ferramenta (lista de sessões do Claude Code, `opencode session list`), que só vê a mesma ferramenta, e jura que o time está desligado. Instale a skill em cada máquina e escreva no `CLAUDE.md` e no `AGENTS.md` que o canal é o herdr.
- `herdr agent prompt ... --wait` trava quem pediu. Mande sem `--wait` e leia depois com `herdr agent read <nome>`.
- Agente parado pode estar só pedindo permissão (`herdr agent get` mostra `blocked`). Já vimos 45 minutos assim.
- OpenCode não lê `.mcp.json`: declare o MCP no `opencode.json`.
- OpenCode: liberar `external_directory` não libera o `read`. Declare os dois (e `glob` e `grep` se o agente procura arquivos).
- OpenCode no Windows escreve o caminho em minúscula. Declare as duas grafias.
- Mudou o `opencode.json`? Reinicie o agente.
- `opencode serve --hostname 0.0.0.0` sem `OPENCODE_SERVER_PASSWORD` abre um agente com terminal pra rede toda.

**Quando aparecer**
- Nome de agente some quando o painel fecha ou ele reinicia: `herdr agent list` e `herdr agent rename`.
- Resposta de outro agente é hipótese. "Risco zero" e "domínio público" já vieram sem conferência.
- Permissão negada encerra o `opencode run` no meio. Retome com `opencode run -s <sessão>`.
- Modelo gratuito com limite de 50 imagens por pedido quebra a sessão. Leia recortes pequenos; quebrou, `/new`.
- Depois de reiniciar a máquina, sessão restaurada no OpenCode pode dar erro de `reasoning encrypted_content`: `/new` e reenvie.
- Guarde o pedido num arquivo (brief). Se a máquina cair, reenvia em uma linha.
- Imagem e música na GPU ao mesmo tempo estouram a memória. Confira `nvidia-smi` antes e ligue offload.
- O Git Bash transforma `/new` em `C:/Git/new`. Use `MSYS_NO_PATHCONV=1` na frente.

## Licença

MIT, mantendo o `LICENSE`. A skill caveman é de terceiro (Copyright (c) 2026 Julius Brussee,
MIT), com a licença original em `.claude/skills/caveman/LICENSE`.
