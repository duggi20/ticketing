-- Airbyte's MySQL source reads the binlog as a replication client rather than
-- polling tables, so it needs replication grants in addition to SELECT.
CREATE USER IF NOT EXISTS 'airbyte'@'%' IDENTIFIED BY 'airbytepw';

GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT
  ON *.* TO 'airbyte'@'%';

FLUSH PRIVILEGES;
