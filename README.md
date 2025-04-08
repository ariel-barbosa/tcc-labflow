# Sistema de Controle de Laboratórios

## Introdução

O **Sistema de Controle de Laboratórios** é um projeto desenvolvido para solucionar problemas comuns em escolas e instituições de ensino relacionados à gestão e uso de laboratórios. Muitas vezes, a falta de controle adequado gera conflitos de horário e ocupação indevida dos ambientes de estudo. Este sistema visa otimizar a reserva e utilização desses espaços, proporcionando uma melhor experiência para alunos e professores.

O projeto foi concebido com base em pesquisas de campo realizadas na Escola Senai de Itumbiara - GO, mas pode ser adaptado para outras instituições e diferentes tipos de ambientes de estudo e pesquisa, como salas de reuniões, bibliotecas e salas de vídeo.

## Funcionalidades Principais
- **Reserva de Laboratórios**: Permite que professores e funcionários reservem laboratórios online.
- **Consulta de Disponibilidade**: Exibe a disponibilidade dos laboratórios em um calendário interativo.
- **Gestão Administrativa**: Administradores podem gerenciar horários e disponibilidade dos laboratórios.
- **Notificações**: Envio de e-mails ou SMS para confirmação e lembrete de reservas.
- **Geração de Relatórios**: Relatórios detalhados sobre o uso dos laboratórios.
- **Histórico de Reservas**: Consulta de reservas anteriores.
- **Integração com Autenticação da Escola**: Permite login seguro para usuários autorizados.

## Tecnologias Utilizadas
- **Linguagem de Programação**: Python
- **Framework Web**: Django
- **Banco de Dados**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Autenticação**: Django Authentication

## Requisitos do Sistema
### Requisitos Funcionais
| ID  | Descrição | Prioridade |
| --- | --------- | ---------- |
| RF01 | Permitir que os usuários reservem laboratórios online. | Alta |
| RF02 | Exibir a disponibilidade dos laboratórios em um calendário. | Alta |
| RF03 | Permitir a reserva por data, hora e tipo de laboratório. | Alta |
| RF04 | Enviar notificações de confirmação por e-mail/SMS. | Média |
| RF05 | Permitir que administradores gerenciem os horários. | Alta |
| RF06 | Gerar relatórios de uso dos laboratórios. | Média |
| RF07 | Permitir cancelamento de reservas. | Média |
| RF08 | Exibir histórico de reservas. | Baixa |
| RF09 | Permitir reserva de equipamentos específicos. | Média |
| RF10 | Integrar o sistema com a autenticação da escola. | Alta |

### Requisitos Não Funcionais
| ID  | Descrição | Prioridade |
| --- | --------- | ---------- |
| RNF01 | Responsivo e acessível em diferentes dispositivos. | Alta |
| RNF02 | Interface intuitiva e fácil de usar. | Alta |
| RNF03 | Proteção dos dados dos usuários. | Alta |
| RNF04 | Tempo de resposta rápido. | Média |
| RNF05 | Escalável para grande número de usuários. | Média |
| RNF06 | Compatível com principais navegadores. | Alta |
| RNF07 | Design moderno e atraente. | Baixa |
| RNF08 | Fácil manutenção e atualização. | Média |
| RNF09 | Disponibilidade 24/7. | Alta |
| RNF10 | Manual do usuário e suporte técnico. | Média |

## Como Instalar e Executar o Projeto
1. Clone o repositório:
   ```sh
   git clone https://github.com/seuusuario/sistema-controle-laboratorios.git
   ```
2. Acesse o diretório do projeto:
   ```sh
   cd sistema-controle-laboratorios
   ```
3. Crie um ambiente virtual e ative-o:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
4. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
5. Execute as migrações do banco de dados:
   ```sh
   python manage.py migrate
   ```
6. Inicie o servidor:
   ```sh
   python manage.py runserver
   ```
7. Acesse no navegador:
   ```
   http://127.0.0.1:8000/
   ```

## Contribuição
Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do repositório
2. Crie um branch para sua funcionalidade (`git checkout -b feature-nova`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova funcionalidade'`)
4. Envie para o repositório remoto (`git push origin feature-nova`)
5. Abra um Pull Request

## Licença
Este projeto é licenciado sob a [MIT License](LICENSE).

## Contato
Caso tenha dúvidas ou sugestões, entre em contato pelo e-mail: **arielbarbosasantos1@gmail.com**.
Muito Obrigado!
