class mtecConnectModbus {
    constructor(frequencyInverterID="01") {
        this.settings = {
            "frequencyInverterID": frequencyInverterID,
            "keepAlive": {
                "command": "03FD000001",
                "interval": 250,
                "callback": undefined,
                "active": true
            },
            "serial": {
                baudRate: 19200,
                dataBits: 8,
                stopBits: 2,
                parity: "none",
                flowControl: "none"
            },
            "log": false,
            "sendCallback": undefined,
            "receivedCallback": undefined
        }
        this.temp = {
            "sendBuffer": [],
            "valueBuffer": [],
            "readBuffer": [],
            "sendReady": false,
            "lastSpeed": 0
        }
        this.available = ("serial" in navigator);
        this.connected = false;
    }

    async connect() {
        this.serialStart();
        await this.until(_=>this.connected);
        // ToDo: return true/false
        return true;
    }

    async serialStart() {
        this.port = await navigator.serial.requestPort();
        await this.port.open(this.settings.serial);
        this.active = true;
        this.reader = this.port.readable.getReader();
        this.temp.sendReady = true;
        this.connected = true;
        if (this.settings.log) {
            console.log("connected ");
        }
        this.readLoop();
    }

    async readLoop() {
        while (true) {
            const {value, done} = await this.reader.read();
            if (value) {
                if (this.settings.log) {
                    console.log("read      ", value);
                }
                this.received(value);
            }
        }
    }

    async sendCommand(parameter, value) {
        return await this.sendHexCommand(this.settings.frequencyInverterID + parameter + this.int2hex(value, 4));
    }

    async sendHexCommand(command) {
        this.temp.sendBuffer.push(command + this.calcCRC(command));
        this.sendHex();
        await this.until(_=>this.temp.valueBuffer.length > 0);
        var b = this.temp.valueBuffer.shift();
        console.log(b);
        var commandvalue = b.value;
        this.keepAlive();
        return commandvalue;
    }

    async keepAlive() {
        if (this.settings.keepAlive.active) {
            this.settings.keepAlive.loop = setTimeout(async()=>{
                clearTimeout(this.settings.keepAlive.loop);

                if (typeof this.settings.keepAlive.command == "function") {
                    var c = this.settings.keepAlive.command();
                } else {
                    var c = this.settings.keepAlive.command;
                }

                var command = this.settings.frequencyInverterID + c;
                this.temp.sendBuffer.push(command + this.calcCRC(command));
                this.sendHex();
                await this.until(_=>this.temp.valueBuffer.length > 0);
                var b = this.temp.valueBuffer.shift();
                var value = b.value;
                if (typeof this.settings.keepAlive.callback == "function" && b.type == 3) {
                    this.settings.keepAlive.callback(value);
                }

                this.keepAlive();
            }
            , this.settings.keepAlive.interval);
        }
    }

    sendHex() {
        if (this.temp.sendReady && this.temp.sendBuffer.length > 0) {
            this.send(this.temp.sendBuffer.shift());
        }
    }

    send(hex) {

        if (typeof this.settings.sendCallback == "function") {
            this.settings.sendCallback(hex);
        }

        this.temp.sendReady = false;
        var hexArray = this.hex2array(hex);
        const writer = this.port.writable.getWriter();
        writer.write(hexArray);
        writer.releaseLock();
        if (this.settings.log) {
            console.group();
            console.log("sent      " + hexArray);
        }
    }

    received(inputValues) {
        for (var value of inputValues) {
            this.temp.readBuffer.push(value);
        }
        var values = this.temp.readBuffer;

        var completeDataLength = Infinity;
        if (this.temp.readBuffer.length >= 3) {
            if (this.temp.readBuffer[1] == 3) {
                // Type: read
                var dataLength = this.temp.readBuffer[2];
                completeDataLength = 3 + dataLength + 2;
                // ID, Type, Length, <Length>, checksum, checksum
            } else if (this.temp.readBuffer[1] == 6) {
                // Type: write single Block
                completeDataLength = 8;
            }
        }

        if (this.temp.readBuffer.length >= completeDataLength) {
            if (this.settings.log) {
                console.log("received  " + this.temp.readBuffer);
                console.groupEnd();
            }
            this.temp.readBuffer = this.temp.readBuffer.slice(completeDataLength);

            var message = new Object();
            message.fcID = values[0];
            message.type = values[1];
            if (message.type == 6) {
                message.param = this.int2hex(values[2] * 256 + values[3], 4);
                message.value = values[4] * 256 + values[5];
                message.crc = this.int2hex(values[6] * 256 + values[7], 4);
            } else if (message.type == 3) {
                message.length = this.int2hex(values[2], 2);
                message.value = 0
                for (var i = 0; i < dataLength; i++) {
                    message.value *= 256;
                    message.value += values[i + 3];
                }
                message.crc = this.int2hex(values[5] * 256 + values[6], 4);
            }
            var command = "";
            for (var i = 0; i < completeDataLength; i++) {
                command += this.int2hex(values[i], 2);
            }
            if (this.calcCRC(command) != message.crc) {// ToDo: bad CRC
            }
            this.temp.valueBuffer.push(message);

            if (typeof this.settings.receivedCallback == "function") {
                this.settings.receivedCallback(command + message.crc);
            }

            this.temp.sendReady = true;
            this.sendHex();
        }
    }

    until(conditionFunction) {
        const poll = resolve=>{
            if (conditionFunction())
                resolve();
            else
                setTimeout(_=>poll(resolve), 10);
        }
        return new Promise(poll);
    }

    calcCRC(command) {
        var buffer = this.hex2array(command);
        var crc = 0xFFFF;
        for (var pos = 0; pos < buffer.length; pos++) {
            crc ^= buffer[pos];
            for (var i = 8; i != 0; i--) {
                if ((crc & 0x0001) != 0) {
                    crc >>= 1;
                    crc ^= 0xA001;
                } else
                    crc >>= 1;
            }
        }
        var reversed = (crc % 256) * 256 + Math.floor(crc / 256);
        var crcstr = reversed.toString(16);
        while (crcstr.length < 4) {
            crcstr = "0" + crcstr;
        }
        return crcstr.toString(16).toUpperCase();
    }

    int2hex(value, length) {
        var s = Math.round(value).toString(16).toUpperCase();
        while (s.length < length) {
            s = "0" + s;
        }
        return s;
    }
    hex2int(hex) {
        return parseInt(hex, 16);
    }
    hex2array(hexString) {
        return new Uint8Array(hexString.match(/.{1,2}/g).map(byte=>parseInt(byte, 16)));
    }

    get ready() {
        return (async()=>{
            var switches = await this.sendCommand("03FD06", 1);
            return ((switches % 32) - (switches % 16) != 0);
        }
        )();
    }
    set ready(value) {
        throw new Error("ready not setable");
    }

    get frequency() {
        return (async()=>{
            return await this.sendCommand("03FD00", 1) / 100;
        }
        )();
    }
    set frequency(value) {
        return (async()=>{
            return await this.sendCommand("06FA01", value * 100);
        }
        )();
    }

    get voltage() {
        return (async()=>{
            return await this.sendCommand("03FD05", 1) / 100;
        }
        )();
    }
    set voltage(value) {
        throw new Error("voltage not setable");
    }

    get current() {
        return (async()=>{
            return await this.sendCommand("03FD03", 1) / 100;
        }
        )();
    }
    set current(value) {
        throw new Error("current not setable");
    }

    get torque() {
        return (async()=>{
            return await this.sendCommand("03FD18", 1) / 100;
        }
        )();
    }
    set torque(value) {
        throw new Error("torque not setable");
    }

    async start() {
        return await this.sendHexCommand(this.settings.frequencyInverterID + "06FA00C400");
    }
    async startReverse() {
        return await this.sendHexCommand(this.settings.frequencyInverterID + "06FA00C600");
    }
    async stop() {
        return await this.sendHexCommand(this.settings.frequencyInverterID + "06FA000000");
    }
    async emergencyStop() {
        return await this.sendHexCommand(this.settings.frequencyInverterID + "06FA001000");
    }

    get speed() {
        throw new Error("speed not getable");
    }

    set speed(value) {
        return (async()=>{
            if (value != this.temp.lastSpeed) {
                if (value == 0) {
                    this.stop();
                } else {
                    if (value < 0 && !(this.temp.lastSpeed < 0)) {
                        await this.startReverse();
                    } else if (value > 0 && !(this.temp.lastSpeed > 0)) {
                        await this.start();
                    }
                    await (this.frequency = Math.abs(value));
                }
            }
            this.temp.lastSpeed = value;
        }
        )();
    }
}