# MCP nas três ferramentas

Um servidor MCP liga o agente num sistema de fora (GitHub, YouTube, Trello, pasta de
arquivos). O servidor é o mesmo pra todo mundo. O que muda é **onde** cada ferramenta
procura a configuração e **como** ela escreve a variável de ambiente.

| Ferramenta | Arquivo | Onde fica | Variável de ambiente |
|---|---|---|---|
| Claude Code | `.mcp.json` | Na pasta do agente | `${VAR}` |
| OpenCode | `opencode.json` (bloco `mcp`) | Na pasta do agente | `{env:VAR}` |
| Hermes | `config.yaml` (bloco `mcp_servers`) | Global, em `~/.hermes/` | `${VAR}` ou `${env:VAR}` |

Os três exemplos desta pasta configuram **os mesmos dois servidores**, um local e um
remoto, pra você comparar lado a lado:

- [`exemplo.mcp.json`](exemplo.mcp.json): Claude Code
- [`exemplo.opencode.json`](exemplo.opencode.json): OpenCode
- [`exemplo.hermes-config.yaml`](exemplo.hermes-config.yaml): Hermes

## Regras que evitam dor de cabeça

1. **Segredo nunca no arquivo.** Chave e token entram só como variável de ambiente. No
   Hermes, a própria documentação manda guardar em `~/.hermes/.env`.
2. **O OpenCode não lê `.mcp.json`.** Se o agente roda nas duas ferramentas, declare o
   servidor nos dois arquivos, com a mesma variável de ambiente.
3. **O Hermes não tem configuração por pasta.** O `config.yaml` é um só pra máquina
   inteira. Se dois agentes Hermes precisam de MCPs diferentes, filtre as ferramentas de
   cada servidor com `tools.include` / `tools.exclude`.
4. **No OpenCode, permissão de pasta é separada por ferramenta.** Liberar
   `external_directory` não libera o `read`. Se o agente precisa ler fora da própria
   pasta, declare os dois (o exemplo mostra como).
5. **Registre no catálogo.** Todo MCP novo entra em `catalogos/mcps.md`, com o
   nome da variável de ambiente que ele usa (nunca o valor).

## Fontes

- OpenCode: <https://opencode.ai/docs/mcp-servers/>
- Hermes: <https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference>
- Claude Code: <https://docs.claude.com/en/docs/claude-code/mcp>
