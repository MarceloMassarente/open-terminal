# Mapeamento da integração Open Terminal ↔ OpenWebUI (arquivos no contêiner)

Este documento descreve **como o Open Terminal expõe o filesystem interno do contêiner para a UI do OpenWebUI** (barra lateral de arquivos com upload/download/preview/edição) e como replicar o padrão em outro tool server.

## 1) Como o OpenWebUI enxerga o Open Terminal

No OpenWebUI, essa integração não é configurada como MCP/tool server comum: ela é uma conexão específica de **Open Terminal**. Isso habilita no frontend um navegador de arquivos com ações de listar, abrir, editar, upload e download.

- Conexão “Direct”: browser do usuário chama o Open Terminal diretamente.
- Conexão “System-Level”: backend do OpenWebUI atua como proxy para o Open Terminal.

## 2) Contrato HTTP que habilita navegação de arquivos

O Open Terminal fornece endpoints REST para filesystem (todos com API key via bearer, exceto health). O padrão de operação é path-based, com `os.path.abspath(...)` para normalização.

### Descoberta/capability
- `GET /api/config` → retorna feature flags (ex.: `terminal: true/false`) para o cliente adaptar UI.

### Navegação
- `GET /files/cwd` → cwd atual.
- `POST /files/cwd` → altera cwd.
- `GET /files/list?directory=...` → lista diretório com metadados (`name`, `type`, `size`, `modified`).

### Leitura/visualização
- `GET /files/read?path=...` → leitura textual para consumo do agente; para binários só permite prefixes configurados (ex.: `image/*`) e extrai texto de PDF.
- `GET /files/view?path=...` → serve bytes brutos com MIME correto para preview/download na UI (sem restrição de tipo binário de `read`).
- `GET /files/display?path=...` → sinal de “abrir no viewer do cliente” (não retorna conteúdo).

### Escrita/gestão
- `POST /files/write` → grava texto em arquivo.
- `POST /files/mkdir` → cria diretório.
- `DELETE /files/delete?path=...` → remove arquivo/pasta.
- `POST /files/move` → move/renomeia.
- `POST /files/replace` → replace textual estruturado.

### Busca
- `GET /files/grep` → busca conteúdo textual em árvore.
- `GET /files/glob` → busca por padrão de nome/caminho.

### Upload
- `POST /files/upload?directory=...`:
  - multipart (`file`) para upload direto da UI;
  - ou `url=...` para o servidor baixar remotamente e salvar.

## 3) Como upload/download funcionam na prática na UI

### Upload
1. Usuário escolhe arquivo no OpenWebUI.
2. UI envia multipart para `POST /files/upload` com `directory` destino.
3. Servidor cria pasta (se necessário) e grava bytes.
4. UI atualiza listagem com `GET /files/list`.

### Download
Não há endpoint "download" dedicado no estado atual (os temporários foram removidos/deprecados).

Fluxo típico:
1. UI solicita `GET /files/view?path=...`.
2. Como resposta é binária com MIME adequado, o browser pode abrir preview ou disparar download.

## 4) Regras de segurança/comportamento que impactam integração

- Autenticação por bearer (`verify_api_key`) aplicada aos endpoints de arquivos.
- CORS configurável (`CORS_ALLOWED_ORIGINS`) para suportar chamadas diretas do browser no modo Direct.
- Endpoints internos relevantes podem estar `include_in_schema=False`, ou seja, integração depende de contrato conhecido entre OpenWebUI e Open Terminal, não apenas do OpenAPI público.
- Não existe sandbox/chroot no código atual de arquivos: caminhos absolutos são aceitos; o isolamento normalmente vem do contêiner em que o serviço roda.

## 5) Blueprint para replicar em outro tool server

Implemente os seguintes blocos:

1. **Auth + CORS**
   - Bearer token único por instância/tenant.
   - CORS com allowlist explícita para o domínio do OpenWebUI (modo Direct).

2. **API de arquivos compatível**
   - Mesmo conjunto semântico de endpoints acima.
   - Respostas de listagem com metadados consistentes.

3. **Dois caminhos de leitura**
   - `read` para texto/LLM (com proteção para binário).
   - `view` para bytes brutos (preview/download pela UI).

4. **Upload multipart**
   - Aceitar upload direto do navegador para pasta alvo.
   - Opcional: upload por URL no backend.

5. **Descoberta de capacidades**
   - Endpoint tipo `/api/config` para flags (ex.: terminal habilitado).

6. **Isolamento de filesystem (recomendado para produção)**
   - Definir `ROOT_DIR` e rejeitar path traversal fora da raiz permitida.
   - Opcional: montar volumes por usuário/tenant.

7. **Erros previsíveis para UI**
   - `404` para não encontrado, `400` para path inválido, `409` conflito de destino, `415` tipo não suportado.

## 6) Checklist mínimo de compatibilidade OpenWebUI-like

- [ ] `GET /health`
- [ ] `GET /api/config`
- [ ] `GET /files/list`
- [ ] `GET /files/read`
- [ ] `GET /files/view`
- [ ] `POST /files/upload` (multipart)
- [ ] `POST /files/write`
- [ ] `DELETE /files/delete`
- [ ] Auth bearer em todos os endpoints sensíveis
- [ ] CORS correto para modo browser-direct

## 7) Observação arquitetural

O MCP neste projeto (`FastMCP.from_fastapi`) expõe as rotas como ferramentas para agentes, mas a experiência de **navegação de arquivos com upload/download na UI** vem da integração Open Terminal dedicada no OpenWebUI e do contrato REST acima.
