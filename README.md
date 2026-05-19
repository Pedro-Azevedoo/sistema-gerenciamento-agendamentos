# Sistema de Gerenciamento de Agendamentos

Projeto Integrador – UNIVESP (Bacharelado em Tecnologia da Informação)

**Tecnologias:** Python · Flask · SQLite · Bootstrap 5

---

## Pré-requisitos

- Python 3.10 ou superior
- pip

---

## Como executar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Iniciar o servidor
python app.py
```

Acesse `http://127.0.0.1:5000` no navegador.

**Credenciais padrão:**
- Usuário: `admin`
- Senha: `admin123`

---

## Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Login | Tela de autenticação do sistema |
| Listar agendamentos | Visualização com filtros por data e nome |
| Criar agendamento | Cadastro com validação de conflito de horário |
| Editar agendamento | Atualização com revalidação de conflito |
| Excluir agendamento | Remoção com confirmação |

---

## Estrutura do projeto

```
trab-univesp-pi-1/
├── app.py              # Aplicação Flask (rotas)
├── database.py         # Conexão e criação do banco SQLite
├── agenda.db           # Banco de dados (gerado automaticamente)
├── requirements.txt    # Dependências Python
└── templates/
    ├── base.html            # Layout base (navbar, alertas)
    ├── login.html           # Tela de login
    ├── agendamentos.html    # Listagem com filtros
    └── form_agendamento.html # Formulário de criação/edição
```

---

## Equipe

- Lariza Maria Daré
- Mariana Ferreira de Oliveira
- Lindolfo M. E. M. Paulino da Silva
- Leandro Brosco Camanforte
- Pedro Azevedo

Tutor: Junio Gironi da Rocha
Polo: Pederneiras, Jaú, Macatuba e Reginópolis – 2026
