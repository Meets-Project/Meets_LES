# Diagramas do Meets em draw.io

Fontes editáveis (.drawio, XML mxGraph) usadas na cópia do Canva "Meets — Casos de Uso (draw.io)".
O conteúdo é o mesmo de `../fontes-elk` (mesmos textos e numeração dos passos, FP/FA/FE).

- Classe, DER e MER: posição dos nós e arestas do layout ELK (`_geometria-mermaid.json`).
- Sequência: linhas de vida UML (ator, boundary, control, entity, banco), mensagens numeradas, quadros alt/opt/loop/par e notas FA/FE.
- Atividade: UML com raias verticais (uma por ator), nó inicial/final, decisões com guardas [condição] e nós de objeto `i : Item [estado]` (seta tracejada).

Abrir para editar: clique no link (abre no diagrams.net a partir do GitHub; para salvar, use *Arquivo → Salvar como* no seu Drive/dispositivo ou faça o commit do arquivo).

## Visão geral e atividades de negócio

- [negocio-1-evento](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fnegocio-1-evento.drawio)
- [negocio-2-conteudo](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fnegocio-2-conteudo.drawio)
- [negocio-3-moderacao](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fnegocio-3-moderacao.drawio)
- [negocio-4-analise](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fnegocio-4-analise.drawio)
- [sem-sistema](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fsem-sistema.drawio)

## Atividades dos casos de uso (stand-by: #015, #005, #006)

- [atividade-005-avaliar-evento](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fatividade-005-avaliar-evento.drawio)
- [atividade-006-avaliar-apresentador](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fatividade-006-avaliar-apresentador.drawio)
- [atividade-007-ranking](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fatividade-007-ranking.drawio)
- [atividade-008-dashboards](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fatividade-008-dashboards.drawio)
- [atividade-013-denuncias](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fatividade-013-denuncias.drawio)
- [atividade-015-lembrete](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fatividade-015-lembrete.drawio)

## Diagramas de classe

- [classe-005-avaliar-evento](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fclasse-005-avaliar-evento.drawio)
- [classe-006-avaliar-apresentador](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fclasse-006-avaliar-apresentador.drawio)
- [classe-007-ranking](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fclasse-007-ranking.drawio)
- [classe-008-dashboards](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fclasse-008-dashboards.drawio)
- [classe-013-denuncias](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fclasse-013-denuncias.drawio)
- [classe-015-lembrete](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fclasse-015-lembrete.drawio)

## DER (recortes e gerais)

- [der-005-avaliar-evento](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fder-005-avaliar-evento.drawio)
- [der-006-avaliar-apresentador](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fder-006-avaliar-apresentador.drawio)
- [der-007-ranking](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fder-007-ranking.drawio)
- [der-008-dashboards](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fder-008-dashboards.drawio)
- [der-013-denuncias](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fder-013-denuncias.drawio)
- [der-015-lembrete](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fder-015-lembrete.drawio)
- [der-geral-1-usuarios-rede-comunicacao](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fder-geral-1-usuarios-rede-comunicacao.drawio)
- [der-geral-2-conteudo-interacoes](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fder-geral-2-conteudo-interacoes.drawio)
- [der-geral-3-avaliacao-moderacao](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fder-geral-3-avaliacao-moderacao.drawio)

## MER conceitual

- [mer-005-avaliar-evento](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fmer-005-avaliar-evento.drawio)
- [mer-006-avaliar-apresentador](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fmer-006-avaliar-apresentador.drawio)
- [mer-007-ranking](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fmer-007-ranking.drawio)
- [mer-008-dashboards](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fmer-008-dashboards.drawio)
- [mer-013-denuncias](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fmer-013-denuncias.drawio)
- [mer-015-lembrete](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fmer-015-lembrete.drawio)
- [mer-geral](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fmer-geral.drawio)

## Sequência (linguagem do código, FP/FA/FE)

- [sequencia-005-avaliar-evento](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fsequencia-005-avaliar-evento.drawio)
- [sequencia-006-avaliar-apresentador](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fsequencia-006-avaliar-apresentador.drawio)
- [sequencia-007-ranking](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fsequencia-007-ranking.drawio)
- [sequencia-008-dashboards](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fsequencia-008-dashboards.drawio)
- [sequencia-013-denuncias](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fsequencia-013-denuncias.drawio)
- [sequencia-015-lembrete](https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FMeets-Project%2FMeets_LES%2Fdocs%2Fdiagramas-elk%2FDocumenta%25C3%25A7%25C3%25A3o%2FDocumentos%2520Meets%2Fdiagramas_LES%2Fapresentacao%2Ffontes-drawio%2Fsequencia-015-lembrete.drawio)

## Regerar

```bash
cd ../slides
python3 geometria_mermaid.py <svgs> ../fontes-drawio/_geometria-mermaid.json <svgs>/*.svg   # SVGs do mmdc (layout ELK)
python3 gerar_drawio.py                  # → ../fontes-drawio/*.drawio
DRAWIO_VIEWER=viewer-static.min.js python3 render_drawio.py ../drawio ../fontes-drawio/*.drawio   # → ../drawio/*.png
CHROMIUM=... python3 gerar_slides_drawio.py   # → png-drawio/
```

`viewer-static.min.js` vem do repositório jgraph/drawio (src/main/webapp/js).
