CREATE DATABASE fcvolei;
USE fcvolei;
CREATE TABLE `fcvolei`.`partidos`
  (
     `nombre_liga` VARCHAR(50) NOT NULL,
     `grupo`       VARCHAR(50) NOT NULL,
     `numero_jornada`     VARCHAR(20) NOT NULL,
     `local`       VARCHAR(50) NOT NULL,
     `visitant`   VARCHAR(50) NOT NULL,
     `dia`         VARCHAR(10) NOT NULL,
     `hora`        VARCHAR(10) NOT NULL,
     `lugar`       VARCHAR(50) NOT NULL,
     PRIMARY KEY (`nombre_liga`, `grupo`, `numero_jornada`, `local`,`visitant`)
  )
engine = innodb;
