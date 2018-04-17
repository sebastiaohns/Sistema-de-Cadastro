drop table if exists entries;
create table membro (
  id integer primary key autoincrement,
  nome text not null,
  matricula integer,
  telefone integer,
  email text,
  senha text not null
);