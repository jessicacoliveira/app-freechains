import subprocess
import json

# Gera um par de chaves pública e privada a partir de uma palavra-chave
def criarPubpvt(keyword):
    resultado = subprocess.run(["./freechains", "keys", "pubpvt", keyword], stdout=subprocess.PIPE, text=True)
    saidas = resultado.stdout.strip().split()
    chave_pub = saidas[0]
    chave_pvt = saidas[1]
    return chave_pub, chave_pvt

# Entra em um canal especificado com a chave do pioneiro (só aceita 1 pioneiro)
def joinCanal(key, canal):
    subprocess.run(["./freechains", "chains", "join", canal, key], stdout=subprocess.PIPE, text=True)

# Sai de um canal
def leaveCanal(canal):
    subprocess.run(["./freechains", "chains", "leave", canal], stdout=subprocess.PIPE, text=True)

# Posta mensagem no canal especificado, assinando com a chave privada
def post(texto,chave,canal): 
    resultado = subprocess.run (["./freechains", "chain", canal, "post", "inline", texto, f"--sign={chave}"], stdout=subprocess.PIPE, text=True)
    return resultado.stdout.strip()  # retorna o hash do post

# Dá like em um post, assinando com a chave privada
def like(canal, hash_post, chave):
    subprocess.run(["./freechains", "chain", canal, "like", hash_post, f"--sign={chave}"], stdout=subprocess.PIPE, text=True)

# Dá dislike em um post, assinando com a chave privada
def dislike(canal, hash_post, chave):
    subprocess.run(["./freechains", "chain", canal, "dislike", hash_post, f"--sign={chave}"], stdout=subprocess.PIPE, text=True)

# Recupera o conteúdo (payload) de um post a partir do seu hash
def getPayload(hash_post, canal):   
    resultado = subprocess.run (["./freechains", "chain", canal, "get", "payload", hash_post], stdout=subprocess.PIPE, text=True)
    payload = resultado.stdout.strip()

    if payload == "": #tirar isso depois
        return ""  # (like ou dislike)
    else:
        return f"{payload}"  # publicacao

# Obtém a reputação de um usuário 
def getUserRep(canal, chave):
    resultado = subprocess.run (["./freechains", "chain", canal, "reps", chave], stdout=subprocess.PIPE, text=True)
    return resultado.stdout.strip()

# Obtém a reputação de um post 
def getPostRep(canal, hash_post):
    resultado = subprocess.run (["./freechains", "chain", canal, "reps", hash_post], stdout=subprocess.PIPE, text=True)
    return resultado.stdout.strip()

def getConsensus(canal):
    resultado = subprocess.run(["./freechains", "chain", canal, "consensus"], stdout=subprocess.PIPE, text=True)
    saidas = resultado.stdout.strip().split()
    return saidas

# Lista as mensagens dos hashes fornecidos, ignorando likes/dislikes
def listarConversa(canal, lista_hash):
    for hash_post in lista_hash:
        msg=getPayload(hash_post, canal)
        if msg != "":
            print(msg)

#retorna lista de heads
def getHeads(canal):
    resultado = subprocess.run(["./freechains", "chain", canal, "heads"], stdout=subprocess.PIPE, text=True)
    saidas = resultado.stdout.strip().split()
    return saidas

# Retorna o hash do bloco gênesis da cadeia
def getGenesis(canal):
    resultado = subprocess.run(["./freechains", "chain", canal, "genesis"], stdout=subprocess.PIPE, text=True)
    return resultado.stdout.strip()

# Busca posts que contenham a keyword, até um limite de iterações
def buscaTermo(canal, keyword, limite):
    heads = getHeads(canal)
    genesis = getGenesis(canal)
    
    resultados = []
    contador = 0

    # Verifica nos blocos heads
    for head_hash in heads:
        if contador >= limite:
            break
        payload = getPayload(head_hash, canal)
        if payload != "" and keyword in payload:
            resultados.append(head_hash)
        contador += 1

    # Percorre a cadeia para trás
    atual = heads[0]
    while contador < limite and atual != genesis:
        backs = getBacks(canal, atual)
        anterior = backs[0]
        payload = getPayload(anterior, canal)
        if payload != "" and keyword in payload:
            resultados.append(anterior)
        contador += 1
        atual = anterior
        
    return resultados

# Retorna o bloco completo de um post em formato JSON
def getBloco(canal, hash_post):
    resultado = subprocess.run(["./freechains", "chain", canal, "get", "block", hash_post], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    saida = resultado.stdout.strip()
    
    return json.loads(saida)

# Retorna hash do bloco anterior
def getBacks(canal, hash_post):
    bloco = getBloco(canal, hash_post)
    
    return bloco.get("backs", "")

# Retorna o hash do post que recebeu um like/dislike
def getHashLike(canal, hash_post):
    bloco = getBloco(canal, hash_post)
    
    like_info = bloco.get("like", {})
    return like_info.get("hash", None)

# Retorna a chave pública de quem deu o like/dislike no post
def getUserLike(canal, hash_post):
    bloco = bloco = getBloco(canal, hash_post)
    
    like_info = bloco.get("sign", {})
    return like_info.get("pub", None)

# Verifica se um bloco é de like (1) ou dislike (-1)
def isLikeOrDislike(canal, hash_post):
    bloco = getBloco(canal, hash_post)

    like_info = bloco.get("like", {})
    return like_info.get("n", None) # n eh 1 para like, -1 para dislike e null para post

# Calcula o score de um post com base na reputação de quem deu like/dislike
def calculaScore(canal, hash_post):
    heads = getHeads(canal)
    parada = hash_post
    
    score = 0
    # Verifica nos blocos heads
    for head_hash in heads:
        payload = getPayload(head_hash, canal)
        if payload == "":
            hash_like = getHashLike(canal, head_hash)
            if hash_post == hash_like:
                user = getUserLike(canal, head_hash)
                tipo = isLikeOrDislike(canal, head_hash)
                rep = getUserRep(canal,user)
                if tipo == 1:
                    score+=rep
                elif tipo == -1:
                    score-=rep
    
    # Percorre a cadeia para trás
    atual = heads[0]
    while atual != parada:
        backs = getBacks(canal, atual)
        anterior = backs[0]
        payload = getPayload(anterior, canal)
        if payload == "":
            hash_like = getHashLike(canal, anterior)
            if hash_post == hash_like:
                user = getUserLike(canal, anterior)
                tipo = isLikeOrDislike(canal, anterior)
                rep = getUserRep(canal,user)
                if tipo == 1:
                    score +=rep
                elif tipo == -1:
                    score -=rep
        atual = anterior
    
    return score

# Conta quantos usuários com reputação maior ou igual ao valor especificado deram like no post
def getHowManyUsersRepLimit (canal, hash_post, limite_rep):
    heads = getHeads(canal)
    parada = hash_post
    
    soma_users = 0
    # Verifica nos blocos heads
    for head_hash in heads:
        payload = getPayload(head_hash, canal)
        if payload == "":
            hash_like = getHashLike(canal, head_hash)
            if hash_post == hash_like:
                user = getUserLike(canal, head_hash)
                tipo = isLikeOrDislike(canal, head_hash)
                rep = getUserRep(canal,user)
                if tipo == 1 and rep >= limite_rep:
                    soma_users += 1
    
    # Percorre a cadeia para trás
    atual = heads[0]
    while atual != parada:
        backs = getBacks(canal, atual)
        anterior = backs[0]
        payload = getPayload(anterior, canal)
        if payload == "":
            hash_like = getHashLike(canal, anterior)
            if hash_post == hash_like:
                user = getUserLike(canal, anterior)
                tipo = isLikeOrDislike(canal, anterior)
                rep = getUserRep(canal,user)
                if tipo == 1 and rep >= limite_rep:
                    soma_users += 1
        atual = anterior
    
    return soma_users

# Retorna um lista com os hashes dos posts recentes 
def pickRecentPosts(canal, limite):
    heads = getHeads(canal)
    genesis = getGenesis(canal)
    
    lista = []
    contador = 0

    # Verifica nos blocos heads
    for head_hash in heads:
        if contador >= limite:
            break
        payload = getPayload(head_hash, canal)
        if payload != "":
            lista.append(head_hash)
        contador += 1

    # Percorre a cadeia para trás
    atual = heads[0]
    while contador < limite and atual != genesis:
        backs = getBacks(canal, atual)
        anterior = backs[0]
        payload = getPayload(anterior, canal)
        if payload != "":
            lista.append(anterior)
        contador += 1
        atual = anterior
        
    return lista

# Mostra os posts ordenados pela reputação do autor (em ordem decrescente)
def showPostsRepAuthorOrder(canal, lista_hash):
    lista_reps = []
    for hash_post in lista_hash:
        autor = getUserLike(canal, hash_post)
        rep = getUserRep(canal, autor)
        rep = float(rep)
        lista_reps.append((hash_post, rep))

    lista_reps.sort(key=lambda x: x[1], reverse=True)

    for hash_post, rep in lista_reps:
        payload = getPayload(hash_post, canal)
        if payload != "":
            print(payload)

# Mostra os posts ordenados pela reputação do próprio post
def showPostsRepPostOrder(canal, lista_hash):
    lista_reps = []
    for hash_post in lista_hash:
        rep = getPostRep(canal, hash_post)
        rep = float(rep)
        lista_reps.append((hash_post, rep))

    lista_reps.sort(key=lambda x: x[1], reverse=True)

    for hash_post, rep in lista_reps:
        payload = getPayload(hash_post, canal)
        if payload != "":
            print(payload)

# Mostra os posts recentes ordenados pelo score calculado
def showPostsScoreOrder(canal, limite):
    lista_recentes = pickRecentPosts(canal, limite)
    lista_score = []
    
    for hash_post in lista_recentes:
        score = calculaScore(canal, hash_post)
        score = float(score)
        lista_score.append((hash_post, score))

    lista_score.sort(key=lambda x: x[1], reverse=True)

    for hash_post, score in lista_score:
        payload = getPayload(hash_post, canal)
        if payload != "":
            print(payload)

# Mostra os posts recentes na ordem em que foram encontrados
def showRecentPostsFirst(canal, limite):
    lista_recentes = pickRecentPosts(canal, limite)
    listarConversa(canal, lista_recentes)
