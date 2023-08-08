# IOTproject


<ul>
  <li>Setup environment</li>
  
  ``python -m venv .``
  <li>install dependencies</li>

  ``pip install -e . `` <br />
  ``cd flaskr/static`` <br />
  ``npm install``
  <li>Initializing database</li>

  ``flask init_db  --debug run``
  <li>Testing</li>
  
``python -m pytest -caputre=yes``
  <li>Running</li>

``flask --app flaskr --debug run``

