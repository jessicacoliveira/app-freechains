# Fórum Público Genérico com Freechains

Estudo de implementação de funcionalidades esperadas em um fórum público utilizando o Freechains. Esboço pode ser utilizado como base para aplicações ou protótipos mais complexos com o protocolo.

## Funcionalidades
### Implementadas
1) `Criar chaves pubpvt:` gera um par de chaves pública e privada baseado em uma palavra-chave digitada pelo usuário;
2) `Postar:` permite postar no canal, caso tenha reputação suficiente;
4) `Like/dislike:` o usuário escolhe um post e dá um like ou dislike com sua chave privada;
5) `Join/leave em canal:` permite que o usuário entre (join) ou saia (leave) de um canal;
6) `Consultar reputação:` o usuário pode consultar a reputação de um usuário (por chave pública) ou de um post (por hash);
7) `Busca por palavra-chave:` pesquisa as últimas n postagens que contêm uma palavra-chave informada;
8) `Listar mensagens:` lista os posts do canal na ordem de consenso (ordem cronológica aprovada pela rede);
9) `Listar mensagens por reputação dos autores (decrescente):` ordena os posts conforme a reputação dos autores (usuários que postaram)
10) `Listar mensagens por reputação dos posts (decrescente):` ordena os posts com base na reputação que o post recebeu (por likes/dislikes).
11) `Listar mensagens por Score:` calcula uma **pontuação** para cada post somando a reputação dos usuários que deram like e subtraindo dos que deram dislike;
12) `Listar mensagens por entrada na cadeia:` mostra as publicações mais recentes até um limite de n posts.

### Falta Implementar
12) `Listar posts em destaque`;
13) `Sincronização`.

### Fora de escopo
14) `Sistema de login`;
15) `Interface gráfica`.

## Ferramentas utilizadas
- Sistema operacional Linux.
- Freechains v.0.10.1
- Python3.
