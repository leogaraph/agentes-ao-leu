# 9router: um endereço pra todos os modelos

[9router](https://github.com/decolua/9router) é um proxy local que junta vários provedores
de modelo (gratuitos e pagos) atrás de um endereço só, no formato da API da OpenAI. O agente
aponta pro 9router e escolhe o modelo pelo nome; trocar de provedor vira trocar uma linha.

O que ele dá pro time:

- **Um provedor pra todo mundo.** OpenCode, Hermes e scripts usam o mesmo endereço.
- **Combos.** Uma lista de modelos em ordem: se o primeiro falha ou bate no limite de uso, o
  9router passa pro seguinte. O agente pede `9router/<combo>` e não sabe qual respondeu.
- **Painel.** Uso, erros e chaves num lugar só.

## Instalar e ligar

```powershell
npm install -g 9router
9router
```

O painel abre em `http://localhost:20128/dashboard`. Conecte lá os provedores (cada um com a
sua chave, que fica só no 9router) e copie a chave do próprio 9router.

Pra apontar uma ferramenta pro 9router sem editar config na mão:

```powershell
npx 9router connect http://localhost:20128 --tools opencode
```

Ou no `opencode.json`, com a chave em variável de ambiente (nunca no arquivo):

```json
{
  "provider": {
    "9router": {
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "http://localhost:20128/v1", "apiKey": "{env:NINEROUTER_KEY}" }
    }
  },
  "model": "9router/<seu-combo>"
}
```

`opencode models | findstr 9router` lista o que ele enxerga. Docs oficiais:
<https://github.com/decolua/9router>.

**Segurança:** o 9router guarda as chaves de todos os provedores. Deixe ele ouvindo só em
`localhost`, com senha no painel, e nunca suba `resultados.csv`, log ou print do painel sem
conferir se tem chave aparecendo.

## Peça pro seu agente

```text
Leia 9router/README.md deste repositório. Instale o 9router (npm install -g 9router) e me
diga quando o painel abrir em http://localhost:20128/dashboard: eu mesmo conecto os
provedores e coloco as chaves, você não digita chave nenhuma. Depois que eu disser "pronto",
ligue o OpenCode nele (npx 9router connect http://localhost:20128 --tools opencode), liste os
modelos gratuitos com opencode models, grave os nomes em 9router/benchmark/modelos.txt e rode
o benchmark em série (python run.py, depois python resumo.py). Me mostre o top 3 de cada
categoria e proponha um combo por categoria (pesquisa, backend, simples), do melhor pro pior.
Eu crio os combos no painel. Chave e senha só em variável de ambiente, nunca em arquivo,
commit ou mensagem.
```

## Qual modelo vai em qual combo: benchmark

Modelo gratuito muda toda semana, e nome bonito não diz se ele acerta. A pasta
[`benchmark/`](benchmark/) testa cada modelo em tarefas de verdade, corrigidas sem humano, e
diz quem vai em cada combo.

| Categoria | Testa | Corrigida por |
|---|---|---|
| `simples` | Seguir formato: um comando, um JSON, uma tabela | regex, chaves de JSON |
| `pesquisa` | Ler arquivo e responder certo | regex com o gabarito |
| `backend` | Corrigir/escrever código que passa em teste | `assert` em Python |

```powershell
cd 9router\benchmark
python run.py --categorias simples --modelos <um-modelo>   # teste rápido
python run.py --retomar                                    # bateria inteira, continua de onde parou
python resumo.py                                           # acerto, tempo e top 3 por categoria
```

- `modelos.txt`: um modelo por linha, com o nome que o 9router usa (sem o `9router/`).
- `tarefas/<categoria>/<nome>.json`: `prompt`, arquivos que a tarefa cria (`arquivos`) e a
  lista `check` (`regex_all`, `regex_none`, `json_keys`, `python_assert`).
- Cada execução roda `opencode run -m 9router/<modelo>` numa pasta temporária, com timeout.
- Modelo que bate no limite de uso 2 vezes seguidas é pulado e marcado.
- Resultado em `resultados.csv`. Rode em série: em paralelo, os gratuitos batem no limite.

Com o resultado, monte um combo por categoria no painel do 9router, do melhor pro pior.
Exemplo de leitura: modelo que tira 100% em `simples` e `pesquisa` mas 0% em `backend` entra
nos dois primeiros combos e fica fora do de código.

Só depende do Python (stdlib) e do OpenCode.
