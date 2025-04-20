Esse é um Sistema de Aluguel de Bicicletas - Projeto Acadêmico

Integrantes: Cesar Medina, Felipe Brum, Luisa Figueiredo e Ricardo Macedo

Este projeto foi desenvolvido como parte de uma atividade acadêmica para simular um sistema de aluguel de bicicletas. O sistema permite que usuários realizem o cadastro, login, aluguel e devolução de bicicletas.

**Atenção:** Este é um projeto educacional. Não digite dados reais de cartão de crédito. Nenhuma informação sensível é armazenada ou transmitida.

---

Tecnologias Utilizadas

- Python
- Django
- HTML5 & CSS3
- JavaScript (validações nos formulários)
- SQLite (banco de dados padrão do Django)

---

Funcionalidades

- Cadastro e login de usuários (com CPF e senha)
- Aluguel e devolução de bicicletas
- Validações automáticas nos formulários (CPF, telefone, cartão, etc.)
- Sistema de administrador Django para visualização de dados
- Página de alteração cadastral
- Interface simples e responsiva

---

Como rodar o projeto localmente:

1. Clone o repositório:
   ```bash
   git clone https://github.com/fbrum44/projeto-django-bikes.git

2.Crie e ative um ambiente virtual:

  python -m venv venv
  venv\Scripts\activate   # No Windows

3. Instale as dependências:

  pip install -r requirements.txt

4. Rode as migrações:
   
  python manage.py migrate

5. Inicie o servidor local:
 
  python manage.py runserver

6. Acesse:

     Acesso o link gerado.

---

Prints das telas do Projeto:

1. Tela Inicial:
   ![image](https://github.com/user-attachments/assets/7e60d051-f1d1-4208-90a6-3426c15a6b45)

2. Tela de Cadastro:
  ![image](https://github.com/user-attachments/assets/9dff6a17-5b21-442d-934a-3c262af9b74b)

3. Tela do Perfil do Usuário:
  ![image](https://github.com/user-attachments/assets/30af31a7-1126-492d-9cd4-eca090d249ab)

4. Tela das opções de Aluguel:
   ![image](https://github.com/user-attachments/assets/6cb676da-66e0-4bac-8952-db9715997457)

---

Este projeto não possui licença comercial e é distribuído apenas para fins educacionais.

