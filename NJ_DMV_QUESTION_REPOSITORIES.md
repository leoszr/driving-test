# Repositórios de perguntas para o NJ MVC

Pesquisa feita em 3 de setembro de 2026.

## Resultado

### 1. Melhor fonte reutilizável

**[s-inu/NJ-Driving_Knowledge_Test-Questions-Pool-BreakDown](https://github.com/s-inu/NJ-Driving_Knowledge_Test-Questions-Pool-BreakDown)**

- É o único repositório encontrado cujo conteúdo é claramente específico de New Jersey.
- O arquivo principal, [`NJ DMV Knowledge Test_plus_image_link.txt`](https://github.com/s-inu/NJ-Driving_Knowledge_Test-Questions-Pool-BreakDown/blob/main/NJ%20DMV%20Knowledge%20Test_plus_image_link.txt), tem 1.288 linhas e cerca de 169 KB segundo a API do GitHub.
- Formato: texto tabulado, com enunciado, alternativa correta marcada, alternativas A–D e separadores.
- Idiomas: inglês e chinês.
- Inclui referências a imagens para algumas questões de placas.
- Última atualização observada no repositório: 9 de junho de 2024.
- Não há arquivo `LICENSE` na raiz. Portanto, o código/conteúdo não tem permissão explícita de reutilização, modificação ou redistribuição.

**Avaliação:** melhor ponto de partida técnico para análise ou conversão, mas não deve ser copiado para um produto sem autorização do autor ou substituição por conteúdo próprio baseado no manual oficial.

### 2. Aplicativo multiestado, com utilidade limitada

**[harish-kunta/USdrivinglicense](https://github.com/harish-kunta/USdrivinglicense)**

- Aplicativo Android de simulados para todos os estados.
- O arquivo [`app/src/main/res/values/arrays.xml`](https://github.com/harish-kunta/USdrivinglicense/blob/master/app/src/main/res/values/arrays.xml) lista New Jersey entre os estados disponíveis.
- O README afirma que as perguntas são baseadas nos manuais oficiais de cada estado.
- A inspeção não encontrou um banco local claramente separado e identificável como “perguntas de New Jersey”; o projeto aparenta obter ou selecionar conteúdo em tempo de execução.
- Última atualização observada: 18 de fevereiro de 2022.
- Não há arquivo `LICENSE` na raiz.

**Avaliação:** pode ajudar a entender fluxo e UI de um quiz, mas não é uma boa fonte direta de um dataset auditável de NJ.

## Projetos descartados

- [`jrm2k6/dmv-practice`](https://github.com/jrm2k6/dmv-practice): possui perguntas Class C em JSON, mas não há evidência de que sejam específicas de New Jersey.
- [`heiner/dmv.md`](https://gist.github.com/heiner/7b20b021dca9ed0f00fea4aaf4478483): perguntas gerais de DMV; não identificadas como NJ.
- [`psegurap/us-driving-practice-test`](https://github.com/psegurap/us-driving-practice-test): projeto multiestado em espanhol; a busca no código não encontrou “New Jersey”.
- [`TGilany/DrivingTest`](https://github.com/TGilany/DrivingTest): repositório recente, mas a busca não revelou um banco indexado de perguntas de NJ.

## Fontes oficiais para validar ou criar perguntas

- [NJ MVC — Sample Knowledge Test](https://nj.gov/mvc/license/sample_knowledge_test.htm)
- [NJ MVC — respostas do teste de exemplo](https://www.nj.gov/mvc/license/answers.htm)
- [NJ MVC — Driver Manuals](https://www.nj.gov/mvc/about/manuals.htm)
- [New Jersey Driver Manual em PDF](https://nj.gov/mvc/pdf/license/drivermanual.pdf)

O NJ MVC informa que o exame geral tem 50 questões e exige 40 respostas corretas (80%). O manual oficial listado pelo MVC estava marcado como revisado em setembro de 2025 na data desta pesquisa.

## Recomendação

Use o repositório `s-inu` apenas como referência para mapear temas e formato. Para este projeto, a opção juridicamente e tecnicamente mais segura é produzir perguntas próprias, com respostas e explicações verificadas no manual atual do NJ MVC. Guarde em cada questão a seção ou página usada como fonte. Isso evita depender de material sem licença e facilita atualizar itens quando a lei ou o manual mudar.
