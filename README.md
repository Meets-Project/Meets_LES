# Meets

Aplicativo social para divulgação e participação em eventos, publicação de conteúdos e avaliação gamificada de apresentadores (Projeto Integrador — ADS).

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `Código/backend` | API REST (Node.js 20+, Express 5, PostgreSQL). Camadas: `src/app.js` e `src/routes/` (rotas), `src/services/` (moderação, pontuação, relógio), repositórios SQL (`src/*Repository.js`, `src/repository.js`). |
| `Código/backend/migrations` | Migrações SQL versionadas; `rollback/` tem o script de desfazer de cada uma a partir da 010. |
| `Código/snack` | Aplicativo React Native / Expo (Android, iOS e web). |
| `Documentação/Documentos Meets` | Documento de Visão, Atividades do Negócio, Requisitos, Casos de Uso e Modelagem (`.docx`, com cópia em `PDF/`). |
| `Documentação/Documentos Meets/diagramas_LES` | Diagramas em PNG; as fontes editáveis (Mermaid/Graphviz) ficam em `fontes/`. |
| `Documentação/Documentos Meets/gerador` | Script que gera os documentos Word a partir de dados conferidos com o código. |
| `Documentação/Template_professora` | Modelos e regras da disciplina. |

## Como rodar a API

### Opção 1: Rodando com Docker Compose (Recomendado)

Inicia o banco de dados PostgreSQL e a API automaticamente:

```bash
# Iniciar o banco e o backend em segundo plano:
docker compose up -d

# Ver logs do backend em tempo real:
docker logs -f meets_backend

# Pausar os containers:
docker compose stop

# Reiniciar os containers pausados:
docker compose up -d

# Parar e remover os containers:
docker compose down
```

### Opção 2: Rodando a API localmente (com Hot-Reload)

Caso queira editar o código do backend e ver alterações instantâneas sem rebuild do Docker:

```bash
# 1. Inicie apenas o banco PostgreSQL no Docker:
docker compose up -d postgres

# 2. Rode o backend no seu terminal:
cd Código/backend
cp .env.example .env        # ajuste se necessário (o padrão já aponta para localhost:5432)
npm install
npm run migrate             # aplica as migrações (também roda ao iniciar)
npm run dev                 # http://localhost:3333 (com reload automático ao salvar)
npm test                    # testes (Vitest + Supertest + pg-mem)
```

Variáveis importantes: `JWT_SECRET` (obrigatória em produção), `APP_TIMEZONE` (padrão `America/Sao_Paulo`, usada para saber se um evento já terminou), `CORS_ORIGIN`, `SMTP_*` (código de verificação de e-mail; sem SMTP, em desenvolvimento o código aparece no log).

### Primeiro administrador

O primeiro administrador é definido por linha de comando, depois de a pessoa se cadastrar no app:

```bash
npm run make-admin -- email@exemplo.com
```

Os demais administradores podem ser promovidos pela tela **Manter usuários**.

### Desfazer uma decisão (rollback)

Cada decisão de escopo tem a sua migração e o seu commit. Para desfazer a parte de banco de uma delas:

```bash
npm run rollback -- 015_drop_live_rooms   # desfaz a última primeiro (015 → 010)
```

Depois, reverta o commit correspondente com `git revert`.

## Como rodar o aplicativo

```bash
cd Código/snack
cp .env.example .env        # configure EXPO_PUBLIC_API_URL=http://localhost:3333
npm install
npm run web                 # abre a versão Web diretamente no navegador
# ou
npx expo start              # Android/iOS/web em desenvolvimento (QR Code para app Expo Go)
npm run build               # gera a versão web em dist/ (publicada na Vercel)
```

O endereço da API fica em `data/apiConfig.js` (porta 3333 local; Render em produção). Depois de alterar o código, gere o `dist/` de novo antes de publicar.

## Documentação

Os documentos são gerados por script para continuarem iguais ao código:

```bash
cd "Documentação/Documentos Meets/gerador"
python3 gerar.py            # requer python-docx, Pillow, LibreOffice e pdftotext
```

Requisitos e regras ficam em `gerador/dados.py`, e os casos de uso em `gerador/casos_de_uso.py`. Ao mudar uma regra no código, ajuste o dado correspondente e gere de novo. Os diagramas são gerados a partir de `diagramas_LES/fontes` (Mermaid CLI e Graphviz).

Os arquivos do Astah (`astah/`) são da primeira versão e **não** foram atualizados; os diagramas válidos são os de `diagramas_LES`.
