---
fontSize: 11
lineSpacing: 1.3
paragraphSpacing: 8
align: left
titleAlign: left
---

# Método de Continuidade do Projeto — Pilares em Python

## Por que isso é necessário

Um chat com IA não é um banco de dados confiável de longo prazo: histórico pode ser perdido, truncado ou você pode trocar de modelo/sessão. A solução é **nunca depender da memória do chat** — toda decisão importante, todo código e todo próximo passo vive em **arquivos dentro da pasta do projeto**, versionados como qualquer código.

**Regra de ouro:** se não está escrito num arquivo da pasta, não aconteceu.

---

## 1. Estrutura de pastas sugerida

```
Pilarespython-Corsini/
│
├── CONTEXTO.md                  ← arquivo raiz, visão geral do projeto (lido primeiro, sempre)
├── GLOSSARIO.md                 ← símbolos e termos técnicos (fck, εcu, Sd, Rd...)
│
├── aulas/
│   ├── aula01_resumo.md
│   ├── aula02_resumo.md
│   ├── aula03_resumo.md
│   └── Aula_0X_Materiais.pdf    ← PDFs originais das aulas, para referência
│
├── sessoes/
│   ├── 2026-11-17_sessao01.md   ← resumo de cada sessão de trabalho/estudo
│   ├── 2026-11-18_sessao02.md
│   └── ...
│
├── codigo/
│   ├── materiais.py              ← leis constitutivas (aula 02)
│   ├── geometria.py               (futuro)
│   ├── estados_limite.py          (futuro)
│   └── testes/
│       └── test_materiais.py
│
├── docs_automacao/
│   ├── agenda_pilares.py
│   ├── credentials.json          ⚠️ nunca versionar/compartilhar
│   ├── token.json                ⚠️ nunca versionar/compartilhar
│   └── manual_agenda.md
│
└── decisoes/
    └── DECISOES.md               ← log cronológico de decisões técnicas importantes
```

**Por que separar assim:**
- `aulas/` = conteúdo teórico (o que o professor explicou)
- `codigo/` = o que você está construindo
- `sessoes/` = histórico de cada "turno de trabalho" com a IA
- `decisoes/` = só as decisões que importam manter (evita re-explicar o mesmo raciocínio)

---

## 2. O que registrar em `CONTEXTO.md` (arquivo-mestre)

Esse é o **primeiro arquivo que você cola/anexa** em qualquer novo chat, com qualquer IA. Ele deve responder: "o que é este projeto, onde estamos, o que falta".

```markdown
# CONTEXTO.md — Pilares em Python (Curso Ricardo Corsini)

## O que é o projeto
Implementação em Python de um verificador de resistência de seções de
concreto armado à flexocompressão oblíqua (ELU), seguindo o curso
"Pilares em Python - Parte I" do professor Ricardo Corsini.

## Objetivo final
Dado: geometria da seção, materiais, armaduras, NSd, Mx,Sd, My,Sd
→ Programa decide se a seção resiste, e gera a curva de interação Mx-My.

## Estado atual (atualizar sempre)
- Aulas estudadas: 01 (escopo/convenções), 02 (materiais no ELU)
- Código escrito: função `parametros_concreto()`, `tensao_concreto()`, `tensao_aco()`
- Código testado: sim, conferências da seção 2.13 da aula 02
- Próxima aula do curso: Ciclo 07 (quinta, 19/11, 20h) — Estados-limite de deformação

## Convenções fixas do projeto (não mudar sem registrar em DECISOES.md)
- Compressão positiva, tração negativa
- Unidades internas: mm, mm², MPa, N, N·mm; deformação adimensional
- gamma_c = 1.40, gamma_s = 1.15, Es = 210000 MPa
- NSd >= 0 apenas (flexotração fora do escopo desta versão)

## Links rápidos
- Resumos de aula: ./aulas/
- Log de decisões: ./decisoes/DECISOES.md
- Última sessão: ./sessoes/ (ver arquivo mais recente)
```

---

## 3. Documentar contexto técnico sem duplicar código

**Regra:** `CONTEXTO.md` e os resumos de sessão **nunca colam o código inteiro** — eles apontam para o arquivo e explicam a decisão por trás dele.

Exemplo de como registrar isso no `DECISOES.md`:

```markdown
## 2026-11-17 — Vetorização das leis de materiais
**Decisão:** usar NumPy com máscaras booleanas (comp, parab, plateau) em
vez de loop com if/else por fibra.
**Motivo:** performance ao avaliar milhares de fibras; padrão usado pelo
próprio material do curso (aula 02, seção 2.8).
**Onde está:** codigo/materiais.py, função tensao_concreto()
**Cuidado:** np.clip() no aço limita ±fyd preservando sinal — não usar
valor absoluto, perde a distinção tração/compressão.
```

Isso evita duplicar 50 linhas de código em três arquivos diferentes — você sempre aponta para a fonte única (`codigo/materiais.py`).

Para **comandos e configurações** (ex: ambiente virtual, instalação), mantenha em um arquivo único e reaproveitável — no seu caso, já existe o manual "Dicas de Criação de Ambiente Virtual", e deve ficar referenciado no `CONTEXTO.md`, não recopiado.

---

## 4. Procedimento de fechamento/retomada de sessão

### Ao final de cada sessão (5 minutos, sempre):
1. Abra `sessoes/AAAA-MM-DD_sessaoNN.md` e preencha o modelo da seção 5 abaixo
2. Se tomou alguma decisão técnica nova → adicione uma entrada em `decisoes/DECISOES.md`
3. Se o código mudou → salve o arquivo `.py` real na pasta `codigo/`
4. Atualize a seção **"Estado atual"** do `CONTEXTO.md` (3-4 linhas, sobrescrevendo a anterior)

### Ao começar uma nova sessão (com qualquer IA, inclusive outra):
1. Anexe/cole o `CONTEXTO.md` primeiro
2. Anexe o resumo da **última sessão** (`sessoes/`)
3. Se for continuar um código específico, anexe só o arquivo `.py` relevante
4. Diga explicitamente: "Estamos no projeto X, veja o CONTEXTO.md anexado, última vez paramos em Y, hoje quero fazer Z"

Isso recria o contexto em segundos, sem depender do histórico do chat.

---

## 5. Modelo de resumo de sessão (preencher ao final de cada encontro)

Copie este bloco para um novo arquivo em `sessoes/AAAA-MM-DD_sessaoNN.md`:

```markdown
# Sessão NN — AAAA-MM-DD

## O que foi feito hoje
-

## Aulas/conteúdo estudado
-

## Código escrito ou alterado
- Arquivo:
- O que faz:
- Testado? (sim/não, como)

## Decisões tomadas
- (se houver, também espelhar em decisoes/DECISOES.md)

## Dúvidas abertas / pontos travados
-

## Próximo passo (o que fazer na próxima sessão)
-

## Observações / lembretes
-
```

---

## Recomendação geral de fluxo de trabalho

1. **Um projeto = uma pasta local**, versionada se possível (Git, mesmo que só você use).
2. **`CONTEXTO.md` é sagrado** — é o único arquivo que você garante estar sempre atualizado e sempre recarrega em qualquer sessão nova.
3. **Separe "teoria do curso" de "código do projeto"** — resumos de aula não se misturam com implementação.
4. **Decisões técnicas relevantes vão para um log separado** (`DECISOES.md`), não ficam perdidas em conversas de chat.
5. **Nunca copie-cole código inteiro na documentação** — aponte para o arquivo fonte; documentação referencia, não duplica.
6. **O resumo de sessão é o elo entre um dia e o outro** — 5 minutos de disciplina no fim do dia economizam 30 minutos de "cadê que eu parei" no dia seguinte.

Com essa estrutura, mesmo que o histórico do chat se perca, você recompõe o contexto completo em menos de 1 minuto, com qualquer IA, a qualquer momento.