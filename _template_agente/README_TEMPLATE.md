# Como instanciar um agente novo a partir deste template

1. Copiar esta pasta inteira para onde o time de agentes mora, com o nome
   do agente novo.
2. Em `CLAUDE.md`: substituir todos os `{{NOME_AGENTE}}` pelo nome do
   agente, preencher `{{ESCOPO}}` e `{{FERRAMENTAS}}`.
3. Em `AGENTS.md`: mesma coisa, versão enxuta (Missão, Divisão de domínio,
   Limites duros). Gerar sempre os dois — Claude Code lê `CLAUDE.md`;
   OpenCode e Hermes leem `AGENTS.md`.
4. Skill específica do agente vai em `.claude/skills/<nome-skill>/` — já
   vem criado; apagar `_leia-me.txt` de dentro quando a primeira skill de
   verdade nascer.
5. `memoria_local/MEMORY.md` já vem pronto — só ajustar o título com o
   nome real do agente.
6. Se o agente rodar como sessão própria, abrir a sessão com o working
   directory dessa pasta — o `CLAUDE.md` local é carregado
   automaticamente.
7. Registrar o agente novo em `../catalogos/agentes.md`.

Lembrete: agente novo só é criado com aprovação prévia do usuário (ver
`CLAUDE.md` do `../orquestrador/`).
