Minha Biblioteca
Alexandre Sanson - 1711450

Sistema de gerenciamento de leituras integrado à Google Books API, desenvolvido em Python
utilizando o Framework Django.

Deploy: Railway - https://inf1407trabalho1-production.up.railway.app/ || https://agsbiblioteca.dev.br/

O usuário é inicialmente apresentado à tela de login, que contém também um botão para permitir cadastro de novos
usuários.

Na página Home, são listados os livros cadastrados, e através da barra de busca o usuário pode realizar uma consulta
através da API Google Books, podendo adicionar um dos livros apresentados à lista. Também está disponível um campo para
a inserção de anotações pessoais em cada livro.

A biblioteca disponibiliza imagens das capas por meio de URLs obtidas do Google Books, que ocasionalmente
apresentam falhas na exibição.

O link no nome de usuário redireciona para a página de configuração de perfil, onde o usuário pode redefinir 
seu nome ou senha.

Foi implementada a funcionalidade de envio de email para confirmação de criação de conta e recuperação de senha.