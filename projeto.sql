CREATE SCHEMA Projeto;
USE Projeto;

-- Verificar tabelas do Banco
SHOW TABLES;
SELECT @@hostname;

-- Remover tabelas, mas apenas para casos extremos
DROP TABLE Usuario;
DROP TABLE TipoUsuario;

DROP TABLE Labs;
DROP TABLE Uso_Lab;

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
    CONSTRAINT uk_email_Usuario UNIQUE (email),
	CONSTRAINT fk_id_TipoUsuario_Usuario FOREIGN KEY (id_tipo) REFERENCES TipoUsuario (id)
);

CREATE TABLE Uso_Lab(
	id INT NOT NULL AUTO_INCREMENT,
    resultado VARCHAR(50) NOT NULL,
    CONSTRAINT pk_id_Uso_Lab PRIMARY KEY (id)
) AUTO_INCREMENT = 0;


CREATE TABLE Labs (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    tipo_status INT NOT NULL,
    disponibilidade INT NOT NULL, -- Para disponível 1 e para indisponível 2
    CONSTRAINT pk_id_Labs PRIMARY KEY (id),
    CONSTRAINT fk_registro_Labs_Uso_Lab FOREIGN KEY (tipo_status) REFERENCES Uso_Lab (id)
);


-- Testes de inserções USUÁRIOS
INSERT INTO TipoUsuario(nome_tipo)
VALUES('professor'), ('alunos'), ('admin');

INSERT INTO Usuario(nome, email, senha, cpf, telefone, id_tipo, atividade)
VALUES('Joao', 'joao@email.com', 'jvsenha', '78509099332', '9912345678', 3, '1');

-- Teste inserção Labs
INSERT INTO Uso_Lab(resultado)
VALUES('Ativado'), ('Desativado');

INSERT INTO Labs(nome, tipo_status, disponibilidade)
VALUES("salax", 0, 0), ("salay", 1, 1);

-- Verificar Respostas
SELECT * FROM TipoUsuario;
SELECT * FROM Usuario;
SELECT * FROM Uso_Lab;
SELECT * FROM Labs;

-- SELECT id FROM Usuario WHERE email='Bia@Bia' AND senha='123';
