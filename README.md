# IOTproject


<ul>
  <li>Setup environment</li>
  
  ``python -m venv venv`` <br />
  ``. venv/bin/activate``
  <li>install dependencies</li>

  ``pip install -e . `` <br />
  ``source cd flaskr/static && npm install``
  <li>Initializing database</li>

  ``flask --app flaskr init-db``
  <li>Testing</li>
  
``source cd tests/ && python -m pytest -caputre=yes``
  <li>Running</li>

``flask --app flaskr --debug run``

