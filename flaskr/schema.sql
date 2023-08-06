DROP TABLE IF EXISTS Iotdata;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Sensors;
DROP TABLE IF EXISTS Devices;


CREATE TABLE User (
    id          INTEGER    PRIMARY KEY AUTOINCREMENT,
    username    TEXT       UNIQUE NOT NULL,
    password    TEXT       NOT NULL
);

CREATE TABLE Sensors(
  id            INTEGER     PRIMARY KEY,
  sensor_name   TEXT        UNIQUE NOT NULL,
  unit          TEXT        
);

CREATE TABLE Devices(
  id            INTEGER     PRIMARY KEY,
  device_name   TEXT        UNIQUE NOT NULL,
  details       TEXT,
  city          TEXT,
  coordinates   TEXT
);

CREATE TABLE Iotdata (
  id            INTEGER     PRIMARY KEY AUTOINCREMENT,
  author_id     INTEGER     NOT NULL,
  device_id     INTEGER     NOT NULL,
  created_time  DATETIME    DEFAULT CURRENT_TIMESTAMP,
  sampled_time  DATETIME    NOT NULL,
  sensor_id     INTEGER     NOT NULL,
  sensor_value  REAL        NOT NULL,
  FOREIGN KEY (author_id) REFERENCES User (id),
  FOREIGN KEY (sensor_id) REFERENCES Sensors (id),
  FOREIGN KEY (device_id) REFERENCES Devices (id)
);

