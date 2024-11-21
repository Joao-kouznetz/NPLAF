# Como rodar o applicativo

## Api da open AI

coloque em um arquivo .env a sua credencial da openAi

gere uma secret_key para criptografia

Create a random secret key that will be used to sign the JWT tokens.

To generate a secure random secret key use the command:

```
openssl rand -hex 32
```

# Como rodar a aplicação?

Para rodar a aplicação em a sua máquina local é apenas necessário ter o docker baixado utilizar o comando abaixo.

``` zsh
docker-compose up --build
```

e para descer o app fazer

``` zsh
docker-compose down
```

depois de fazer isso a primeira vez pode so utilizar o seguinte, pois ja vai ter a imagem no seu computador:

```zsh
docker-compose up
```

Abaixo tem o relatório desenvolvido... Também é possível acessá-lo no pdf no repositorio

# Relatório sobre problema

## Problema a ser resolvido

A correção automática de questões dissertativas. Caso isso seja possível, pode reduzir a sobrecarga dos professores com tarefas de correção, permitindo que tenham mais tempo para focar em atividades pedagógicas. Além disso, os alunos poderiam estudar de forma mais realista, respondendo questões dissertativas e recebendo feedback automatizado.

---

## Ferramentas existentes e limitações

Já existem ferramentas que abordam aspectos relacionados a esse problema, como:

### 1. Correção de Gramática e Ortografia

- **Trinka.ai**: Focado na revisão de textos acadêmicos, identificando erros gramaticais e ortográficos.
- **Grammarly e Writefull**: Melhoram a redação de textos, mas não avaliam conteúdo dissertativo.

### 2. Correção Automática de Questões Fechadas

- **ExamIo e Blackboard**: Corrigem exercícios de múltipla escolha rapidamente, aliviando a carga dos professores, mas ainda não atendem questões dissertativas.

### 3. Assistentes Educacionais com IA

- **Duolingo**: Implementa IA generativa para auxiliar alunos na prática de conversação e escrita.
- **Khan Academy**: Utiliza IA generativa em cursos para responder dúvidas dos alunos e, com o recurso *Khanmigo*, oferece suporte para atividades e feedback em redações.

Embora *Khanmigo* seja o mais próximo do escopo do problema abordado, ainda não é uma ferramenta dedicada exclusivamente à correção automática de questões dissertativas de maneira autônoma.

---

## Práticas de correção em escolas

Para entender como a correção de questões dissertativas é realizada atualmente, entrevistei dois professores de uma escola particular em São Paulo:

### 1. Professor de Biologia

- Elabora um gabarito para as provas e o disponibiliza para os alunos após a realização.
- A correção é feita manualmente e o tempo gasto varia de acordo com sua disponibilidade.
- Informou que não corrige as lições de casa dos alunos.
- Mencionou que não confiaria em inteligência artificial para corrigir suas provas.

### 2. Professora de História

- Avalia os alunos com base em textos, considerando critérios específicos para a elaboração das respostas.
- Explicou que não utilizaria um modelo de inteligência artificial para corrigir provas, pois acredita que isso diminuiria o contato com os alunos.

---

# Descrevendo minha ferramenta

Minha ferramenta inicial foi desenvolvida antes das conversas com os professores. Ela consistia em um sistema onde o usuário fornecia a questão, a resposta do aluno e o gabarito. Em seguida, o sistema retornava se a resposta do aluno estava **correta**, **errada** ou **incompleta**.

---

## Medindo impacto

Para avaliar o impacto da ferramenta no auxílio à correção de questões e na redução do tempo gasto pelos professores, coletei provas corrigidas (de história). A partir dos resultados, elaborei manualmente questões em um formato diferente para testes.

### Descobertas

- A ferramenta não foi eficaz na correção de textos longos que exigem múltiplos critérios.
- Mostrou-se surpreendentemente eficiente em corrigir perguntas fechadas com gabarito estruturado.

Apresentei os resultados aos professores, mas suas opiniões não mudaram. Ambos continuaram a não desejar utilizar inteligência artificial para corrigir provas. No entanto, o professor de biologia sugeriu que a ferramenta poderia ser útil no aprendizado dos alunos, especialmente para corrigir lições de casa, permitindo que eles recebessem feedback imediato, sem precisar consultar um gabarito manualmente.

---

## Refatorando a ferramenta

Com base nos feedbacks e na mudança do público-alvo (de professores para alunos), refatorei a ferramenta. Agora, ela:

- Indica se a resposta está **certa** , **errada** ou **incompleta** .
- Fornece recomendações específicas sobre o que o aluno pode **acrescentar** ou **remover** para que a resposta seja considerada correta.

Essa versão foi considerada interessante pelo professor.

---

## Medindo impacto 2

Conversei com dois ex-alunos da escola e propus que respondessem duas perguntas usando a ferramenta.

### Resultados

- Em nenhuma das perguntas os alunos acertaram na primeira tentativa.
- Com as recomendações fornecidas pela ferramenta, ambos revisaram suas respostas e chegaram à solução correta.

### Conclusão

O teste demonstrou que a ferramenta pode incentivar os alunos a refletirem e revisarem suas respostas de forma independente, promovendo aprendizado ativo mesmo sem intervenção direta de um professor.

---

# Exemplos testados

Pergunta:
Compare as teorias de evolução propostas por Darwin e Lamarck, destacando os pontos principais de cada uma.
Gabarito:

Charles Darwin propôs a teoria da seleção natural como o principal mecanismo de evolução. Segundo essa teoria, os indivíduos de uma população apresentam variações herdáveis, e aqueles com características que lhes conferem maior vantagem em seu ambiente têm maior probabilidade de sobreviver e se reproduzir. Com o tempo, essas características vantajosas tornam-se mais comuns na população. Para Darwin, a evolução ocorre por meio de um processo gradual e cumulativo, impulsionado pela sobrevivência diferencial dos mais aptos.

Jean-Baptiste Lamarck, por outro lado, acreditava que a evolução se dava pelo uso e desuso de estruturas e pela transmissão de características adquiridas. Em sua teoria, os organismos se adaptavam ao longo de suas vidas em resposta às necessidades impostas pelo ambiente, e essas adaptações eram passadas para seus descendentes. Um exemplo clássico de sua teoria é o pescoço das girafas, que, segundo Lamarck, teria se alongado porque os ancestrais das girafas esticavam o pescoço para alcançar folhas mais altas.

Pergunta:

Explique o papel das enzimas na digestão humana, destacando onde elas atuam e como contribuem para a absorção de nutrientes.

Gabarito:

As enzimas desempenham um papel fundamental na digestão humana, catalisando reações químicas que quebram macromoléculas em moléculas menores, facilitando sua absorção pelo organismo. No ambiente oral, a amilase salivar inicia a digestão do amido, quebrando-o em maltose. No estômago, a pepsina, ativada pelo ambiente ácido, degrada proteínas em peptídeos menores. No intestino delgado, enzimas como tripsina e quimotripsina, produzidas pelo pâncreas, continuam a digestão de proteínas, enquanto a amilase pancreática converte o amido restante em açúcares simples. Além disso, lipases quebram lipídeos em ácidos graxos e glicerol. As enzimas do intestino delgado, como maltase, lactase e sucrase, completam a digestão de carboidratos. Esses processos garantem que os nutrientes sejam transformados em formas absorvíveis, como aminoácidos, glicose e ácidos graxos, que serão transportados pelo sangue para utilização no metabolismo celular.

{
  
  "gabarito":"A seleção natural é um processo pelo qual características hereditárias que contribuem para a sobrevivência e a reprodução se tornam mais comuns numa população, enquanto características prejudiciais tornam-se mais raras. Isto ocorre porque indivíduos com características vantajosas têm mais sucesso na reprodução, de modo que mais indivíduos na próxima geração herdem tais características.",
  "questao": "Descreva o que é seleção natural",
  "texto":"Seleção natural é um método evolutivo desenvolvido por cientistas como Charles Darwin. Esse processo indica como são selecionadas as  characteristics de uma espécie  que são transmitidas para o seus descendentes. Na teoria evolutiva se diz que as características são criadas aleatoriamente e com a seleção natural, ou seja a capacidade de o ambiente, o ecossistema em que a espécie vive filtra isso com base na sobrevivência do indivíduo e na capacidade de reprodução desse indivíduo então características que permitem que o indivíduo sobreviva mais e tenham mais sucesso na reprodução são transmitidas mais para seus descendentes."
}

# exemplo de avaliação testada

Texto do aluno:

A crise dos preços, que ocorreu no fim do século XIX, foi superada pelas potências europeias e os EUA devido a certas mudanças no capitalismo decorrentes da Segunda Revolução Industrial! O principal motivo pelo aumento de preços (recuperação da crise) foi a concentração de capital nas mãos das elites, consequência da monopolização da economia europeia e estado-unidense. Tal fenômeno ocorre devido à rápida industrialização e aumento de técnicas, que forçam as elites corporativas a formarem carteis (nos EUA são trustes) que possibilitam uma fixação de preços em um mercado na qual a direção natural deles sera para baixo. Os carteis e trustes possibilitaram uma monopolização do equilíbrio entre oferta e demanda (preços) nas mãos da elite, funilando o capital para as corporações e grandes empresas. Outra característica assumida pelo capitalismo
eu função da saída da crise dos preços foi o protecionismo. Nos EUAe Alemanha, tal estratégia impulsionou a s duas potências no patamar de
"superpotências" no início do século XX. A intervenção dos estados no controle de tarifas de importação agiram como um escudo defendendo o mercado interno do livre mercado e Segunda Revolução Industrial, aumentando investimento interno e fortelecendo a industria nacional A Inglaterra não adotou tal estratégia permanecendo participantes do mercado "livre", uma decisão que provou-se errônea, provocando a superação industrial da Alemanha e EUA. Assim, as características tanto econômicas quanto políticas assumidas pelo capitalismo a partir da sequnda revolução  Industrial ajudaram na recuperação da crise e na formação de um novo cenáro mundial na virada /início do século XX

Gabarito:

Gabarito: Introdução: contexto (tempo: 1873-1896, lugar: Europa e Estados Unidos da América; tema: Capitalismo monopolista e 2ª Revolução Industrial

Dados fornecidos pela tabela: No período de 1875 a 1879 há um certo equilíbrio no que diz respeito ao índice de produção industrial no Reino Unido, França, Alemanha e Estados Unidos.

Crise de 1873-1896: A partir do aprofundamento da crise de 1873, caracterizada por déflação e crise de
lucros, nota-se uma ascensão acelerada da Alemanha e dos Estados Unidos, seguidos de longe pela França, e uma desaceleração relativa da Inglaterra, até então sede do sistema capitalismo mundial (hegemonia).  Recuperação da Crise: Essa aceleração se deu através da prática do protecionísmo que visava diminuir a concorrência entre as indústrias nacionais e, assim, fazer os preços subirem internamente o que possibilitará a recuperação da crise.  No entanto, a Inglaterta, extremamente dependente das matérias-primas externas para alimentar as suas
indústrias não consegue abandonár o livre-comércio, levando aos baixos aumentos nos seus índices de produção ao longo dos anos até 1913.

Características assumidas pelo capitalismo: A partir de 1896, a saída encontrada para recuperar-se da crise de preços se consolida na forma do capitalismo monopotista, caracterizado por protecionismo estatal - barreiras alfandegárias visando aumentar o preço dos produtos importados, grandes empresas e concentração de capital, como os cartéis - a combinação de preços entre as empresas com vistas a garantir os lucros esperados -, e o truste

conglomerado de empresas que partilha o mesmo conselho administrativo, com tomada de decisões coletivas que garantem o sucesso das empresas.

2ª Revolução Industrial: As características assumidas pelo capitalismo monopolista, principalmente na
Alemanha e Estados Unidos, possibilitam o investimento massivo dos excedentes de capitais em indústrias de inovação - o protecionismo possibilita o excedente de capitais; a estruturas das grandes empresas asseguram as grandes somas de investimentos que exigem as indústrias química e elétrica da 2ª Revolução industrial; e os
carteis e trustes garantem que a concorrência não seja um impedimento para as altas margens de lucros

Conclusão: Assim, conforme reiterado pelos dados fornecidos pela tabela, às vésperas da 1ª GM Alemanha e Estados Unidos disputam a hegemonia perdída pelo Reino Unido, tendo suas riquezas advindas do capitalismo monopolista e da 2ª Revolução Industrial.

### Como foi testada a questão acima

Questão acima foi testada passando todos os topicos junto com o texto e passando cada tópico de maneira separada
