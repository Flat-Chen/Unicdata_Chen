let asc_key = "jeH3O1VX";
let base_lv = "nHnsU4cX";

function desDecrypt(a) {
    a = a.replace(/\s*/g, "");
    let tmpiv = CryptoJS.enc.Utf8.parse("nHnsU4cX");
    var b = CryptoJS.enc.Utf8.parse("jeH3O1VX");
    var c = CryptoJS.DES.decrypt({
        ciphertext: CryptoJS.enc.Base64.parse(a)
    }, b, {
        iv: CryptoJS.enc.Utf8.parse("nHnsU4cX"),
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
        formatter: CryptoJS.format.OpenSSL
    });
    return c.toString(CryptoJS.enc.Utf8)
}

words = (2) [1850240627, 1429496664], latin1Str = "nHnsU4cX"

function parse() {
    // Shortcut
    var latin1StrLength = latin1Str.length;

    // Convert
    var words = [];
    for (var i = 0; i < latin1StrLength; i++) {
        words[i >>> 2] |= (latin1Str.charCodeAt(i) & 0xff) << (24 - (i % 4) * 8);
    }

    return new WordArray.init(words, latin1StrLength);
}



var subInit = WordArray.init = function (typedArray) {
    // Convert buffers to uint8
    if (typedArray instanceof ArrayBuffer) {
        typedArray = new Uint8Array(typedArray);
    }

    // Convert other array views to uint8
    if (
        typedArray instanceof Int8Array ||
        (typeof Uint8ClampedArray !== "undefined" && typedArray instanceof Uint8ClampedArray) ||
        typedArray instanceof Int16Array ||
        typedArray instanceof Uint16Array ||
        typedArray instanceof Int32Array ||
        typedArray instanceof Uint32Array ||
        typedArray instanceof Float32Array ||
        typedArray instanceof Float64Array
    ) {
        typedArray = new Uint8Array(typedArray.buffer, typedArray.byteOffset, typedArray.byteLength);
    }

    // Handle Uint8Array
    if (typedArray instanceof Uint8Array) {
        // Shortcut
        var typedArrayByteLength = typedArray.byteLength;

        // Extract bytes
        var words = [];
        for (var i = 0; i < 8; i++) {
            words[i >>> 2] |= typedArray[i] << (24 - (i % 4) * 8);
        }

        // Initialize this word array
        superInit.call(this, words, typedArrayByteLength);
    } else {
        // Else call normal init
        superInit.apply(this, arguments);
    }
}