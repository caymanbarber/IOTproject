DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Iotdata;

CREATE TABLE User (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT,
    username        TEXT       UNIQUE NOT NULL,
    password    TEXT       NOT NULL
);

CREATE TABLE Iotdata (
  id            INTEGER     PRIMARY KEY AUTOINCREMENT,
  author_id     INTEGER     NOT NULL,
  device_id     INTEGER     NOT NULL,
  created_time  DATETIME    DEFAULT CURRENT_TIMESTAMP,
  sampled_time  DATETIME    NOT NULL,
  sensor_id     INTEGER     NOT NULL,
  sensor_value  REAL        NOT NULL,
  FOREIGN KEY (author_id) REFERENCES User (id)
);