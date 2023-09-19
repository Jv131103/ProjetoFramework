CREATE SCHEMA Projeto;
USE Projeto;

-- Verificar tabelas do Banco
SHOW TABLES;
SELECT @@hostname;

-- Remover tabelas, mas apenas para casos extremos
DROP TABLE Usuario;
DROP TABLE TipoUsuario; -- Pode adicionar outra no lugar!

CREATE TABLE TipoUsuario(
	id INT NOT NULL AUTO_INCREMENT,
    nome_tipo VARCHAR(255) NOT NULL,
    CONSTRAINT pk_id_TipoUsuario PRIMARY KEY (id)
);


CREATE TABLE Usuario(
	id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    cpf VARCHAR(20) NOT NULL,
    telefone VARCHAR(255) NOT NULL,
    id_tipo INT NOT NULL,
    atividade VARCHAR(1) NOT NULL,
    CONSTRAINT pk_id_Usuario PRIMARY KEY (id),
    CONSTRAINT uk_cpf_Usuario UNIQUE (cpf),
	CONSTRAINT fk_id_TipoUsuario_Usuario FOREIGN KEY (id_tipo) REFERENCES TipoUsuario (id)
);

-- Testes de inserções
INSERT INTO TipoUsuario(nome_tipo)
VALUES('professor'), ('alunos');

INSERT INTO Usuario(nome, email, senha, cpf, telefone, id_tipo, atividade)
VALUES('NomeProfessor', 'email@professor', 'SenhaProfessor', 'cpfProfessor',
'telefoneProfessor', 1, '1'), ('NomeAluno', 'email@aluno', 'SenhaAluno', 
'cpfAluno', 'telefoneAluno', 2, '0');

-- Verificar Respostas

SELECT * FROM TipoUsuario;
SELECT * FROM Usuario;
