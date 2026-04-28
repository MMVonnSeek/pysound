# 🎵 PySound - API inspirado no Spotify
![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![Flask Version](https://img.shields.io/badge/flask-3.0.0-green.svg)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange.svg)
![SQLite](https://img.shields.io/badge/database-SQLite-blue.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)
> Uma API REST completa para gerenciamento de músicas e playlists, desenvolvida com Flask e autenticação JWT.

##  Sobre o Projeto
PySound é uma API backend desenvolvida durante as aulas de back-end no SENAI Taguatinga. O projeto simula um serviço de streaming de música (como Spotify), permitindo:
- ✅ Autenticação segura com JWT
- ✅ CRUD completo de músicas
- ✅ Criação e gerenciamento de playlists
- ✅ Relacionamento muitos-para-muitos entre músicas e playlists
- ✅ Interface visual para testes (sem precisar de Postman)
- ✅ Banco de dados SQLite com SQLAlchemy ORM


### Objetivo Educacional
Este projeto foi criado para demonstrar na prática:
- Como estruturar uma API REST profissional
- Implementação de autenticação stateless com JWT
- Uso de ORM para manipulação de banco de dados
- Boas práticas de segurança (hash de senhas, permissões)
- Organização de código com Blueprints


## Demonstração

<div align="center">
 <img src="screenshots/dashboard.png" alt="Dashboard do PySound" width="800">
 <p><em>Dashboard principal com estatísticas e últimas músicas</em></p>
</div>
<div align="center">
 <img src="screenshots/login.png" alt="Tela de Login" width="400">
 <img src="screenshots/songs-list.png" alt="Lista de Músicas" width="400">
 <p><em>Autenticação e gerenciamento de músicas</em></p>
</div>


##  Tecnologias Utilizadas
| Tecnologia | Versão | Finalidade |
|------------|--------|-------------|
| **Python** | 3.10+ | Linguagem principal |
| **Flask** | 3.0.0 | Framework web |
| **Flask-SQLAlchemy** | 3.1.1 | ORM para banco de dados |
| **Flask-JWT-Extended** | 4.6.0 | Autenticação com tokens JWT |
| **Flask-CORS** | 4.0.0 | Compartilhamento de recursos entre origens |
| **Werkzeug** | 3.0.1 | Hash de senhas e utilitários |
| **SQLite** | - | Banco de dados leve |


## Estrutura do Projeto
```
pysound/  
   ├── app.py               # Configuração principal da aplicação  
   ├── models.py            # Modelos do banco de dados (ORM)  
   ├── requirements.txt     # Dependências do projeto  
   ├── routes/  
   │       ├── auth.py      # Rotas de autenticação  
   │       ├── songs.py     # Rotas de músicas (CRUD)  
   │       └── playlists.py # Rotas de playlists  
   ├── templates/  
   │        └── index.html  # Interface visual de testes  
   └── screenshots/         # Imagens da documentação  
```

---
##  Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior
- Git (opcional, para clonar o repositório)

### Passo a Passo
1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/pysound.git
cd pysound
```

2.  **Crie um ambiente virtual**
```
# Windows
python -m venv venv
venv\Scripts\activate


# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3.  **Instale as dependências**
```
pip install -r requirements.txt
```

4.  **Execute a aplicação**
```
python app.py
```

6.  **Acesse no navegador**

-   Interface visual: [http://localhost:5000](http://localhost:5000)
    
-   API: [http://localhost:5000/songs](http://localhost:5000/songs)
    

## Endpoints da API

### Autenticação

| Método | Endpoint | Descrição | Auth |
| ------ | -------- | --------- | ---- |
| POST | `/auth/register` | Criar nova conta | ❌ |
| POST | `/auth/login` | Login e obtenção do token | ❌ |

### Músicas

| Método | Endpoint | Descrição | Auth |
| ------ | -------- | --------- | ---- |
| GET | `/songs` | Listar todas as músicas (com filtros) | ❌ |
| GET | `/songs/{id}` | Buscar música específica | ❌ |
| POST | `/songs` | Adicionar nova música | ✅ |
| DELETE | `/songs/{id}` | Remover música (sendo o dono) | ✅ |

### Playlists

| Método | Endpoint | Descrição | Auth |
| -- | --- | ---- | --- |
| GET | `/playlists` | Listar todas as playlists | ❌ |
| POST | `/playlists` | Criar nova playlist | ✅ |
| POST | `/playlists/{id}/songs` | Adicionar música à playlist | ✅ |

### Filtros Disponíveis

Para a rota `/songs`, você pode usar query parameters:

-   `?q=termo` - Busca geral (título, artista, álbum)
    
-   `?genre=rock` - Filtrar por gênero
    
-   `?artist=Queen` - Filtrar por artista
    

Exemplo: `http://localhost:5000/songs?q=Bohemian&genre=Rock`

---
## Exemplos de Uso

### 1. Registrar um novo usuário

```
curl -X POST http://localhost:5000/auth/register \
 -H "Content-Type: application/json" \
 -d '{
 "username": "joaosilva",
 "email": "joao@email.com",
 "password": "123456"
 }'
```

### 2. Fazer login

```
curl -X POST http://localhost:5000/auth/login \
 -H "Content-Type: application/json" \
 -d '{
 "email": "joao@email.com",
 "password": "123456"
 }'
```

**Resposta esperada:**

```
{
 "message": "Login realizado!",
 "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
 "user": {
 "id": 1,
 "username": "joaosilva",
 "email": "joao@email.com"
 }
}
```
### 3. Adicionar uma música (requer token)

```

curl -X POST http://localhost:5000/songs \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer SEU_TOKEN_AQUI" \
 -d '{
 "title": "Yesterday",
 "artist": "The Beatles",
 "album": "Help!",
 "genre": "Rock",
 "duration": 125
 }'
```

### 4. Listar músicas com filtro

```

curl -X GET "http://localhost:5000/songs?genre=Rock&artist=Beatles"
```

### 5. Criar uma playlist

```

curl -X POST http://localhost:5000/playlists \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer SEU_TOKEN_AQUI" \
 -d '{
 "name": "Minhas Favoritas",
 "description": "Músicas que mais gosto"
 }'
``` 

## Interface Visual

O projeto inclui uma interface HTML completa para testar todos os endpoints:

-   **Dashboard**: Estatísticas em tempo real
    
-   **Autenticação**: Registro e login com armazenamento do token
    
-   **Músicas**: Busca, adição e remoção
    
-   **Playlists**: Criação e gerenciamento
    
-   **Documentação**: Tabela com todos os endpoints
    

A interface é auto-suficiente e não requer configuração adicional.

## Segurança

-   ✅ Senhas armazenadas com hash (bcrypt via Werkzeug)
    
-   ✅ Tokens JWT com assinatura digital
    
-   ✅ Verificação de permissão em rotas protegidas
    
-   ✅ Proteção contra SQL injection (via ORM)
    
-   ✅ Validação de dados de entrada
    

## Testando a API

### Opção 1: Interface Visual

Acesse `http://localhost:5000` e use a interface completa.

### Opção 2: Postman/Insomnia

Importe a collection (em breve disponível) ou faça requisições manuais.

### Opção 3: cURL (terminal)

Use os exemplos fornecidos acima.

---
## Banco de Dados

O projeto usa SQLite com o seguinte schema:

```

-- Tabela User
id (PK), username, email, password, created_at
-- Tabela Song
id (PK), title, artist, album, duration, genre, url, created_at, user_id (FK)
-- Tabela Playlist
id (PK), name, description, created_at, user_id (FK)
-- Tabela de associação (many-to-many)
playlist_songs: playlist_id (FK), song_id (FK)
```

### Diagrama de Relacionamento

```

User (1) ──────< (N) Song
  │
  └────────────< (N) Playlist
                  │
                  └──< (N:M) >── Song
```

## Problemas Comuns e Soluções

| Problema | Possível Causa | Solução |
| -------- | -------------- | ------- |
| `ModuleNotFoundError` | Ambiente virtual não ativado | Execute `venv\Scripts\activate` |
| Erro 401 ao acessar rota protegida | Token inválido ou expirado | Faça login novamente |
| Erro 403 ao deletar música | Usuário não é o dono | Apenas o criador pode deletar |
| Banco não cria as tabelas | `db.create_all()` não executado | Rode `python app.py` que executa automaticamente |
| Porta 5000 já em uso | Outra aplicação usando a porta | Mude a porta no `app.run(port=5001)` |
    

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](https://LICENSE) para mais detalhes.

## Créditos

Desenvolvido pela turma de **Técnico em Informática para Internet - TEC.043.004** do **SENAI Taguatinga-DF**.

**Instrutor:** Max Muller

**Disciplina:** Codificação para Back-End 

**Ano:** 2026
