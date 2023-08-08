# IOTproject


<ul>
  <li>Setup environment</li>
  
  ``python -m venv venv`` <br />
  ``. venv/bin/activate``
  <li>install dependencies</li>

  ``pip install -e . `` <br />
  ``source cd flaskr/static && npm install``
  <li>Initializing database</li>

  ``flask init_db  --debug run``
  <li>Testing</li>
  
``python -m pytest -caputre=yes``
  <li>Running</li>

``flask --app flaskr --debug run``

