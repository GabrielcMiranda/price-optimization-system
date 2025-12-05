# 💰 Sistema de Otimização de Preços

Sistema web para otimização de preços utilizando cálculo diferencial. Calcula automaticamente o preço ótimo que maximiza o lucro com base em funções de custo e demanda fornecidas pelo usuário.

## 📋 Descrição

O **Sistema de Otimização de Preços** é uma aplicação completa voltada para empreendedores que desejam encontrar o preço ideal de seus produtos para gerar o maior lucro possível. O sistema permite:

- Cadastrar produtos com suas respectivas funções de custo e demanda
- Calcular automaticamente o preço ótimo que maximiza o lucro
- Visualizar graficamente a análise de custo, receita e lucro
- Gerenciar múltiplos produtos e suas otimizações
- Autenticação segura com JWT tokens

### Fundamento Matemático

O sistema utiliza cálculo diferencial para encontrar o ponto ótimo através da fórmula:

```
L(p) = p · Q(p) - C(Q(p))
```

Onde:
- **L(p)**: Função de lucro
- **p**: Preço (variável de decisão)
- **Q(p)**: Função de demanda (quantidade vendida em função do preço)
- **C(Q)**: Função de custo (custo total em função da quantidade)

O sistema resolve `dL/dp = 0` para encontrar pontos críticos, verifica a segunda derivada (`d²L/dp² < 0`) para confirmar máximos, e descarta automaticamente valores negativos ou complexos, garantindo soluções economicamente plausíveis.

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **FastAPI**: Framework web moderno e de alta performance
- **SQLAlchemy**: ORM para manipulação do banco de dados
- **PostgreSQL**: Banco de dados relacional
- **SymPy**: Biblioteca para cálculo simbólico e resolução de derivadas
- **Matplotlib**: Geração de gráficos
- **Cloudinary**: Armazenamento de imagens (gráficos)
- **JWT**: Autenticação e autorização

### Frontend
- **Angular 20.3.0**: Framework TypeScript
- **Tailwind CSS v3**: Framework CSS utilitário
- **RxJS**: Programação reativa

## 📦 Requisitos

### Backend
- Python 3.11 ou superior
- PostgreSQL 12 ou superior
- Conta Cloudinary (gratuita)

### Frontend
- Node.js 18 ou superior
- npm ou yarn

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/GabrielcMiranda/price-optimization-system.git
cd price-optimization-system
```

### 2. Configuração do Backend

#### 2.1. Criar ambiente virtual e instalar dependências

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

#### 2.2. Configurar variáveis de ambiente

Crie um arquivo `.env` na pasta `backend/` com:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/price_optimization
SECRET_KEY=sua_chave_secreta_jwt_aqui
CLOUDINARY_CLOUD_NAME=seu_cloud_name
CLOUDINARY_API_KEY=sua_api_key
CLOUDINARY_API_SECRET=seu_api_secret
```

#### 2.3. Criar banco de dados PostgreSQL

```bash
# Acesse o PostgreSQL
psql -U postgres

# Crie o banco
CREATE DATABASE price_optimization;
\q
```

#### 2.4. Inicializar o banco de dados

```bash
# Executar script de inicialização (cria as tabelas)
python -m app.core.database.init_db
```

#### 2.5. Executar o backend

```bash
python -m app.main
```

O backend estará rodando em `http://localhost:8000`

### 3. Configuração do Frontend

#### 3.1. Instalar dependências

```bash
cd frontend
npm install
```

#### 3.2. Executar o frontend

```bash
ng serve
```

O frontend estará rodando em `http://localhost:4200`

## 💡 Exemplos de Uso

### Exemplo 1: Produto Simples

**Dados:**
- **Nome do Produto**: Notebook Dell
- **Função de Custo C(q)**: `100 + 50*q`
  - Custo fixo de R$ 100
  - Custo variável de R$ 50 por unidade
- **Função de Demanda Q(p)**: `200 - 2*p`
  - Demanda máxima de 200 unidades
  - Elasticidade: -2 (cada R$ 1 no preço reduz 2 unidades vendidas)

**Resultado Esperado:**
- Preço Ótimo: ~R$ 62.50
- Lucro Máximo: ~R$ 1,875.00

### Exemplo 2: Produto Complexo

**Dados:**
- **Nome do Produto**: Exemplo Complexo
- **Função de Custo C(q)**: `50 + 3*q + 0.01*q**2`
  - Custo fixo de R$ 50
  - Custo variável crescente (economia de escala inversa)
- **Função de Demanda Q(p)**: `800 - 1.5*p`
  - Demanda máxima de 800 unidades
  - Elasticidade: -1.5

**Resultado Esperado:**
- Preço Ótimo: ~R$ 272.09
- Lucro Máximo: ~R$ 103,861.37

### Variáveis das Funções

- **Função de Custo**: Use `q` como variável (quantidade)
- **Função de Demanda**: Use `p` como variável (preço)

### Operadores Suportados

- Adição: `+`
- Subtração: `-`
- Multiplicação: `*`
- Divisão: `/`
- Potenciação: `**` (ex: `q**2` para q²)
- Parênteses: `(` `)`

## 📁 Estrutura do Projeto

```
price-optimization-system/
├── backend/
│   ├── app/
│   │   ├── core/             # Núcleo da aplicação
│   │   │   ├── database/     # Configuração e inicialização do banco
│   │   │   │   ├── connection.py    # Conexão com PostgreSQL
│   │   │   │   └── init_db.py       # Script de inicialização
│   │   │   ├── security.py   # Funções de segurança (JWT, hash)
│   │   │   └── settings.py   # Configurações da aplicação
│   │   ├── models.py         # Modelos do banco de dados (User, PriceOptimization)
│   │   ├── routers/          # Rotas da API
│   │   │   ├── auth_router.py         # Autenticação
│   │   │   └── optimization_router.py # Otimizações
│   │   ├── services/         # Lógica de negócio
│   │   │   ├── auth_service.py        # Serviço de autenticação
│   │   │   ├── optimization_service.py # Serviço de otimização
│   │   │   ├── optimization_calc.py    # Cálculos matemáticos
│   │   │   └── file_service.py        # Upload de imagens
│   │   ├── schemas.py        # Schemas Pydantic (validação)
│   │   └── main.py          # Aplicação principal FastAPI
│   └── requirements.txt      # Dependências Python
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/         # Serviços e modelos principais
│   │   │   │   ├── guards/   # Guards de autenticação
│   │   │   │   ├── interceptors/  # Interceptors HTTP
│   │   │   │   ├── models/   # Interfaces TypeScript
│   │   │   │   └── services/ # Serviços (API calls)
│   │   │   ├── features/     # Páginas da aplicação
│   │   │   │   ├── auth/     # Login e Registro
│   │   │   │   └── optimization/  # Página de otimização
│   │   │   └── shared/       # Componentes reutilizáveis
│   │   │       └── components/  # Button, Input, Card, etc.
│   │   ├── styles.scss       # Estilos globais
│   │   └── index.html
│   ├── angular.json
│   ├── package.json
│   ├── tailwind.config.js    # Configuração Tailwind CSS
│   └── tsconfig.json
└── README.md
```

## 🗄️ Estrutura do Banco de Dados

### Tabela: `users`
| Campo      | Tipo         | Descrição                    |
|------------|--------------|------------------------------|
| id         | UUID (PK)    | Identificador único          |
| username   | VARCHAR(50)  | Nome de usuário (único)      |
| email      | VARCHAR(100) | E-mail (único)               |
| password   | VARCHAR(255) | Senha hasheada (bcrypt)      |
| created_at | TIMESTAMP    | Data de criação              |

### Tabela: `price_optimizations`
| Campo              | Tipo         | Descrição                        |
|--------------------|--------------|----------------------------------|
| id                 | UUID (PK)    | Identificador único              |
| user_id            | UUID (FK)    | Referência ao usuário            |
| optimization_name  | VARCHAR(100) | Nome do produto                  |
| cost_function      | TEXT         | Função de custo C(q)             |
| demand_function    | TEXT         | Função de demanda Q(p)           |
| optimal_price      | FLOAT        | Preço ótimo calculado            |
| max_profit         | FLOAT        | Lucro máximo calculado           |
| graph_image_url    | TEXT         | URL da imagem do gráfico         |
| created_at         | TIMESTAMP    | Data de criação                  |
| updated_at         | TIMESTAMP    | Data de atualização              |

**Relacionamento**: Um usuário pode ter múltiplas otimizações (1:N)

## 🔐 Funcionalidades de Segurança

- **Autenticação JWT**: Tokens seguros para autenticação
- **Guards de Rota**: Proteção de rotas no frontend
- **Interceptors HTTP**: Injeção automática de tokens
- **Senhas Hasheadas**: Bcrypt para armazenamento seguro
- **CORS Configurado**: Apenas origem permitida (localhost:4200)
- **Validação de Entrada**: Pydantic no backend, Reactive Forms no frontend

## 🎨 Funcionalidades da Interface

- **Design Responsivo**: Funciona em desktop, tablet e mobile
- **Feedback Visual**: Mensagens de erro e sucesso claras
- **Loading States**: Indicadores visuais durante processamento
- **Validação em Tempo Real**: Feedback imediato nos formulários
- **Gráficos Interativos**: Visualização clara dos resultados

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Gabriel Miranda** - [GitHub](https://github.com/GabrielcMiranda)
- **Carlos Silva**
- **Yago Schnorr**

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📞 Suporte

Para suporte ou dúvidas, abra uma issue no repositório do GitHub.

---

Desenvolvido com ❤️ usando Python, FastAPI, Angular e muita matemática! 📊