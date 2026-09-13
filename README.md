# Agentes ao léu

Você tem o Claude Code aberto numa janela, o OpenCode na outra, talvez um Hermes rodando
num servidor. Pede uma coisa pra um, copia a resposta, cola no outro, volta, confere
quem travou. No fim do dia você virou o carteiro dos seus próprios agentes.

Eu passei por isso. Este repositório é o que eu montei pra sair dessa: um agente
orquestrador que recebe o pedido e delega, especialistas que fazem o trabalho, e
ferramentas de empresas diferentes conversando direto entre si pelo
[herdr](https://herdr.dev), sem você no meio levando recado.

## Pra quem é

- Quem já usa mais de uma ferramenta ou plataforma de IA e cansou de ficar trocando de janela.
- Quem tem agente de harness diferente (Claude Code, OpenCode, Hermes, Codex, Pi ou qualquer outro) e quer que eles trabalhem juntos.
- Quem quer montar um time de agentes com regra clara, sem instalar coisa da internet no escuro.

## Funciona com a sua ferramenta

Aqui a gente roda e testa com **Claude Code, OpenCode e Hermes**, então os exemplos usam
esses três. Mas nada no esquema depende deles: o herdr reconhece mais de 20 ferramentas de
agente (Codex, Pi, Cursor, Copilot, Grok e outras), e o que o repositório ensina vale pra
qualquer uma:

- **Identidade:** a maioria das ferramentas lê `AGENTS.md`. As que não leem costumam ter um
  arquivo próprio (o Claude Code usa `CLAUDE.md`). Mantenha os dois com o mesmo conteúdo.
- **Skills:** o formato `SKILL.md` virou padrão aberto e várias ferramentas já leem. Confira
  na documentação da sua em qual pasta ela procura.
- **MCP:** o servidor é o mesmo pra todas. Só muda o arquivo onde cada uma declara.
- **Conversa entre agentes:** se o herdr reconhece a ferramenta, ela entra no time.

Usa outra ferramenta e adaptou? Abra uma issue ou um pull request contando onde ela lê cada
coisa, que a gente acrescenta nas tabelas.

É o mesmo esquema que eu uso no canal [LeuAoLeo](https://www.youtube.com/@leuaoleo), e o
repositório cresce junto com ele: cada vídeo que monta uma peça nova do time deixa ela aqui.

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
| Outras (Codex, Pi, Cursor...) | Cada uma tem o seu | Veja "MCP" na documentação dela | Quase sempre dá pra usar variável de ambiente |

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
| Outras (Codex, Pi, Cursor...) | Muitas leem `.agents/skills/`; confira na documentação | Quase todas leem `AGENTS.md` |

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

## Pulo do gato: problemas conhecidos e contornados

Tudo aqui aconteceu de verdade rodando o time. Se você cair num desses, o conserto já
está do lado.

### Comunicação entre agentes

- **Não trave a sessão esperando resposta.** `herdr agent prompt <nome> "texto" --wait`
  deixa o agente parado até o outro terminar, sem fazer mais nada. Mande sem `--wait`,
  siga em outra tarefa e leia depois com `herdr agent read <nome>`. Só espere quando a
  resposta decide o próximo passo.
- **Instale a skill do herdr em cada ferramenta.** Sem ela, o agente tenta o canal nativo
  da própria ferramenta: o Claude Code usa a lista de sessões dele, que só enxerga outras
  sessões Claude Code, e o OpenCode usa `opencode session list`, que só enxerga OpenCode.
  Resultado: o agente jura que o resto do time está desligado. Instale uma vez em cada
  máquina com `npx skills add herdrdev/herdr --skill herdr -g` e deixe escrito no
  `CLAUDE.md` e no `AGENTS.md` que o canal é o herdr.
- **Nome de agente some.** Se o painel fecha ou o agente reinicia, o nome que você deu
  vai embora. Redescubra com `herdr agent list` e renomeie com `herdr agent rename`.
- **Agente "travado" pode estar só pedindo permissão.** `herdr agent get <nome>` mostra
  `blocked` quando ele está esperando você aprovar alguma coisa. Já vimos agente parado
  45 minutos assim. Leia a tela com `herdr agent read <nome>` antes de achar que quebrou.
- **Resposta de outro agente é hipótese, não fato.** Agente escreve "risco zero" ou
  "domínio público" sem conferir. Antes de repassar pro usuário, confira na fonte.

### OpenCode

- **Não lê `.mcp.json`.** Declare o MCP no `opencode.json`, bloco `mcp`.
- **Permissão de pasta é separada por ferramenta.** Liberar `external_directory` não
  libera `read`, `glob` nem `grep`. Declare todas, com os mesmos caminhos.
- **No Windows, ele escreve o caminho em minúscula** (`e:\projeto` em vez de
  `E:\Projeto`). Se a regra de permissão não bate, declare as duas grafias.
- **Mudou o `opencode.json`? Reinicie o agente.** A configuração só é lida na subida.
- **Negação de permissão encerra o `opencode run`.** Em modo sem tela, se o agente tenta
  ler algo bloqueado (um `.env`, por exemplo), a execução termina no meio. Retome a mesma
  sessão com `opencode run -s <id-da-sessao>` dizendo pra ele não ler aquilo.
- **`opencode serve --hostname 0.0.0.0` abre o agente pra rede inteira.** Sem a variável
  `OPENCODE_SERVER_PASSWORD`, qualquer aparelho da rede manda comando pra um agente com
  terminal. Use `127.0.0.1` quando o acesso for só da própria máquina.

### Modelo e sessão

- **Limite de imagens por pedido.** Alguns modelos gratuitos aceitam no máximo 50 imagens
  por requisição e a sessão quebra quando passa disso. Leia imagem em recorte pequeno e
  poucas vezes por tarefa. Quebrou? Abra uma sessão nova com `/new`.
- **Sessão restaurada que não volta.** Depois de reiniciar a máquina, uma sessão antiga
  pode falhar com erro de `reasoning encrypted_content`. Abra uma sessão nova com `/new`
  e reenvie a tarefa.
- **Escreva o pedido num arquivo.** Se a máquina desliga, a tarefa em andamento se perde,
  mas um arquivo de instruções (brief) no disco deixa você reenviar em uma linha.
- **Duas tarefas pesadas de GPU ao mesmo tempo estouram a memória.** Geração de imagem e
  de música juntas derrubaram tudo aqui. Peça pro agente conferir `nvidia-smi` antes de
  usar a placa, e ligue o modo de economia de memória (offload) no gerador.

### Terminal no Windows

- **O Git Bash transforma `/new` em caminho** (vira `C:/Git/new`). Ao mandar comando com
  barra pro agente via terminal, use `MSYS_NO_PATHCONV=1` na frente.

## Como começar: peça pro seu agente

Este repositório é feito pra agente ler. Você não precisa copiar pasta na mão: abra o seu
Claude Code, OpenCode, Hermes, Codex, Pi ou a ferramenta que você usa, numa pasta vazia, e
cole o pedido. Cada bloco abaixo é um
pedido pronto.

**1. Montar o time do zero**

```text
Clone https://github.com/leogaraph/agentes-ao-leu e leia o README inteiro, principalmente
"Regras do time" e "Pulo do gato". Depois:
1. Instale o herdr (https://herdr.dev) se ainda não estiver instalado e instale a skill
   dele pra você: npx skills add herdrdev/herdr --skill herdr -g
2. Copie orquestrador/ pra esta pasta. A partir de agora você é o orquestrador: siga o
   CLAUDE.md ou o AGENTS.md dele, o que a sua ferramenta ler.
3. Crie a pasta catalogos/ com agentes.md, skills.md e mcps.md e registre você como
   primeiro agente.
4. Me mostre a árvore de pastas e me diga, em 5 linhas, como você vai delegar.
Não instale nada além disso sem me perguntar.
```

**2. Criar um especialista**

```text
Crie um agente novo a partir de _template_agente/. Nome: <nome>. Escopo: <o que ele faz e o
que não faz>. Ferramenta: <Claude Code, OpenCode ou Hermes>. Preencha CLAUDE.md e AGENTS.md
com o mesmo conteúdo essencial, registre em catalogos/agentes.md e me mostre o que ficou
antes de ligar ele.
```

**3. Importar um agente ou skill da internet sem instalar cru**

```text
Estude este repositório: <link>. Não instale nada. Me responda em 5 linhas: o que ele faz,
o que aproveita pro nosso time, o que briga com as nossas regras (segredo, espera, escopo),
se vira agente, skill ou MCP no catálogo, e o que você mudaria. Só depois do meu ok, adapte
pro _template_agente/, registre no catálogo e me mostre a diferença pro original.
```

**4. Ligar um MCP nas três ferramentas**

```text
Quero o MCP <nome> disponível pro time. Leia mcp/README.md e declare o servidor no formato
de cada ferramenta que a gente usa, com o segredo só em variável de ambiente (me diga o
nome da variável, eu mesmo coloco o valor). Registre em catalogos/mcps.md.
```

**5. Ligar o modo caveman num agente que ainda não tem**

```text
Copie .claude/skills/caveman/ do _template_agente/ pra pasta do agente <nome>, junto com o
LICENSE, e acrescente a seção "Modo caveman (obrigatório)" no CLAUDE.md e no AGENTS.md dele,
igual ao template.
```

Se o agente tentar falar com os outros por outro caminho que não o herdr, ou disser que o
resto do time está desligado, veja o "Pulo do gato".

### Se preferir fazer na mão

1. Instale o herdr: <https://herdr.dev>. Depois instale a skill dele em cada ferramenta: `npx skills add herdrdev/herdr --skill herdr -g`.
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
