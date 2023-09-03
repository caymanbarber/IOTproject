

var state = {
    devices : [],
    sensors : [],
    openItem : null,
    getObjects(objType) {
        const url = "/devices/api/get_"+objType;
        console.log(url);

        fetch(url)
        .then((response) => {
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => { 
            var items = data.items;
            console.log(objType + ": " +items);
            this.loadObjects(objType, items);
        })
        .catch((error) => {
            // Handle errors
            console.error('Fetch error:', error);
        });
    },
    addObject(objType, object){

        const url = "/devices/api/add_"+objType;
        fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
            body: object.getJSON()
        })
        .then(response => response.json())
        .then(data => {

            console.log(data);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });

        if (objType == 'device') {
            state.devices.push(object);

        } else if(objType == 'sensor') {
            state.sensors.push(object);
        }

    },
    loadObjects(objType, jsonList){
        console.log(objType);
        var display = new ListView(objType);
        
        if(objType == "device") {
            this.devices = []
            for(var item of jsonList) {
                this.devices.push(
                    new Device(item.id, item.device_name, item.details, item.city, item.coordinates)
                );
            }
            display.displayItems(this.devices);
        } else if(objType == "sensor") {
            this.sensors = [];
            for(var item of jsonList) {
                this.sensors.push(
                    new Sensor(item.id, item.sensor_name, item.unit)
                );
            }
            display.displayItems(this.sensors);  
        }    
    },
    updateObject(objType, object) {
        const url = "/devices/api/update_"+objType+"/"+object.id;
        
        fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: object.getJSON()
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    },
    deleteObject(objType, objectID) {
        const url = "/devices/api/delete_"+objType+"/"+objectID;
        
        fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    }
};

$(function() {
    state.getObjects("device");
    state.getObjects("sensor");
    

    $(".lists").on('click', 'li div.edit', function(event) {
        event.stopPropagation();

        var id = $(this).parent().children(".id").text();
        
        if(state.openItem != null) {
            state.openItem.next();
            state.openItem.next().find("#id");
            console.log(state.openItem.next().find("#id").val());
            if(state.openItem.next().find("#id").val() == id) {
                state.openItem.next().remove();
                state.openItem = null;
                return;
            } else {
                state.openItem.next().remove();
            }
        }

        
        var clickedObjType = $(this).parent().parent().attr('id');
        var object = null;
        
        if(clickedObjType == 'sensors') {
            for(let sensor of state.sensors) {
                if (sensor.id ==Number(id)) {
                    object = sensor;
                    break;
                }
            }
        } else if(clickedObjType == 'devices') {
            for(let device of state.devices) {
                if (device.id ==Number(id)) {
                    object = device;
                    break;
                }
            }
        }

        state.openItem = $(this).parent();
        let form = object.form;
        state.openItem.after(form);
    });

    $(".lists").on('click', 'li div.save', function(event) {
        var form = $(this).parent().parent();
        var clickedObjType = form.parent().attr('id');
        var obj;
        let name = form.find("#name").val();
        let id = form.find("#id").val();
        
        console.log("id: " + id+ " name: "+name);

        // Require Name and ID
        if (!id || !name) {
            let origColor = form.css("background-color");
            form.css("background-color", "coral");
            form.animate({
                backgroundColor: origColor 
            }, 250);
            return
        }

        // Save each data point from each field
        if (clickedObjType == 'devices') {
            let details = form.find("#details").val();
            let city = form.find("#city").val();
            let coords = form.find("#coordinates").val();
            obj = new Device(id, name, details, city, coords);

        } else if(clickedObjType == 'sensors') {
            let unit = form.find("#unit").val();
            obj = new Sensor(id, name, unit);
        }

        let objType = clickedObjType.substring(0, clickedObjType.length - 1);
        let url = "/devices/api/get_"+objType;
        console.log(url);
        fetch(url)
        .then((response) => {
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => { 
            var items = data.items;

            console.log(items.map(function(element){
                return element.id;
            }));

            // If id in server update server
            if (items.map(function(element){
                    return element.id;
                }).includes(Number(obj.id)) ){

                state.updateObject(objType, obj);
            } else {
                state.addObject(objType, obj);
                form.parent().append(obj.entry);
            }
            form.remove();
        })
        .catch((error) => {
            console.error('Fetch error:', error);
        });

    });

    $(".lists").on('click', 'li div.delete', function(event) {
        var form = $(this).parent().parent();
        var clickedObjType = form.parent().attr('id');
        let id = form.find("#id").val();

        let objType = clickedObjType.substring(0, clickedObjType.length - 1);
        let url = "/devices/api/get_"+objType;
        console.log(url);
        fetch(url)
        .then((response) => {
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => { 
            var items = data.items;

            console.log(items.map(function(element){
                return element.id;
            }));

            // If id in server update server
            if (items.map(function(element){
                return element.id;
            }).includes(Number(id)) ){
                state.deleteObject(objType, id);
            } else {
                let origColor = form.css("background-color");
                form.css("background-color", "coral");
                form.animate({
                    backgroundColor: origColor 
                }, 250);
                return  
            }
        })
        .catch((error) => {
            console.error('Fetch error:', error);
        });

        form.prev().remove();
        form.remove();

        
        // Close form, send update to server, update list
    });

    $(".column ").on('click', 'div.button.register', function(event) {
        var clickedObjType = $(this).prev().attr('id');
        var tempObj;
        if (clickedObjType == 'devices') {
            tempObj = new Device(null, "", "", "", "");
        } else if(clickedObjType == 'sensors') {
            tempObj = new Sensor(null, "", "");
        }

        $(this).prev().append(tempObj.form);

        // Add new entry to list with empty name
        // Add form
        // Require Name and ID
        // Null if empty
        // Close form, send update to server, update list
    });
});



class ListView {
    objType;
    constructor(objType) {
        this.objType = objType;
    };

    displayItems(items) {
        console.log(items);
        for(let item of items) {
            if(this.objType == "sensor") {
                console.log("shoiuld be sensor. is: "+this.objType);
                console.log(item.entry);
                $("#sensors").append(item.entry);
            } else if(this.objType == "device") {
                console.log("shoiuld be device. is: "+this.objType);
                console.log(item.entry);
                $("#devices").append(item.entry);
                
            }   
        }
    }

    displaySettings() {

    }

};

class Object {
    id = null;
    name = null;
    entry = null;

    constructor(id, name) {
        this.id = id;
        this.name = name;
        this.makeEntry();
    }

    set setID (id) {
        this.id = id;
    };

    set setName (name) {
        this.name = name;
    };

    makeEntry() {
        this.entry = `
        <li class="entry">
            <div class = "id">${this.id}</div>
            <div class = "name">${this.name}</div>
            <div class = "button edit">edit</div>
        </li>
        `;
    }
};

class Device extends Object {
    details = null;
    city = null;
    coordinates = null;
    form = null;

    constructor(id, name, details, city, coordinates) {
        super(id, name);
        this.details = details;
        this.city = city;
        this.coordinates = coordinates;
        this.makeForm();
    }

    set setDetails(details) {
        this.details = details;
    }

    set setCity(city) {
        this.city = city;
    }

    set setCoordinates(coordinates) {
        this.coordinates = coordinates;
    }

    getJSON() {
        return JSON.stringify({ id: this.id, device_name: this.name, details: this.details, city: this.city, coordinates: this.coordinates});
    }

    update() {
        this.makeForm();
        super.makeEntry();
    }

    makeForm() {
        this.form = `
        <li class="form">
            <input type="number" id="id" name="id" min="0" placeholder="Sensor ID" value=${this.id}>
            <input type="text" id="name" name="name" placeholder="Sensor Name" value="${this.name}">
            <input type="text" id="details" name="details" placeholder="Details" value="${this.details}">
            <input type="text" id="city" name="city" placeholder="City" value="${this.city}">
            <input type="text" id="coordinates" name="coordinates" placeholder="Coordinates" value="${this.coordinates}">
            <div class="buttons">
                <div class = "button delete">Delete</div>
                <div class = "button save">Save</div>
            </div>
        </li>
        `;
    }
};

class Sensor extends Object {
    unit = null;
    form = null;
    
    constructor(id, name, unit) {
        super(id, name);
        this.unit = unit;
        this.makeForm();
    }

    set setUnit(unit) {
        this.unit = unit;
    }

    getJSON() {
        return JSON.stringify({ id: this.id, sensor_name: this.name, unit: this.unit});
    }

    update() {
        this.makeForm();
        super.makeEntry();
    }

    makeForm() {
        this.form = `
        <li class="form">
            <input type="number" id="id" name="id" min="0" placeholder="Sensor ID" value=${this.id}>
            <input type="text" id="name" name="name" placeholder="Sensor Name" value="${this.name}">
            <input type="text" id="unit" name="unit" placeholder="Unit" value="${this.unit}">
            <div class="buttons">
                <div class = "button delete">Delete</div>
                <div class = "button save">Save</div>
            </div>
        </li>
        `;
    }
};

