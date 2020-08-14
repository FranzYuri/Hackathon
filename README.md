![Hackathon 2020 Logo - Projeto Jupiter](https://github.com/Projeto-Jupiter/Hackathon/raw/master/Logo.png)

# BEM VINDOS!

Hoje você faz história participando da primeira Hackathon inter-áreas do Projeto Jupiter!

Não sabe exatamente o que te espera? Não tem problema, a organização estará aqui para te ajudar durante toda a maratona. Vamos começar com um texto introdutório, mas qualquer dúvida, qualquer uma mesmo, estamos à disposição!

# POR ONDE COMEÇAR

Nesta Hackathon, não temos apenas um desafio, mas sim vários! Mais de 70 para dizer a verdade. E agora você vai superar o seu primeiro desafio. Mas antes disso, duas perguntas:

- Já tem conta no GitHub?
- Sua conta já está adicionada à organização do Projeto Jupiter? 

Não ou não sabe? Sem problemas, só entrar em contato com a organização que te ajudamos a resolver esses pré-requisitos. Veja a seção [Comunicação](#COMUNICAÇÃO) para mais detalhes.

Sim e sim? Então já está tudo certo para começarmos, vamos-lá!

## Escolhendo um issue

Cada desafio da Hackathon foi cadastrado como um issue aqui no GitHub. Mas o que é um issue? É quase como uma tarefa, mas vai além. Não tem um prazo para ser entregue, o importante é discutir como resolvé-lo e implementar a solução. Mais detalhes no [GitHub Guides](https://guides.github.com/features/issues/).

Você encontra todos os issues na aba [Issues](https://github.com/Projeto-Jupiter/Hackathon/issues). Cada um deles tem um título e uma descrição que você pode visualizar clicando nele. Além disso, há uma série de labels para te ajudar a escolher um issue, como por exemplo os labels Easy, Medium e Hard que indicam a dificuldade de resolver o issue e também os labels Aero, Prop, Rec, SE, Safety e Marketing que indicam quais áreas estão mais relacionadas ao issue. Mas nada disso é um impedimento. Se você é da Rec e quer resolver um problema relacionado a Prop, é ótimo!

Leia todos os issues e utilize o filtro de labels para te ajudar a escolher seu primeiro desafio. Sinta-se a vontade para mandar mensagens nos issues tirando dúvidas ou pedindo mais detalhes antes ou até depois de se decidir. 

Quando estiver decidido, se dirija à barra lateral direita do issue e em **Assignees**, clique na opção **assign yourself** para registrar você como responsável por resolver um issue. E se já tiver outro responsável? Não tem problema, mais de uma pessoa pode resolver o mesmo desafio! Lembre-se que você pode resolver quantos issues quiser durante essa Hackathon! E se precisar de ajuda, use a abuse dos comentários no issue para nossos organizadores de ajudarem.

![GIF - Escolhendo um issue](https://github.com/Projeto-Jupiter/Hackathon/raw/master/images/escolhendo_um_issue.gif)


## Criando um branch

Agora que já sabe qual desafio vai resolver primeiro, é hora de começar a resolve-lo. Para isso, vamos organizar nosso ambiente de trabalho.

Todas as contribuições que você fizer, será em um branch.
 - O que é uma **contribuição**? É qualquer adição, remoção ou edição de arquivo aqui no nosso repositório do Hackathon.
 - O que é um **branch**? O desenvolvimento de um projeto, como o nosso, é exatamente igual uma linha do tempo. E quando várias pessoas começam a contribuir em paralelo, então essa linha do tempo se ramifica em vários **branches**. Lá na frente, quando a sua ramificação já estiver pronta para voltar a linha do tempo principal, chamada de **master**, juntamos o seu **branch** ao **master** em uma operação conhecida como **merge**. Mais detalhes no [GitHub Guides](https://guides.github.com/introduction/flow/)

 Agora que já sabe o que é um branch, vamos criar um. Na página inicial desse repositório, clique na setinha ao lado de **master**, como mostra o GIF abaixo. Insira o nome do seu branch no campo indicado e pressione *Enter*! Pronto, seu branch está criado. Procure criar um branch com um nome representativo, como por exempo `equipeA_issue21`.  Mas não siga necessariamente esse padrão, está livre para ser criativo!

![GIF - Criando um branch](https://github.com/Projeto-Jupiter/Hackathon/raw/master/images/criando_um_branch.gif)

 No seu novo branch, verá uma cópia de todos os arquivos da linha de tempo original, o **master**. Agora, está livre para adicionar, remover e editar os arquivos como quiser, sem medo!

## Fazendo seu primeiro commit

Commit? Isso mesmo, fazer/dar um commit é simplesmente a ação de editar, de alguma forma, os arquivos do seu branch. Seja editando um ou mais arquivos, adicionando novos ou ainda removendo arquivos velhos. Mais detalhes no [GitHub Guides](https://guides.github.com/introduction/flow/)

Para fazer um commit pelo GitHub mesmo, você deve primeiro garantir que está no seu branch. Isto é, verifique que não está no master, mas sim no branch que você criou.

Então, tem algumas opções:

- Adicionar um arquivo: clique no botão `Add file`, como ilustra o desenho a seguir. Terá duas opções, ou adicionar um arquivo fazendo upload, ou criando um arquivo de texto no próprio GitHub.

- Editar ou remover um arquivo: clique em um arquivo dentro do seu branch, que você gostaria de editar ou remover. Ao abrir o arquivo, você terá a opção de editá-lo ou removê-lo clicando nos botões mostrados no GIF a seguir.

Para esse exemplo, seu primeiro commit, optaremos por editar o `Participantes.md`. Clique nele para abrí-lo. Então, clique no ícone do lápis para editá-lo. Nesse caso, vamos modificar o arquivo adicionando o nome do grupo e cada participante. Então, role a página para baixo, onde encontrára a opção para **Commit Changes**, que nada mais é do que salvar suas alterações no seu branch.

Cada commit exige uma descrição simples, de no máximo 50 caractéres e sem pontuação no final. Mas caso tenha o desejo de descrever melhor o que fez, pode adicionar uma descrição extendida também.

Por fim, verifique que está realizando o commit no branch correto e aperte o botão `Commit changes`! Pronto, seu primeiro commit está feito e as alterações do arquivo `Participantes.md` estão salvas.

![GIF - Fazendo seu primeiro commit](https://github.com/Projeto-Jupiter/Hackathon/raw/master/images/fazendo_seu_primeiro_commit.gif)


## Fazendo um pull request

Com o commit realizado, nosso branch, ou ramificação da linha de desenvolvimento, está diferente da linha principal, a master. Se julgarmos que já está na hora de migrar nossas alterações para a master, devemos realizar um **pull request**. Mais detalhes no [GitHub Guides](https://guides.github.com/introduction/flow/)

Um **pull request** é um pedido para adicionar as alterações feitas no nosso branch ao master. Assim, trata-se de uma operação feita para um branch inteiro, não apenas para um único commit (a não ser que tenhamos apenas um commit no nosso branch, como é o caso agora).

Para criar um pull request, volte a página principal do seu branch e clique em `Compare & pull request`. Ao clicar, uma nova página será aberta, onde você pode dar um nome à sua solicitação e descrevé-la com mais detalhes. Além disso, rolando a página para baixo, poderá ver as modificações feitas nos arquivos, em comparação com àqueles que estão no master.

Após adicionar a descrição, é preciso adicionar os **revisores** do pull request. Os **revisores** são responsáveis por revisarem as edições e aprovarem ou não a junção do seu branch com o master. No caso da Hackathon, os revisore são os organizadores! Então, pode adicionar qualquer um deles ou mesmo o time de revisores.

Por fim, basta clicar em `Create pull request` e esperar a revisão da organização! Quando sua revisão for aprovada, ganhará os pontos do desafio e suas edições poderam ir para o master!

Mas lembre-se que é possível que os organizadores exijam alguma mudança no seu código, então fique atento se for avisado por algum deles!

![GIF - Fazendo um pull request](https://github.com/Projeto-Jupiter/Hackathon/raw/master/images/fazendo_um_pull_request.gif)

## Resumo

É isso, com seu pull request aprovado, você acaba de contribuir para o nosso Projeto Jupiter e conquistar pontos na Hackathon!

Vamos relembrar os passos:

1. Criar um branch novo.
2. Editar arquivos e dar commit.
3. Fazer um pull request para juntar suas edições ao master.
4. Aguardar a aprovação dos revisores.
5. Ganhar pontos!

# COMUNICAÇÃO

Temos alguns canais de comunicação principais! Durante a Hackathon, usaremos o Discord e o GitHub também. Mais detalhes a seguir.

## Discord

Todos deveriam estar no server da Hackathon já. Ainda não está? Sem problemas, entre em contato com alguém da organização por WhatsApp mesmo que vamos te ajudar!

No discord, temos o canal de avisos e o de discussão, que todos podem ver. Além disso, há um para cada grupo, porém são privados e apenas os membros do respectivo grupo e os organizadores podem se comunicar por lá. Ótimo para aquelas dúvidas que você julga não ser relevante para os outros participantes. Mas sinta-se a vontade de usar o canal que quiser.

## GitHub

Aqui pelo GitHub vamos nos comunicar por meio dos comentários nos **issues** e **pull requests**.

Qualquer dúvida sobre código, como implementar, por onde começar, enfim, qualquer coisa relacionada ao desafio que escolheu, pode mandar como comentário no respectivo issue que vamos te ajudar!

Todos os participantes podem ver seus comentários... quem sabe um participante não acaba ajudando o outro também?


# CRONOGRAMA

## Sexta
21:00 - Abertura

21:00 - Início dos dommits

## Sábado
21:00 - Apresentações parciais

## Domingo
20:00 - Encerramento dos commits

20:00 - Apresentações finais

22:00 - Encerramento e premiação

# REGRAS!

## Paz e Amor

Estamos em família! Que essa seja uma competição saúdavel. Mals comportamentos não serão tolerados, mas isso não é problema, sei que entre nós há apenas paz e amor.

## Novos Desafios

Teve outra ideia que ainda não está na lista de desafios/issues? Ou foi resolver um issue e acabou fazendo muito mais coisa? Sem problemas, avise os organizadores! Estamos dispostos a adicionar novos desafios a qualquer momento.

Sempre que um novo desafio for criado, todos os participantes serão avisados.

## Pontuação

Os desafios, ou issues, são dividos em 3 níveis de dificuldade:

- Easy: 5 pontos
- Medium: 20 pontos
- Hard: 50 pontos

O nível de dificuldade de um determinado desafio pode ser encontrado como um dos labels do desafio e também na lista de todos os desafios divulgados. A organização pode alterar a dificuldade de um desafio a qualquer momento, mas apenas para um nível mais difícil.

## Bônus

Os organizadores podem prestigiar equipes pelos seus trabalhos com resultados além do esperado com uma pontuação de bônus, limitada entre 1 a 5 pontos para cada desafio.

Para o bônus, os organizadores levaram em conta soluções que:

- Vão além do esperado;
- Possuem um padrão de código bem documentado e bem escrito;
- São muito criativas!

## Premiação

Cada grupo receberá uma quantia de R$ 15,00 a cada 10 pontos conquistados! Por exemplo, se conquistarem 25 pontos, os participantes ganharão R$ 30,00 em conjunto. É simbólico, mas dá para conquistar muito mais! O prêmio máximo por equipe é limitado a R$ 150,00. 

*Obs: a qualquer momento os organizadores podem optar por aumentarem o prêmio monetário, mas não podem diminuí-lo.

Além disso, os três grupos com melhor pontuação receberam, além de prestígio, prêmios simbôlicos anunciados ao fim da competição.

E o melhor prêmio será conquistado se todas as equipes juntas atingirem um total de 300 pontos, ou seja, um quinto de todos os desafios propostos. Convidaremos veteranos e fundadores do Jupiter para contar histórias da equipe e como a participação no Jupiter é um diferencial na vida de cada um!



