# Diagramas da cópia do deck original (layout ELK)

Fontes Mermaid usadas na cópia do Canva "Meets — Casos de Uso" com layout ELK.

- Todos os diagramas (exceto casos de uso e sequência) têm `layout: elk`.
- Os diagramas de sequência usam os nomes do código (telas, `api.js`, rotas, repositórios)
  e marcam os fluxos: FP (principal), FA (alternativo) e FE (exceção).
- `mer-geral.mmd` e `der-geral-*.mmd` são o modelo completo (slides 8 a 11).

Renderizar: `mmdc -i arquivo.mmd -o ../elk/arquivo.png -s 3 -b white -w 1800`
Slides: `CHROMIUM=... python3 ../slides/gerar_slides_elk.py` (gera `../slides/png-elk`).
