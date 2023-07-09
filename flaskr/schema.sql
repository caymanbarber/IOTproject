DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Sensor;
DROP TABLE IF EXISTS Devices;
DROP TABLE IF EXISTS Iotdata;

CREATE TABLE User (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT,
    username        TEXT       UNIQUE NOT NULL,
    password    TEXT       NOT NULL
);

CREATE TABLE Iotdata (
  id            INTEGER     PRIMARY KEY AUTOINCREMENT,
  device_id     INTEGER     NOT NULL,
  created_time  DATETIME    DEFAULT CURRENT_TIMESTAMP,
  sampled_time  DATETIME    NOT NULL,
  sensor_id     INTEGER     NOT NULL,
  sensor_value  REAL        NOT NULL
);