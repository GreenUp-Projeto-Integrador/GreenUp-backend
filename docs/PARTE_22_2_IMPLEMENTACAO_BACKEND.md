# 22.2 Backend

No 6º período, foi implementado o núcleo inicial do backend do GreenUp utilizando Python, Django, Django REST Framework e PostgreSQL. A aplicação foi estruturada como uma API REST desacoplada do frontend React. Essa organização permite que a interface envie requisições HTTP ao servidor e receba respostas em JSON, sem acessar diretamente o banco de dados.

O código foi dividido por domínios de negócio. O app `accounts` concentra usuários, autenticação, dados pessoais, alteração de senha e suspensão de contas. O app `collection_points` mantém os pontos de coleta e as lixeiras associadas. O app `disposals` registra os descartes, categorias de resíduos, imagens comprobatórias e movimentações de pontuação. O app `notifications` registra os alertas direcionados aos gestores. Por fim, o app `analytics` consulta os dados persistidos para produzir os indicadores iniciais do dashboard.

Dentro desses módulos, as responsabilidades foram separadas em `models`, `serializers`, `services`, `views`, `urls` e `permissions`. Os models representam as entidades e os relacionamentos persistidos. Os serializers validam e transformam os dados recebidos ou enviados pela API. Os services concentram operações que envolvem regras de negócio. As views coordenam as requisições e respostas. Os arquivos de urls registram os endpoints, enquanto as permissions controlam o acesso de usuários, gestores e administradores.

O fluxo principal implementado foi o registro de descarte. Ao receber a requisição, a API verifica o token JWT e identifica o usuário autenticado. O serializer exige o código da lixeira, pelo menos uma categoria, a quantidade, a descrição dos itens, uma imagem e o nível de ocupação entre 1 e 4. Após a validação, a view chama o serviço de descarte. Esse serviço localiza e bloqueia a lixeira durante a operação, registra o descarte, associa suas categorias e imagens, calcula a pontuação e atualiza o nível de ocupação.

O registro utiliza `transaction.atomic()` porque altera várias entidades relacionadas. Dessa forma, descarte, categorias, imagens, pontuação, lixeira e eventual notificação são confirmados como uma única operação. Caso alguma etapa apresente erro, as alterações são revertidas, evitando dados incompletos ou inconsistentes.

A RNE-001 foi aplicada por meio da autenticação JWT e da permissão `IsAuthenticated`. Assim, requisições sem autenticação não conseguem registrar descartes. A RNE-002 foi implementada no serializer de entrada, que rejeita o registro quando um dos dados obrigatórios está ausente ou inválido. Também é verificado se o código informado corresponde a uma lixeira ativa.

A RNE-003 foi concentrada no serviço de descarte. Quando a ocupação passa de um nível igual ou inferior a 3 para o nível 4, o sistema altera o status da lixeira para coleta necessária e cria uma notificação para o gestor responsável pelo ponto de coleta. A transição de nível é verificada para evitar a criação repetida do mesmo alerta em registros consecutivos.

A RNE-004 foi implementada por meio de endpoints administrativos de suspensão e reativação. Somente usuários com papel de administrador podem executar essas operações. Ao ser suspensa, a conta recebe a data da suspensão e tem o campo `is_active` desativado, impedindo novas autenticações e o uso das funcionalidades protegidas. A senha é armazenada exclusivamente pelo mecanismo de hash do Django e nunca é retornada pela API.

A pontuação também foi centralizada no serviço. Nesta primeira versão, cada item registrado gera 10 pontos. A movimentação é armazenada em uma tabela própria e vinculada ao descarte que a originou. Essa decisão preserva a origem dos pontos e permite calcular o ranking com dados reais do banco, em vez de utilizar a lista fixa que existe atualmente no frontend.

O histórico pessoal consulta apenas os descartes associados ao usuário autenticado. A filtragem é feita no servidor, de modo que alterar um identificador na interface não permite consultar registros pertencentes a outra conta. A resposta foi organizada com os campos já esperados pelo frontend: identificador, data, tipo, quantidade, descrição dos itens, nível, código da lixeira e imagem.

O acesso aos dados é realizado pelo Django ORM. Foram utilizadas chaves estrangeiras para representar as associações entre usuários, pontos de coleta, lixeiras, descartes, categorias, pontuações e notificações. Também foram adicionadas validações de intervalo para o nível da lixeira, quantidade mínima para o descarte, unicidade de e-mail, CPF e código da lixeira, além de proteção contra exclusões que poderiam quebrar o histórico.

Nas entidades operacionais em que a preservação do histórico é necessária, foi criada uma base de exclusão lógica com os campos `is_active` e `deleted_at`. O gerenciador padrão omite os registros inativos das consultas comuns, mas os dados continuam armazenados para rastreabilidade e auditoria.

As configurações sensíveis são recebidas por variáveis de ambiente. O arquivo de exemplo apresenta as variáveis necessárias para a chave do Django, credenciais do PostgreSQL, hosts permitidos e origem autorizada pelo CORS. O projeto também possui Dockerfile e Docker Compose para iniciar a API e o PostgreSQL de forma reproduzível.

Foram implementados endpoints para cadastro, login, renovação do token, consulta e alteração de dados pessoais, alteração de senha, resumo da conta, listagem de pontos de coleta, busca de lixeira por código, criação e histórico de descartes, ranking, notificações do gestor, suspensão de usuários e estatísticas iniciais do dashboard.

Para verificar o núcleo implementado, foram criados sete testes automatizados. Os testes confirmam que usuários não autenticados não registram descartes, campos obrigatórios são validados, o nível 4 gera notificação ao gestor, a pontuação é registrada, o histórico não expõe dados de outro usuário, administradores conseguem suspender contas e usuários comuns não possuem essa permissão. Todos os sete testes foram executados com sucesso, sem falhas.

Nesta fase, o backend já oferece funcionalidades reais e persistentes, mas ainda não representa o sistema completo. Permanecem como evoluções a leitura efetiva do QR Code no frontend, o fluxo de confirmação da coleta pelo gestor, o cálculo dos tempos médios de coleta, a recuperação de senha, a autenticação social e a substituição das informações mockadas do frontend pelas chamadas à API.
