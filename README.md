# Agentes ao léu

Um time de agentes de IA pronto pra baixar e adaptar: um orquestrador que delega, especialistas
que executam e ferramentas diferentes conversando pelo [herdr](https://herdr.dev).

É o time que eu uso e mostro funcionando no canal **[LeuAoLeo](https://www.youtube.com/@leuaoleo)**.
O repositório cresce a cada vídeo. Deixe uma estrela aqui pra acompanhar as novas peças, e
[se inscreva no canal](https://www.youtube.com/@leuaoleo?sub_confirmation=1) pra ver cada uma sendo montada.

## O que é um template

Um agente de IA é uma ferramenta (Claude Code, OpenCode, Hermes) rodando numa pasta, com um
arquivo de instruções que diz quem ele é e o que pode fazer. Montar esse arquivo do zero a
cada agente dá trabalho e sai diferente toda vez.

O **template** (`_template_agente/`) é o molde: uma pasta pronta, com as instruções já
escritas e lacunas marcadas, como `{{NOME_AGENTE}}` e `{{ESCOPO}}`. Você copia a pasta, preenche
as lacunas e tem um agente novo, já com as mesmas regras do resto do time.

| Peça | O que é |
|---|---|
| **Orquestrador** | O agente que recebe o seu pedido, escolhe quem faz e junta as respostas |
| **Especialista** | Agente com um escopo só (ex.: editar vídeo, cuidar de um servidor), criado a partir do template |
| **Template** | O molde pra criar um especialista novo |
| **Catálogo** | Lista do que o time já tem (agentes, skills, MCPs), pra não criar duas vezes |
| **Skill** | Instrução reutilizável que o agente carrega quando precisa |
| **MCP** | Conexão do agente com uma ferramenta externa. [Vídeo de 20 segundos](https://www.youtube.com/watch?v=0Lb6fxu4Vn0) |
| **herdr** | O terminal onde os agentes ficam abertos e se mandam mensagem |

## Requisitos (Windows)

| Precisa de | Pra quê | Como conferir |
|---|---|---|
| Windows 10 ou 11 | Sistema | |
| PowerShell | Terminal (já vem no Windows) | Menu Iniciar, digite `PowerShell` |
| winget | Instala programas pelo terminal (já vem no Windows 11 e no 10 atualizado) | `winget --version` |
| Node.js (LTS) | Roda o OpenCode e o `npx` | `node -v` |
| npm | Vem junto com o Node.js | `npm -v` |
| OpenCode CLI | O agente que vai usar este repositório | `opencode --version` |
| Git | Baixar este repositório | `git --version` |
| Conta de um provedor de modelo | O OpenCode precisa de um modelo pra responder | Você conecta dentro do OpenCode |

## Instalar no Windows

Abra o **PowerShell** e rode um passo por vez.

**1. Node.js**

```powershell
winget install OpenJS.NodeJS.LTS
```

**2. Git**

```powershell
winget install Git.Git
```

**3. Feche o PowerShell e abra de novo.** Sem isso o terminal não enxerga o que acabou de ser
instalado. Confira:

```powershell
node -v
npm -v
git --version
```

Os três precisam mostrar um número de versão.

**4. OpenCode CLI**

```powershell
npm install -g @opencode/cli
```

Confira:

```powershell
opencode --version
```

**5. Primeiro uso.** Crie uma pasta, entre nela e abra o OpenCode:

```powershell
mkdir meu-time
cd meu-time
opencode
```

Dentro do OpenCode, digite `/connect` e escolha o provedor do seu modelo. Depois siga pra
[Como começar](#como-começar-peça-pro-seu-agente).

Prefere baixar o Node.js pelo site? https://nodejs.org/en/download (escolha o instalador LTS pro Windows).

## Se der erro (Windows)

| O que aparece | O que fazer |
|---|---|
| `winget` não é reconhecido | Abra a Microsoft Store, atualize o "Instalador de Aplicativo" e abra o PowerShell de novo. Ou baixe o Node.js pelo site |
| `node` ou `npm` não é reconhecido logo depois de instalar | Feche o PowerShell e abra de novo. Persistindo, reinicie o Windows |
| `npm : ... a execução de scripts foi desabilitada neste sistema` | Rode `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, responda `S` (ou `Y`, se o Windows estiver em inglês), e tente de novo. Ou use `npm.cmd` no lugar de `npm` |
| `opencode` não é reconhecido depois do `npm install -g` | A pasta global do npm não está no PATH. Veja o caminho com `npm prefix -g` (normalmente `C:\Users\<você>\AppData\Roaming\npm`), adicione em Variáveis de Ambiente, Path, e abra o PowerShell de novo |
| `EACCES` ou `permission denied` no `npm install -g` | Não rode como administrador por reflexo. Confira se o `npm prefix -g` aponta pra uma pasta sua (`AppData\Roaming\npm`) |
| `/new` vira `C:/Git/new` no Git Bash | Use o PowerShell, ou `MSYS_NO_PATHCONV=1` na frente do comando |
| O OpenCode abre e não responde | Falta conectar um modelo. Digite `/connect` |

Não resolveu? leogaraph@gmail.com

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
- Agente parado pode estar só pedindo permissão, e o herdr às vezes mostra `done` nessa hora. Olhe a tela com `herdr agent read <nome>`. Já vimos 45 minutos assim.
- Permissão pasta por pasta trava o time toda semana. No OpenCode, libere a leitura de todas as pastas de trabalho de uma vez e negue só os segredos, que ficam no fim da lista porque a última regra que casa é a que vale. Escrita continua restrita. Pronto pra copiar: [`_template_agente/opencode.json`](_template_agente/opencode.json).
- OpenCode: liberar `external_directory` não libera o `read`. Declare os dois, mais `glob`, `grep` e `list`.
- OpenCode no Windows escreve o caminho em minúscula. Declare as duas grafias.
- OpenCode não lê `.mcp.json`: declare o MCP no `opencode.json`.
- Mudou o `opencode.json`? Reinicie o agente.
- `opencode serve --hostname 0.0.0.0` sem `OPENCODE_SERVER_PASSWORD` abre um agente com terminal pra rede toda.

**Quando aparecer**
- Nome de agente some quando o painel fecha ou ele reinicia: `herdr agent list` e `herdr agent rename`.
- Resposta de outro agente é hipótese. "Risco zero" e "domínio público" já vieram sem conferência.
- Permissão negada encerra o `opencode run` no meio. Retome com `opencode run -s <sessão>`.
- Modelo gratuito com limite de 50 imagens por pedido quebra a sessão. Leia recortes pequenos; quebrou, `/new`.
- Depois de reiniciar a máquina, sessão restaurada no OpenCode pode dar erro de `reasoning encrypted_content`: `/new` e reenvie.
- Guarde o pedido num arquivo (brief). Se a máquina cair, reenvia em uma linha.
- Imagem e música na GPU ao mesmo tempo estouram a memória. Confira `nvidia-smi` antes. Offload pra CPU joga o modelo na RAM (vimos 13 GB), então confira a RAM livre também.
- O Git Bash transforma `/new` em `C:/Git/new`. Use `MSYS_NO_PATHCONV=1` na frente.

## Licença

MIT, mantendo o `LICENSE`. A skill caveman é de terceiro (Copyright (c) 2026 Julius Brussee,
MIT), com a licença original em `.claude/skills/caveman/LICENSE`.
