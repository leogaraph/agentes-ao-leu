# Skills nas três ferramentas

Skill é uma receita: um passo a passo que o agente carrega quando precisa, em vez de
ficar tudo no prompt o tempo todo. O formato é o mesmo nas três ferramentas: uma pasta
com um arquivo `SKILL.md` dentro.

```
<nome-da-skill>/
  SKILL.md
```

```markdown
---
name: revisar-texto
description: Revisa texto em português e aponta erro sem reescrever. Use quando pedirem revisão.
---

1. Leia o texto inteiro antes de comentar.
2. Aponte erro de grafia, concordância e pontuação, com a linha.
3. Não reescreva o texto. Só aponte.
```

`name` em minúsculas e com hífen (é a regra mais chata, é a do OpenCode:
`^[a-z0-9]+(-[a-z0-9]+)*$`). `description` diz **quando** usar, porque é por ela que o
agente decide carregar a skill.

## Onde cada ferramenta procura

| Ferramenta | Pastas que ela lê |
|---|---|
| Claude Code | `.claude/skills/` na pasta do agente e `~/.claude/skills/` |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` (na pasta e em `~`) e `~/.config/opencode/skills/` |
| Hermes | `~/.hermes/skills/` e pastas extras apontadas no `config.yaml` |

## O jeito que funciona pros três

1. Guarde a skill em **`.claude/skills/<nome>/SKILL.md`** dentro da pasta do agente. O
   Claude Code e o OpenCode já leem daí sem configurar nada. É o que o
   `_template_agente/` faz.
2. Pro Hermes, que não procura na pasta do projeto, aponte essa pasta no `config.yaml`
   como diretório extra de skills (a opção se chama `external_dirs` nos guias; confira o
   nome na documentação da sua versão), ou copie a skill pra `~/.hermes/skills/`.
3. Registre a skill em `catalogos/catalogo_skills.md`, com dono e pra quê serve.

## Arquivo de identidade de cada ferramenta

Parecido com a skill, cada ferramenta lê um arquivo diferente pra saber quem o agente é:

| Ferramenta | Lê |
|---|---|
| Claude Code | `CLAUDE.md` |
| OpenCode | `AGENTS.md` |
| Hermes | `SOUL.md`, `AGENTS.md`, `CLAUDE.md`, `.hermes.md` |

Por isso o template tem `CLAUDE.md` **e** `AGENTS.md` com o mesmo conteúdo essencial.

## Fontes

- OpenCode: <https://opencode.ai/docs/skills/>
- Hermes: <https://hermes-agent.nousresearch.com/docs/user-guide/configuration>
- Claude Code: <https://docs.claude.com/en/docs/claude-code/skills>
