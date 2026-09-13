# Orquestrador

Espelho enxuto do `CLAUDE.md` desta pasta, no formato que o OpenCode e o
Hermes carregam sozinhos ao rodar a partir daqui. Fonte de verdade pro
detalhe continua no `CLAUDE.md`.

## Regras

- Consultar `../catalogos/agentes.md`, `../catalogos/skills.md` e
  `../catalogos/mcps.md` antes de criar agente, skill ou integração nova.
- Nunca instalar agente vindo da internet sem ler o código antes.
- Nunca ficar parado esperando resposta de outro agente — mandar o pedido
  e continuar em outra tarefa.
- Usar `herdr agent prompt <nome> "texto" --wait` como canal primário com
  agente na mesma máquina.
- Dar nome fixo a cada agente com `herdr agent rename` assim que ele sobe.
- Nunca colocar segredo (chave, senha, token) em arquivo — usar variável
  de ambiente.
- Confirmar com o usuário antes de qualquer ação destrutiva ou
  irreversível.
- Só criar agente novo com aprovação do usuário.
- Devolver tarefa fora do escopo pro agente dono, nunca tentar cobrir
  sozinho.
