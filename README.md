# Caderno Online de Reclamações

O objetivo da aplicação é permitir que os membros da comunidade universitária (alunos, professores, técnicos) relatem problemas de forma pública e descentralizada, com moderação das denúncias por meio do sistema de reputação do Freechains.

## Como utilizar

*EM CONSTRUÇÃO*

## Funcionalidades
### Implementadas
1) `Criar chaves pubpvt:` gera um par de chaves pública e privada baseado em uma palavra-chave digitada pelo usuário;
2) `Postar reclamação:` permite postar uma reclamação no canal, caso tenha reputação suficiente;
4) `Like/dislike:` o usuário escolhe um post e dá um like ou dislike com sua chave privada;
5) `Join/leave em canal:` permite que o usuário entre (join) ou saia (leave) de um canal usando a chave privada;
6) `Consultar reputação:` o usuário pode consultar a reputação de um usuário (por chave pública) ou de um post (por hash);
7) `Busca por palavra-chave:` pesquisa as últimas n postagens que contêm uma palavra-chave informada;
8) `Listar mensagens:` lista os posts do canal na ordem de consenso (ordem cronológica aprovada pela rede);
9) `Listar mensagens por reputação dos autores (decrescente):` ordena os posts conforme a reputação dos autores (usuários que postaram)
10) `Listar mensagens por reputação dos posts (decrescente):` ordena os posts com base na reputação que o post recebeu (por likes/dislikes).
11) `Listar mensagens por reputação acumulada:` calcula um *score* para cada post somando a reputação dos usuários que deram like e subtraindo dos que deram dislike;
12) `Listar mensagens por entrada na cadeia:` mostra as postagens mais recentes até um limite de n posts.

### Falta Implementar
12) `Listar reclamações em destaque:` filtro incentiva os usuários a acumular reputação para ganhar influência na comunidade, mas dá chance de usuários novos ganharem destaque se a reclamação for relevante o suficiente;
13) `Sincronização:` funcionalidade básica.

### Fora de escopo
14) `Uso de tags:` possível pois busca já está funcional;
15) `Dashboard local`;
16) `Sistema de login`;
17) `Interface gráfica`.

## Ferramentas utilizadas
- Sistema operacional Linux.
- Freechains v.0.10.1
- Python3.
